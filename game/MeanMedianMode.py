import spyral
import extras
import fraction_tools
from fractions import Fraction
import random
import string
import conversation

WIDTH = 1200
HEIGHT = 900
SIZE = (WIDTH,HEIGHT)
FONT_SIZE = 42
BG_COLOR = (0, 0, 0)
FG_COLOR = (255, 255, 255)

RESULT_TIME = 10
FINISH_TIME = 60
FINISH = 3

VILLAGERS = ["images/Villager.png"
    ]
    
class Villager(spyral.Sprite):
    def __init__(self,x,y):
        super(Villager, self).__init__()
        #Villager Stuff
        self.layer = 'bottom'
        self.selected = 0
        self.voff = 60
        
        #Spyral Stuff
        selection = random.randrange(0,2)
        fle = "images/Character Boy.png"
        if(selection != 0):
            fle = "images/Character Horn Girl.png"
        self.image = spyral.Image(filename=fle)
        self.anchor = 'center'
        self.layer = 'bottom'
        self.pos = (x,y)
        self.x = x
        self.y = y

        self.number = random.randrange(1,15)
        self.text = extras.Text(str(self.number),64,(x,y+self.voff),color=(255,255,255),font_size=24)
        self.text.font_size = 24
        self.text.anchor = 'center'
        self.text.layer = "top"
        self.text.x = x
        self.text.y = y+self.voff
        self.text.pos = (x,y+self.voff)

        self.billboard = spyral.Sprite()
        self.billboard.image = spyral.Image(filename="images/Billboard.png")
        self.billboard.anchor = 'center'
        self.billboard.pos = (x,y)
        self.billboard.x = x
        self.billboard.y = y+self.voff
        self.billboard.layer = 'middle'

        if(self.text.y != y):
            print "Not ON TOp Of Head!"
        else:
            print "jklfjaljdklfjaslkdjf What the hell!"
        #add_child(self.billboard)
        
    def check_click(self, position):
        return self.get_rect().collide_point(position)
    def move(self,position):
        if(self.selected == 1):
            self.pos = position
            self.text.pos = (position[0],position[1]+self.voff)
            self.billboard.pos = (position[0],position[1]+self.voff)
    def select(self,tpe):
        self.selected = 1
    def deselect(self):
        self.selected = 0
    def set_number(self, number):
        self.number = number
        self.text = extras.Text(str(number),64,(self.x,self.y+self.voff),color=(255,255,255), font_size=24)
        
