import spyral
import math
import operator
import extras

FONT_PATH = "fonts/00TT.TTF"


class Conversation(spyral.Sprite):
    def __init__(self,tlist,position,scene,w=1200,h=900,button_image="",anchor='bottomleft',layer=100,font_size=24,dcolor=(255,255,255),tcolor=(255,0,255)):

        super(Conversation,self).__init__()
        self.scene = scene
        self.tlist = tlist

        self.wdth = w
        self.heght = h/6
        
        self.tlist = tlist
        self.position = position
        self.button_image = button_image
        self.anchor = anchor
        self.font_size = font_size
        self.tcolor = tcolor
        self.dcolor = dcolor
        self.layer = "toptop"

        self.currentposition = 0
        self.currenttext = 0

        self.ctext = self.tlist[self.currenttext]
        self.visibletext = extras.Text(self.ctext[:self.currentposition], 64, (self.position[0]+8,self.position[1]-(self.heght)+5),anchor='topleft',color=self.tcolor,font_size=self.font_size,layer=self.layer)
        self.visibletext.layer = self.layer
        
        self.button = spyral.Sprite()
        self.button.image = spyral.Image(size = (self.wdth,self.heght))
        self.button.image.fill((0,255,0))
        self.button.anchor = self.anchor
        self.button.pos = (self.position[0],self.position[1]-5)
        self.button.layer = "top"
        self.button.visible = 1

        self.next = extras.Text("Press Z",64,(self.wdth,self.position[1]-3),anchor='bottomright',color=self.tcolor,font_size=self.font_size,layer=self.layer)
        self.next.visible = 0
        
        if(button_image != ""):
            self.button.image = spyral.Image(filename=self.button_image)
    def update_text(self):
        if(self.currentposition < len(self.ctext)):
            self.currentposition += 1
            #self.visibletext.set_text(self.ctext[:self.currentposition])
            self.visibletext.layer = self.layer

            #self.button.image = spyral.Image(size = (self.wdth,self.heght))
            #self.button.image.fill((0,255,0))
            self.next.visible = 0
        if(self.currentposition >= len(self.ctext)):
            self.next.visible = 1
    def quick_end(self):
        self.currentposition = len(self.ctext)
        #self.visibletext.set_text(self.ctext[:self.currentposition])
        self.visibletext.layer = self.layer
        print "Ending Text"
    def to_next(self):
        if(self.currenttext < len(self.tlist)-1):
            self.currentposition = 0
            self.currenttext += 1
            self.ctext = self.tlist[self.currenttext]
            #self.visibletext.set_text(self.ctext[:self.currentposition])
            self.visibletext.layer = self.layer
            return
        if(self.currenttext >= len(self.tlist)-1):
            self.visible = 0
            self.visibletext.visible = 0
            self.button.visible = 0
            return
        print "Going to next text"
    def set_text(self, tlist):
        self.tlist = tlist
    def get_text(self):
        return self.tlist

    def check_click(self, position):
        self.ret = self.button.get_rect().collide_point(position)
        return self.ret
