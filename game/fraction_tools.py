import spyral
import extras

WIDTH = 1200
HEIGHT = 900

BOX_W = 500
BOX_H = 500

LINE_THICKNESS = 5
# The fraction tools
# Several widgets that help the kids visualize fractional operations

class FractionTools(spyral.Scene):
    def __init__(self, difficulty, fractions, operation):
        super(FractionTools, self).__init__()

        self.camera = self.parent_camera.make_child(virtual_size = (WIDTH, HEIGHT), layers=['bottom', 'all', 'shaded', 'grid_lines'])
        
        self.main_group = spyral.Group(self.camera)
        main_box = extras.Button((WIDTH/2, HEIGHT/2-100), image_size=(BOX_W, BOX_H), layer='bottom', group=self.main_group)

        box_bottom = (HEIGHT/2-100) + (BOX_H/2)
        box_top = box_bottom - BOX_H
        box_left = (WIDTH/2) - (BOX_W/2)
        box_right = box_left + BOX_W
        
        d = fractions[0].denominator
        #Horizontal Lines and Vertical Slider
        for x in xrange(0, d+1):
            temp_line = extras.Button((box_left, box_top+x*(BOX_H/d)), image_size=(BOX_W, 6), anchor='topleft', layer='grid_lines', fill=(0,0,0))
            fraction_label = extras.Text(str(d-x) + "/" + str(d), (48, 24), (box_left - 23, box_top+x*(BOX_H/d)), group=self.main_group, font_size=20)
            self.main_group.add(temp_line)

        #Vertical Lines and Horizontal Slider
        d = fractions[1].denominator
        for x in xrange(0, d+1):
            temp_line = extras.Button((box_left+x*(BOX_W/d), box_bottom), image_size=(6, BOX_H), anchor='bottomleft', layer='grid_lines', fill=(0,0,0))
            #fraction_label =
            fraction_label = extras.Text(str(x) + "/" + str(d), (48, 24), (box_left+x*(BOX_W/d), box_bottom + 18), group=self.main_group, font_size=20)
            self.main_group.add(temp_line)

        self.shaded_box = spyral.Sprite(self.main_group)
        self.shaded_box.image = spyral.Image(size=(0,0))
        
        self.vertical_slider = spyral.Sprite(self.main_group)
        self.vertical_slider.image = spyral.Image(size=(48,24))
        self.vertical_slider.image.fill((255,255,255))
        self.vertical_slider.anchor = 'center'
        self.vertical_slider.position = (box_left - 80, box_bottom)
        
        self.horizontal_slider = spyral.Sprite(self.main_group)
        self.horizontal_slider.image = spyral.Image(size=(24,48))
        self.horizontal_slider.image.fill((255,255,255))
        self.horizontal_slider.anchor = 'center'
        self.horizontal_slider.position = (box_left, box_bottom + 65)

    def update(self, dt):
        
        #Check for any new/relevant events
        for event in self.event_handler.get():
            #They clicked the OS exit button at the top of the frame
            if event['type'] == 'QUIT':
                spyral.director.pop()
                return

    def on_enter(self):
        
        background = spyral.Image(size=(WIDTH, HEIGHT))
        background.fill((194,194,194))
        self.camera.set_background(background)

    def render(self):
        self.main_group.draw()
