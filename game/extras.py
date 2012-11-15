import spyral

FONT_PATH = "fonts/bertoltbrecht.ttf"

#Essentially just a wrapper for a rectangle with click detection.
#I have been using it as the base for a button.  Once you make one of these,
#just make some Text and layer the Text on top of the Button
class Button(spyral.Sprite):
    def __init__(self, position, image_size=None, filename=None, anchor='center', layer='all', fill=(255,255,255)):

        super(Button, self).__init__()
        if filename == None and image_size != None:
            self.image = spyral.Image(size=image_size)
            self.image.fill(fill)
        elif filename != None:
            self.image = spyral.Image(filename)
        else:
            raise ValueError("Need either a filename or an image_size")
        
        self.layer = layer
        self.anchor = anchor
        self.pos = position

    def check_click(self, position):
        return self.get_rect().collide_point(position)

#I've used it as the top layer of a button, but could be used for text anywhere on the screen
#Generates a sprite from some text, size and position. Currenlty defaults to the font constant,
#but that can easily be changed to support multiple fonts
class Text(spyral.Sprite):
    def __init__(self, text, image_size, position, anchor='center', layer='all', font_size=14, color=(0,0,0)):

        super(Text, self).__init__()
        #self.image = spyral.Image(size=image_size)
        self.font_size = font_size
        self.color = color
        self.image = spyral.Font(FONT_PATH, font_size, color).render(text)
        self.layer = layer
        self.anchor = anchor
        self.pos = position
        self.text = text

    def set_text(self, text):
        self.image = spyral.Font(FONT_PATH, self.font_size, self.color).render(text)
        self.text = text
    def get_text(self):
        return self.text

class TextBox(spyral.Sprite):
    def __init__(self,dtext,position,answer, button_image="",width=200,height=20,anchor='topleft',layer='all',font_size=14,dcolor=(255,255,255),tcolor=(255,255,0)):

        super(TextBox,self).__init__()
        self.answer = answer
        self.selected = 0

        self.dtext = dtext
        self.position = position
        self.button_image = button_image
        self.anchor = anchor
        self.font_size = font_size
        self.tcolor = tcolor
        self.dcolor = dcolor

        self.description = Text(dtext,64,(position[0],position[1]-30),anchor=self.anchor,color=self.dcolor,font_size=self.font_size)
        
        self.button = spyral.Sprite()
        self.button.image = spyral.Image(size = (width,height))
        self.button.image.fill((0,0,255))
        self.button.anchor = self.anchor
        self.button.pos = (self.position[0],self.position[1]-5)

        self.btext = Text("",64,position,layer=100,anchor=self.anchor,color=self.tcolor,font_size=self.font_size)
        
        if(button_image != ""):
            self.button.image = spyral.Image(filename=self.button_image)
            
    def set_text(self, text):
        self.btext.image = spyral.Font(FONT_PATH, self.font_size, self.tcolor).render(text)
        self.btext.text = text
    def get_text(self):
        return self.btext.text

    def check_click(self, position):
        self.ret = self.button.get_rect().collide_point(position)
        return self.ret
    def select(self,tpe):
        tpe.type = self
    def deselect(self):
        return 0
    def move(self,pos):
        return 0
    def get_answer(self):
        self.set_text(filter(lambda x: x.isdigit(), self.get_text()))
        if(self.get_text() == ""):
            self.set_text("-1")
        print "Converted to Integer: "+self.get_text()
        if(int(self.get_text()) == self.answer):
            self.set_text("Correct")
            self.btext.text = ""
            print "Correct"
        else:
            self.set_text("Wrong - Correct Answer: "+str(self.answer))
            self.btext.text = ""
            print "Wrong"
            return
