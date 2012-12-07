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

VILLAGERS = ["images/Villager.png"
    ]
    
class Villager(spyral.Sprite):
    def __init__(self,x,y,biggest):
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

        self.number = random.randrange(1,biggest)
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
    def __init__(self,difficulty,correct=0,firsttime=1,gender="Hero",name="Hero"):
        super(MeanMedianMode, self).__init__()

        self.gender = gender
        self.name = name
        
        self.time_end = RESULT_TIME
        self.timer = self.time_end+1
        self.createmode = 0
        self.modenum = 0
        self.difficulty = difficulty

        if(self.difficulty == 1):
            self.FINISH = 3
            self.biggest = 5
        if(self.difficulty == 2):
            self.FINISH = 5
            self.biggest = 9
        if(self.difficulty == 3):
            self.FINISH = 7
            self.biggest = 15
        
        self.correct = correct
        print "Correct Answer IS: "+str(correct)
        self.camera = self.parent_camera.make_child(virtual_size = (WIDTH, HEIGHT), layers=['bottom', 'middle','top'])

        self.group = spyral.Group(self.camera)
        self.text = spyral.Group(self.camera)

        self.Ftext = extras.Text("Great Job!", (600, 450), (WIDTH/2, HEIGHT/2), layer='toptop', font_size=110,color=(0,0,255))
        self.CorrectAnswer = extras.Text("", (600, 450), (WIDTH/2, HEIGHT/2), layer='toptop', font_size=55,color=(255,0,0))
        self.MON = extras.Text("Press Enter When You've got the Answer", (600,450),(WIDTH, HEIGHT), layer='bottom', anchor='bottomright',font_size=32,color=(0,0,0))
        
        self.group.add(self.Ftext)
        self.group.add(self.CorrectAnswer)
        self.group.add(self.MON)
        if(self.correct < self.FINISH):
            self.Ftext.visible = 0
            
        self.multiselect = 0
        self.multimax = 1
        
        self.mean = 0
        self.median = 0
        self.mode = 0

        self.VillagerList = []
        self.NumberList = []
        
        self.ListofText = ["Help us "+self.name+"! The wizard came and trapped us in boxes!",
                           "These boxes are magic and cant be broken by anything!",
                           "I think the wizard is hiding with us!",
                           "Move us around and find the Mean, Median and Mode of us to find the Wizard!",
                           "Click on the box and type in the answer when you think you've got it.",
                           "Press Enter to confirm your desicision."]
        self.ListofNames = ["Random Villager",
                           "Random Villager",
                           "Random Villager",
                            "Random Villager",
                            "Random Villager",
                           "Random Villager"]
        if(firsttime == 1)and(self.difficulty == 1):
            self.conversation = conversation.Conversation([self.ListofNames,self.ListofText],(0,HEIGHT+10),self,w=WIDTH,h=HEIGHT,tcolor=(0,0,0))
            self.group.add(self.conversation.button)
            self.text.add(self.conversation.next)
            self.text.add(self.conversation.visibletext)
            self.text.add(self.conversation.nametext)
        else:
            self.conversation = 0

        self.totalnumber = random.randrange(5,8,2)
        for count in range(2,self.totalnumber):
            nvil = Villager(200+(random.randrange(WIDTH-400)),200+random.randrange(HEIGHT-500),self.biggest)
            if(self.createmode > 0)and(self.createmode < random.randrange(3,4))and(self.totalnumber >= 5):
                nvil.set_number(self.modenum)
                self.createmode += 1
            if(self.createmode == 0)and(self.modenum == 0)and(self.totalnumber != 5):
                self.modenum = nvil.number
                self.createmode += 1
            if(self.mean != 0):
                if(count == self.totalnumber-1):
                    while((nvil.number+self.mean) % (len(self.VillagerList)+1) != 0):
                        print "Fixing MEAN : "+str(nvil.number)+" % "+str((len(self.VillagerList)+1))+" = "+str((nvil.number+self.mean) % (len(self.VillagerList)+1))
                        nvil.set_number(nvil.number+1)
                print "Fixed MEAN : "+str(nvil.number)+" % "+str((len(self.VillagerList)+1))+" = "+str((nvil.number+self.mean) % (len(self.VillagerList)+1))
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
            if(rnd != -1):
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
        #Check for any new/relevant events
        for event in self.event_handler.get():
            if(self.correct >= self.FINISH):
                break
            #They clicked the OS exit button at the top of the frame
            if event['type'] == 'QUIT':
                spyral.director.pop()
                return
            #They clicked somewhere
            elif event['type'] == 'KEYDOWN':
                self.ntext = self.get_type(self.type)+event['ascii']
                self.set_type(self.ntext,self.type)
                #print "Typing: "+self.type.dtext
                #ascii 27 is escape key
                if event['ascii'] == chr(27):
                    spyral.director.pop()
                    return
                #ascii 13 is enter key
                if(event['ascii'] == chr(13)):
                    self.canswer = self.type.get_answer()
                    if(self.canswer != None):
                        self.correct += self.canswer
                        print "Correct Answers:"+str(self.correct)
                        if(self.correct == self.FINISH):
                            self.Ftext.visible = 1
                            self.timer = 0
                            self.time_end = FINISH_TIME
                        else:
                            self.CorrectAnswer.visible = 1
                            if(self.canswer == 0):
                                self.CorrectAnswer.set_text("The Answer Was:   "+str(self.type.answer))
                            else:
                                self.CorrectAnswer.set_text("Only "+str(self.FINISH-self.correct)+" more to go!")
                            self.timer = 0
                            self.time_end = FINISH_TIME
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
        #Restarting the game
        if(self.timer < self.time_end):
            self.timer += 1
            #print "Timer: "+str(self.timer)
        if(self.timer == self.time_end):           
            print "Correct Amount: "+str(self.correct)+"/"+str(self.FINISH)
            if(self.correct == self.FINISH):
                village_selection_scene = spyral.director._stack[-3]
                village_selection_scene.MMM_difficulty = min(self.difficulty + 1,3)
                spyral.director.pop()
                spyral.director.pop()
            else:
                return spyral.director.replace(MeanMedianMode(self.difficulty,correct=self.correct,firsttime=0))
