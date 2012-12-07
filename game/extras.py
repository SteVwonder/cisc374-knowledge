import spyral
import math
import operator

pyFraction = __import__('fractions')

FONT_PATH = "fonts/cooper.ttf"

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

        super(Text, self).__init__(group=group)
        #self.image = spyral.Image(size=image_size)
        self.font_size = font_size
        self.color = color
        self.image = spyral.Font(FONT_PATH, self.font_size, color).render(text)
        self.layer = layer
        self.anchor = anchor
        self.pos = position
        self.text = text

    def set_text(self, text):
        self.image = spyral.Font(FONT_PATH, self.font_size, self.color).render(text)
        self.text = text
    def get_text(self):
        return self.text

# Allows writing multiple lines of text to be much easier and only uses one image
# by using a blank image with the size specifications and spyral.Image's draw_image
# to draw each line of text onto the basic image. Takes a list of separate lines,
# one string containing newlines or a plain string. Also includes text-wrapping
#   -- spacing : vertical space between text lines, 0 spaces evenly over the height
#   -- columns : allows formatting with columns, following argument is an option
#   -- order   : "topdown" fills the first column first, second column second, etc.
#		 "leftright" fills the first row first, second row second, etc.
class MultiLineText(spyral.Sprite):
    def __init__(self, text, image_size, position, spacing=0, columns=1, order="topdown", alignment='left', anchor='topleft', layer='all', font_size=14, color=(0,0,0), group=None):

	super(MultiLineText, self).__init__(group=group)
	self.font_size = font_size
	self.color = color
	self.layer = layer
	self.anchor = anchor
	self.pos = position
	self.spacing = spacing
	self.columns = columns
	self.order = order
	self.alignment = alignment
	self.image = spyral.Image(size=image_size)
	self.wdth = (image_size[0]/columns)
	self.texts = []
	self.text = []

	if ('\n' in text):
	    self.text = text.split('\n')
	elif (isinstance(text, str)):
	    self.text.append(text)
	else:
	    self.text = text

	for line in self.text:
	    nline = line
	    while (True):
		proj_width = spyral.Font(FONT_PATH, font_size, color).get_size(nline)[0]
		end = self.wdth*len(nline)/proj_width
		start = 9*self.wdth*len(nline)/proj_width/10
		if ((proj_width < self.wdth) or (start < 0 )):
		    break

		space = nline.find(' ', start, end)
		if (space < 0):
		    start -= 10
		    continue
		
		self.texts.append(spyral.Font(FONT_PATH, font_size, color).render(nline[:space]))
		nline = nline[space+1:]
		
	    self.texts.append(spyral.Font(FONT_PATH, font_size, color).render(nline))
	
	if (spacing == 0):
	    self.spacing = (((image_size[1]*self.columns) - (len(self.texts)*font_size))/len(self.texts))

	offset = 0
	column_pos = 0
	for line in self.texts:
	    self.image.draw_image(line, (column_pos, offset))
	    if (self.columns > 1) and (self.order == "leftright"):
		column_pos += self.wdth
		if (column_pos >= image_size[0]):
		    column_pos = 0
		    offset += (self.spacing + font_size)
	    else:
		offset += (self.spacing + font_size)
		if (self.columns > 1) and (offset >= image_size[1]):
		    offset = 0
		    column_pos += self.wdth