class MeanMedianMode(spyral.Scene):
    def __init__(self,correct=0):
        super(MeanMedianMode, self).__init__()
        
        self.time_end = RESULT_TIME
        self.timer = self.time_end+1
        self.createmode = 0
        self.modenum = 0
        
        self.correct = correct
        print correct
        self.camera = self.parent_camera.make_child(virtual_size = (WIDTH, HEIGHT), layers=['bottom', 'middle','top'])

        self.group = spyral.Group(self.camera)
        self.text = spyral.Group(self.camera)

        self.Ftext = extras.Text("Great Job!", (600, 450), (WIDTH/2, HEIGHT/2), layer='toptop', font_size=110,color=(255,255,255))
        self.group.add(self.Ftext)
        if(self.correct < FINISH):
            self.Ftext.visible = 0
            
        self.multiselect = 0
        self.multimax = 1
        
        self.mean = 0
        self.median = 0
        self.mode = 0

        self.VillagerList = []
        self.NumberList = []
        
        self.ListofText = ["Hey this is a conversation Box.",
                           "The problem is I cannot get more than one line to draw.",
                           "Using multiline strings will not work so instead",
                           "We should just use it like this."]
        self.ListofNames = ["Random Villager #1",
                           "Mohamed Dicko",
                           "Super Grandiose Man of Infinite Wisdom",
                           "A Pair of Pants"]
        self.conversation = conversation.Conversation([self.ListofNames,self.ListofText],(0,HEIGHT+10),self,w=WIDTH,h=HEIGHT,tcolor=(0,0,0))
        self.group.add(self.conversation.button)
        self.text.add(self.conversation.next)
        self.text.add(self.conversation.visibletext)
        self.text.add(self.conversation.nametext)

        self.totalnumber = random.randrange(5,8,2)
        for count in range(2,self.totalnumber):
            nvil = Villager(random.randrange(200+(WIDTH-400)),random.randrange(200+(HEIGHT-500)))
            if(self.createmode > 0)and(self.createmode < random.randrange(2,4))and(self.totalnumber != 5):
                nvil.set_number(self.modenum)
                self.createmode += 1
            if(self.createmode == 0)and(self.modenum == 0)and(self.totalnumber != 5):
                self.modenum = nvil.number
                self.createmode += 1
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
            self.group.add(villager.billboard)

        self.Selectable = []
        #self.meantext = extras.TextBox("Enter Mean",(WIDTH/5,HEIGHT-140),self.mean)
        #self.mediantext = extras.TextBox("Enter Median",((WIDTH/5)*2,HEIGHT-140),self.median)
        #self.modetext = extras.TextBox("Enter Mode",((WIDTH/5)*3,HEIGHT-140),self.get_mode(self.NumberList))

        self.meantext = extras.TextBox("Enter Mean",(WIDTH/2,HEIGHT-140),self.mean)
        self.mediantext = extras.TextBox("Enter Median",(WIDTH/2,HEIGHT-140),self.median)
        self.modetext = extras.TextBox("Enter Mode",(WIDTH/2,HEIGHT-140),self.get_mode(self.NumberList))

        rnd = random.randrange(0,100)            
        if(len(self.VillagerList) <= 3):
            if(rnd < 90):
                self.meantext.visible = 1
                self.mediantext.visible = 0
                self.modetext.visible = 0

                self.type = self.meantext
                rnd = 900
                print "Showing Mean"
        if(rnd < 40):
            self.meantext.visible = 0
            self.mediantext.visible = 1
            self.modetext.visible = 0

            self.type = self.mediantext
            rnd = 900
            print "Showing Median"
        if(rnd > 39)and(rnd < 101): 
            self.meantext.visible = 0
            self.mediantext.visible = 0
            self.modetext.visible = 1

            self.type = self.modetext
            print "Showing Mode"

        self.Selectable.append(self.meantext)
        self.Selectable.append(self.mediantext)
        self.Selectable.append(self.modetext)
        
        for s in self.Selectable:
            if(s.visible == 0):
                s.description.visible = 0
                s.btext.visible = 0
                s.button.visible = 0
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
        background = spyral.Image(filename="images/Mean Median Mode BG.png")
        self.camera.set_background(background)
        print self.camera.layers()
        
    def render(self):
        self.group.draw()
        self.text.draw()
        
    def check_click(self, position, group, select):
        local_position = self.camera.world_to_local(position)
        for sprite in group:
            sprite.deselect()
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
        #Updating Conversations
        if(self.conversation != 0):
            self.conversation.update_text()
        #Restarting the game
        if(self.timer < self.time_end):
            self.timer += 1
            print "Timer: "+str(self.timer)
        if(self.timer == self.time_end):
            print "Correct: "+str(self.correct)
            if(self.correct == FINISH):
                return spyral.director.pop()
            return spyral.director.replace(MeanMedianMode(self.correct))
        #Check for any new/relevant events
        for event in self.event_handler.get():
            if(self.correct >= FINISH):
                break
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
                if(event['ascii'] == chr(13))and(self.timer > RESULT_TIME):
                    self.correct += self.type.get_answer()
                    if(self.correct == FINISH):
                        self.Ftext.visible = 1
                        self.timer = 0
                        self.time_end = FINISH_TIME
                    self.timer = 0
                #ascii 8 is backspace key
                if event['ascii'] == chr(8):
                    txt = self.get_type(self.type)
                    txt = txt[:len(txt)-2]
                    self.set_type(txt,self.type)

                #ascii 122 is the z key
                if event['ascii'] == chr(122) or event['ascii'] == chr(13):
                    if(self.conversation != 0):
                        if(self.conversation.currentposition < len(self.conversation.ctext)-1):
                            self.conversation.quick_end()
                            return
                        if(self.conversation.currentposition >= len(self.conversation.ctext)-1):
                            self.conversation.to_next()
                            return
            elif event['type'] == "MOUSEBUTTONDOWN":
                self.check_click(event['pos'], self.Selectable,1)
            elif event['type'] == "MOUSEBUTTONUP":
                self.deselect(self.Selectable)
            elif event['type'] == 'MOUSEMOTION':
                self.moveselected(event['pos'])
