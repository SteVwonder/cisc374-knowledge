import spyral
import math
pyFraction = __import__('fractions')

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
