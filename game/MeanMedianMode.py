import spyral
import extras
import fraction_tools
from fractions import Fraction
import random
import string

WIDTH = 1200
HEIGHT = 900
SIZE = (WIDTH,HEIGHT)
FONT_SIZE = 42
BG_COLOR = (0, 0, 0)
FG_COLOR = (255, 255, 255)

VILLAGERS = ["images/Villager.png"
    ]
    
class Villager(spyral.Sprite):
    def __init__(self,x,y):
        super(Villager, self).__init__()
        #Villager Stuff
        self.layer = 1
        self.selected = 0
        
        #Spyral Stuff

        self.image = spyral.Image(filename="images/Villager.png")
        self.anchor = 'center'
        self.pos = (x,y)
        self.x = x
        self.y = y

        self.number = random.randrange(10,50)
        self.text = extras.Text(str(self.number),64,self.pos,color=(255,255,255))
        
    def check_click(self, position):
        return self.get_rect().collide_point(position)
    def move(self,position):
        if(self.selected == 1):
            self.pos = position
            self.text.pos = position
    def select(self,tpe):
        self.selected = 1
        self.layer = 2
    def deselect(self):
        self.selected = 0
        self.layer = 1
        
class MeanMedianMode(spyral.Scene):
    def __init__(self, *args, **kwargs):
        super(MeanMedianMode, self).__init__(*args, **kwargs)

        self.camera = self.parent_camera.make_child(virtual_size = (WIDTH, HEIGHT), layers=['bottom', 'top'])

        self.group = spyral.Group(self.camera)
        self.text = spyral.Group(self.camera)

        self.multiselect = 0
        self.multimax = 1
        
        self.mean = 0
        self.median = 0
        self.mode = 0

        self.VillagerList = []
        self.NumberList = []
        
        for count in range(2,random.randrange(5,12,2)):
            nvil = Villager(random.randrange(200+(WIDTH-400)),random.randrange(200+(HEIGHT-500)))
            self.VillagerList.append(nvil)
            self.text.add(nvil.text)
            self.NumberList.append(nvil.number)
            self.mean += nvil.number

        self.mean /= len(self.VillagerList)
        print "Mean = "+str(self.mean)

        self.NumberList.sort()
        self.median = self.NumberList[int(len(self.NumberList)/2)]
        print "Median = "+str(self.median)

        for villager in self.VillagerList:
            self.group.add(villager)

        self.Selectable = []
        self.meantext = extras.TextBox("Enter Mean",(WIDTH/5,HEIGHT-140),self.mean)
        self.mediantext = extras.TextBox("Enter Median",((WIDTH/5)*2,HEIGHT-140),self.median)
        self.modetext = extras.TextBox("Enter Mode",((WIDTH/5)*3,HEIGHT-140),self.get_mode(self.NumberList))
        self.type = self.meantext

        self.Selectable.append(self.meantext)
        self.Selectable.append(self.mediantext)
        self.Selectable.append(self.modetext)
        
        for s in self.Selectable:
            self.text.add(s.description)
            self.text.add(s.btext)
            self.group.add(s.button)
            
        self.Selectable.extend(self.VillagerList)

    def get_mode (self,numberlist):
        mode = max(map(lambda val: (numberlist.count(val), val), set(numberlist)))
        if(mode[0] == 1):
            return 0
        else:
            return mode[1]
            
    def get_type(self,Text):
        return Text.get_text()

    def set_type(self,text,Text):
        return Text.set_text(text)
    
    def on_enter(self):
        background = spyral.Image(size=(WIDTH,HEIGHT))
        background.fill((0, 0, 0))
        self.camera.set_background(background)
        
    def render(self):
        self.group.draw()
        self.text.draw()
        
    def check_click(self, position, group, select):
        local_position = self.camera.world_to_local(position)
        for sprite in group:
            if sprite.check_click(local_position):
                sprite.move(local_position)
                if(select == 1)and(self.multiselect < self.multimax):
                    sprite.select(self)
                    self.multiselect += 1
        self.multiselect = 0

    def deselect(self,List):
        for obj in List:
            if(obj.selected == 1):
                obj.deselect()
    
    def moveselected(self,position):
        local_position = self.camera.world_to_local(position)
        for v in self.VillagerList:
            if(v.selected == 1):
                v.move(local_position)
    
    def update(self, dt):
        #Check for any new/relevant events
        for event in self.event_handler.get():
            #They clicked the OS exit button at the top of the frame
            if event['type'] == 'QUIT':
                spyral.director.pop()
                return
            #They clicked somewhere
            elif event['type'] == 'KEYDOWN':
                self.ntext = self.get_type(self.type)+event['ascii']
                self.set_type(self.ntext,self.type)
                print self.type.dtext
                #ascii 27 is escape key
                if event['ascii'] == chr(27):
                    spyral.director.pop()
                    return
                #ascii 13 is enter key
                if event['ascii'] == chr(13):
                    return self.type.get_answer()
                #ascii 8 is backspace key
                if event['ascii'] == chr(8):
                    txt = self.get_type(self.type)
                    txt = txt[:len(txt)-2]
                    self.set_type(txt,self.type)
            elif event['type'] == "MOUSEBUTTONDOWN":
                self.check_click(event['pos'], self.Selectable,1)
            elif event['type'] == "MOUSEBUTTONUP":
                self.deselect(self.Selectable)
            elif event['type'] == 'MOUSEMOTION':
                self.moveselected(event['pos'])