class TextBox(spyral.Sprite):
    def __init__(self,dtext,position,answer, button_image="",width=200,height=30,anchor='center',layer='all',font_size=24,dcolor=(0,0,0),tcolor=(255,255,0)):

        super(TextBox,self).__init__()
        self.answer = answer
        self.selected = 0
        self.selecting = 0

        self.wdth = width
        self.heght = height
        
        self.dtext = dtext
        self.position = position
        self.button_image = button_image
        self.anchor = anchor
        self.font_size = font_size
        self.tcolor = tcolor
        self.dcolor = dcolor

        self.description = Text(dtext,64,(position[0],position[1]-30),anchor=self.anchor,color=self.dcolor,font_size=self.font_size)
        self.description.layer = "bottom"
        
        self.button = spyral.Sprite()
        self.button.image = spyral.Image(size = (width,height))
        self.button.image.fill((255,0,255))
        self.button.anchor = self.anchor
        self.button.pos = (self.position[0],self.position[1]+1)
        self.button.layer = "bottom"

        self.btext = Text("",64,position,layer=100,anchor=self.anchor,color=self.tcolor,font_size=self.font_size)
        self.btext.layer = "top"
        
        if(button_image != ""):
            self.button.image = spyral.Image(filename=self.button_image)
            
    def set_text(self, text):
        if(self.selecting == 1) and (self.visible == 1):
            self.btext.image = spyral.Font(FONT_PATH, self.font_size, self.tcolor).render(text)
            self.btext.text = text
            self.btext.layer = 10
    def get_text(self):
        return self.btext.text

    def check_click(self, position):
	if(self.visible == 1):
	    self.ret = self.button.get_rect().collide_point(position)
	    return self.ret
    def select(self,tpe):
	if(self.visible == 1):
	    tpe.type = self
	    self.button.image = spyral.Image(size = (self.wdth,self.heght))
	    self.button.image.fill((0,0,255))
	    self.button.anchor = self.anchor
	    self.selecting = 1
    def deselect(self):
	if(self.visible == 1):
	    self.button.image = spyral.Image(size = (self.wdth,self.heght))
	    self.button.image.fill((255,0,255))
	    self.button.anchor = self.anchor
	    self.selecting = 0
	    return 0
    def move(self,pos):
        return 0
    def get_answer(self):
        if(self.selecting == 1) and (self.visible == 1):
            self.set_text(filter(lambda x: x.isdigit(), self.get_text()))
            if(self.get_text() == ""):
                self.set_text("-1")
            #print "Converted to Integer: "+self.get_text()
            if(int(self.get_text()) == self.answer):
                self.set_text("Correct")
                self.btext.text = ""
                #print "Correct"
                return 1
            else:
                self.set_text(str(self.answer))
                self.btext.text = ""
                #print "Wrong"
                return 0

class Fraction():
    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator
    
    def gcd(self):
        d = self.denominator
        n = self.numerator
        while d:
            d, n = n%d, d
        return n
        
    def reduce(self):
        if (self.denominator != 0) and (self.numerator != 1):
            greatest = self.gcd()
            n = self.numerator / greatest
            d = self.denominator / greatest
            return Fraction(n, d)
        else:
            return self

    def __str__(self):
        temp_fraction = self.reduce()
        if(temp_fraction.denominator != 1):
            return str(temp_fraction.numerator) + "/" + str(temp_fraction.denominator)
        else:
            return str(temp_fraction.numerator)

    def __add__(a, b):
        if a.denominator == b.denominator:
            return Fraction(a.numerator + b.numerator, a.denominator)
        else:
            return Fraction(a.numerator * b.denominator +
                            b.numerator * a.denominator,
                            a.denominator * b.denominator)
   
    def __sub__(a, b):
        if (a.denominator == b.denominator):
            return Fraction(a.numerator - b.numerator, a.denominator)
        else:
            temp =Fraction(a.numerator * b.denominator -
                            b.numerator * a.denominator,
                            a.denominator * b.denominator)
            temp.reduce
            return temp

    def _richcmp(self, other, op):
        return op(self.numerator * other.denominator,
                  self.denominator * other.numerator)
    #raise ValueError("Cannot compare fractions with differenct denominators YET!")

    def __lt__(a, b):
        """a < b"""
        return a._richcmp(b, operator.lt)
    
    def __gt__(a, b):
        """a > b"""
        return a._richcmp(b, operator.gt)
    
    def __le__(a, b):
        """a <= b"""
        return a._richcmp(b, operator.le)
    
    def __ge__(a, b):
        """a >= b"""
        return a._richcmp(b, operator.ge)

    def __eq__(a, b):
        """a == b"""
        c = a.reduce()
        d = b.reduce()
        return (c.numerator == d.numerator and
                c.denominator == d.denominator)

    def __mul__(a, b):
        """a * b"""
        return Fraction(a.numerator * b.numerator, a.denominator * b.denominator)
    
    def lcm(a, b):
        def gcd(a, b):
            while b:
                b, a = a%b, b
            return a
        return ( a * b ) / gcd(a, b)
