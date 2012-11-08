import spyral
import math

FONT_PATH = "fonts/00TT.TTF"

#Essentially just a wrapper for a rectangle with click detection.
#I have been using it as the base for a button.  Once you make one of these,
#just make some Text and layer the Text on top of the Button
class Button(spyral.Sprite):
    def __init__(self, position, image_size=None, filename=None, anchor='center', layer='all', fill=(255,255,255), group=None):

        super(Button, self).__init__(group)
            
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
    def __init__(self, text, image_size, position, anchor='center', layer='all', font_size=14, color=(0,0,0), group=None):

        super(Text, self).__init__(group)
        #self.image = spyral.Image(size=image_size)
        self.font_size = font_size
        self.color = color
        self.image = spyral.Font(FONT_PATH, font_size, color).render(text)
        self.layer = layer
        self.anchor = anchor
        self.pos = position

    def set_text(self, text):
        self.image = spyral.Font(FONT_PATH, self.font_size, self.color).render(text)

#class DottedLine(spyral.AggregateSprite):
    # def __init__(self, image_size, dot_length, position, group, fill=(0,0,0), layer='grid_lines'):

    #     super(DottedLine, self).__init__(group)
        
    #     self.image = spyral.Image(size=image_size)
    #     self.pos = position
    #     self.layer = layer

    #     if(image_size[0] >= image_size[1]):
    #         line_length = image_size[0]
    #         direction = 'horizontal'
    #     else:
    #         line_length = image_size[1]
    #         direction = 'vertical'
            
    #     number_of_dots = math.floor(line_length/dot_length/2)
    #     number_of_dots = int(number_of_dots)
        
    #     if direction == 'horizontal':
    #         for x in xrange(number_of_dots):
    #             temp_sprite = spyral.Sprite()
    #             temp_sprite.image = spyral.Image(size=(dot_length/(number_of_dots * 2), image_size[1]))
    #             temp_sprite.image.fill(fill)
    #             temp_sprite.position = (position[0] + (x * 2 * dot_length), position[1])
    #             temp_sprite.layer = layer
    #             self.add_child(temp_sprite)
    #     elif direction == 'vertical':
    #         for x in xrange(number_of_dots):
    #             temp_sprite = spyral.Sprite()
    #             temp_sprite.image = spyral.Image(size=(image_size[0], dot_length/(number_of_dots * 2)))
    #             temp_sprite.image.fill(fill)
    #             temp_sprite.position = (position[0], position[1] + (x * 2 * dot_length))
    #             temp_sprite.layer = layer
    #             self.add_child(temp_sprite)
