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

    def set_text(self, text):
        self.image = spyral.Font(FONT_PATH, self.font_size, self.color).render(text)
