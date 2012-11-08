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
        self.lines = spyral.Group(self.camera)
        self.buttons = spyral.Group(self.camera)
        main_box = extras.Button((WIDTH/2, HEIGHT/2-100), image_size=(BOX_W, BOX_H), layer='bottom', group=self.main_group)

        box_bottom = (HEIGHT/2-100) + (BOX_H/2)
        box_top = box_bottom - BOX_H
        box_left = (WIDTH/2) - (BOX_W/2)
        box_right = box_left + BOX_W
        self.bb = box_bottom
        self.bl = box_left
        d = fractions[0].denominator
        #Horizontal Lines and Vertical Slider
        for x in xrange(0, d+1):
            temp_line = extras.Button((box_left, box_top+x*(BOX_H/d)), image_size=(BOX_W, 6), anchor='topleft', layer='grid_lines', fill=(0,0,0), group=self.lines)
            temp_line.orientation = 'horizontal'
            fraction_label = extras.Text(str(d-x) + "/" + str(d), (48, 24), (box_left - 23, box_top+x*(BOX_H/d)), group=self.main_group, font_size=20)

        #Vertical Lines and Horizontal Slider
        d = fractions[1].denominator
        for x in xrange(0, d+1):
            temp_line = extras.Button((box_left+x*(BOX_W/d), box_bottom), image_size=(6, BOX_H), anchor='bottomleft', layer='grid_lines', fill=(0,0,0), group=self.lines)
            temp_line.orientation = 'vertical'
            fraction_label = extras.Text(str(x) + "/" + str(d), (48, 24), (box_left+x*(BOX_W/d), box_bottom + 18), group=self.main_group, font_size=20)

        self.shaded_box = spyral.Sprite(self.main_group)
        self.shaded_box.image = spyral.Image(size=(0,0))

        self.vertical_slider = extras.Button((box_left - 80, box_bottom), image_size=(48,24), group=self.buttons)
        self.vertical_slider.dragging = False
        self.vertical_slider.clicked = lambda: self.dragging(self.vertical_slider)
        
        self.horizontal_slider = extras.Button((box_left, box_bottom + 65), image_size=(24,48), group=self.buttons)
        self.horizontal_slider.dragging = False
        self.horizontal_slider.clicked = lambda: self.dragging(self.horizontal_slider)

    def update(self, dt):
        
        #Check for any new/relevant events
        for event in self.event_handler.get():
            #Check to see if they clicked a button or slider
            if event['type'] == 'MOUSEBUTTONDOWN':
                self.check_click(event['pos'], self.buttons.sprites())
            elif event['type'] == 'MOUSEBUTTONUP':
                for button in self.buttons.sprites():
                    button.dragging = False
            if (event['type'] == 'MOUSEMOTION'):
                if self.horizontal_slider.dragging:
                    self.check_drag(event['pos'], self.horizontal_slider)
                elif self.vertical_slider.dragging:
                    self.check_drag(event['pos'], self.vertical_slider)
            #They clicked the OS exit button at the top of the frame
            elif event['type'] == 'QUIT':
                spyral.director.pop()
                return

    def on_enter(self):
        
        background = spyral.Image(size=(WIDTH, HEIGHT))
        background.fill((194,194,194))
        self.camera.set_background(background)

    def render(self):
        self.main_group.draw()
        self.lines.draw()
        self.buttons.draw()
        
    def check_click(self, position, group):
        local_position = self.camera.world_to_local(position)
        for sprite in group:
            if sprite.check_click(local_position):
                #This method needs to be set with a lambda function
                sprite.clicked()

    def check_drag(self, position, slider):
        lines = []
        for line in self.lines.sprites():
            if (slider == self.horizontal_slider) and (line.orientation == 'vertical'):
                lines.append(line.x)
            elif (slider == self.vertical_slider) and (line.orientation == 'horizontal'):
                lines.append(line.y)
        lines.sort()
        print "Left", self.bl, "Bottom", self.bb
        print "Mouse", position
        print lines
        x = 0
        if (slider == self.horizontal_slider):
            mouse_position = self.camera.world_to_local(position)[0]
        elif (slider == self.vertical_slider):
            mouse_position = self.camera.world_to_local(position)[1]
            
        while x < len(lines) and mouse_position >= lines[x]:
            x += 1

        #if x == len(lines):
            #return
        if x == 0:
            x += 1 #since we are subtracting by one below, add one to prevent wrap-around
            
        if slider == self.horizontal_slider and slider.x != lines[x-1]:
            slider.x = lines[x-1]
        elif slider == self.vertical_slider and slider.y != lines[x-1]:
            slider.y = lines[x-1]

    def dragging(self, slider):
        slider.dragging = True
