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
    def __init__(self, difficulty, fractions, operation,firsttime = 1,gender="Hero",name="Hero"):
        super(FractionTools, self).__init__()

        self.camera = self.parent_camera.make_child(virtual_size = (WIDTH, HEIGHT), layers=['bottom', 'all', 'shaded', 'grid_lines'])
        self.difficulty = difficulty

        self.gender=gender
        self.name = name
        
        self.main_group = spyral.Group(self.camera)
        self.vertical_lines = spyral.Group(self.camera)
        self.horizontal_lines = spyral.Group(self.camera)
        self.buttons = spyral.Group(self.camera)
        
        #Setup Conversations
        self.ListofText = ["Help, <Name Here> the wizard came and trapped us in boxes!",
                           "These boxes are magic and cant be broken by anything!",
                           "I think the wizard is hiding with us!",
                           "Move us around and find the Mean, Median and Mode of us to find the Wizard!"]
        self.ListofNames = ["Random Villager",
                           "Random Villager",
                           "Random Villager",
                           "Random Villager"]
        if(firsttime == 1)and(self.difficulty == 1):
            self.conversation = conversation.Conversation([self.ListofNames,self.ListofText],(0,HEIGHT+10),self,w=WIDTH,h=HEIGHT,tcolor=(0,0,0))
            self.main_group.add(self.conversation.button)
            self.main_group.add(self.conversation.next)
            self.main_group.add(self.conversation.visibletext)
            self.main_group.add(self.conversation.nametext)
        else:
            self.conversation = 0 

        main_box = extras.Button((WIDTH/3, HEIGHT/2-100), image_size=(BOX_W, BOX_H), layer='bottom', group=self.main_group)

        box_bottom = (HEIGHT/2-100) + (BOX_H/2)
        box_top = box_bottom - BOX_H
        box_left = (WIDTH/3) - (BOX_W/2)
        box_right = box_left + BOX_W
        self.bb = box_bottom
        self.bl = box_left
        self.bt = box_top
        d = fractions[0].denominator
        self.num_of_horizontal_lines = d + 1
        #Horizontal Lines and Vertical Slider
        for x in xrange(0, d+1):
            extras.Button((box_left, box_top+x*(BOX_H/d)), image_size=(BOX_W, 6), anchor='topleft', layer='grid_lines', fill=(0,0,0), group=self.horizontal_lines)
            extras.Text(str(d-x) + "/" + str(d), (48, 24), (box_left - 23, box_top+x*(BOX_H/d)), group=self.main_group, font_size=20, layer='all')

        #Vertical Lines and Horizontal Slider
        d = fractions[1].denominator
        self.num_of_vertical_lines = d + 1
        for x in xrange(0, d+1):
            extras.Button((box_left+x*(BOX_W/d), box_bottom), image_size=(6, BOX_H), anchor='bottomleft', layer='grid_lines', fill=(0,0,0), group=self.vertical_lines)
            extras.Text(str(x) + "/" + str(d), (48, 24), (box_left+x*(BOX_W/d), box_bottom + 18), group=self.main_group, font_size=20, layer='all')

        self.shaded_box = spyral.Sprite(self.main_group)
        self.shaded_box.image = spyral.Image(size=(0,0))
        self.shaded_box.anchor = 'bottomleft'
        self.shaded_box.position = (box_left, box_bottom)
        self.shaded_box.layer = 'shaded'

        self.vertical_slider = extras.Button((box_left - 80, box_bottom), image_size=(48,24), group=self.buttons)
        self.vertical_slider.dragging = False
        self.vertical_slider.clicked = lambda: self.dragging(self.vertical_slider)
        
        self.horizontal_slider = extras.Button((box_left, box_bottom + 65), image_size=(24,48), group=self.buttons)
        self.horizontal_slider.dragging = False
        self.horizontal_slider.clicked = lambda: self.dragging(self.horizontal_slider)
        
        #Large Fraction on Right Side
        self.auto_fraction = self.generate_fraction_image(extras.Fraction(0,0), ((WIDTH-box_right)/2, HEIGHT/2),  (box_right + (WIDTH-box_right)/2, HEIGHT/2))

        #Exit Button
        exit_button = extras.Button(image_size=(200, 50), position=(WIDTH-5, HEIGHT-5), anchor='bottomright', layer='bottom', fill=(125,125,125), group=self.buttons)
        done_text = extras.Text("Done!", (200, 50), (WIDTH - 105, HEIGHT - 30), layer='top', group=self.main_group)
        exit_button.clicked = lambda: spyral.director.pop()
        exit_button.dragging = False

        self.give_tutorial(operation, fractions)
        
    def update(self, dt):
        #Updating Conversations
        if(self.conversation != 0):
            self.conversation.update_text()
        #Check for any new/relevant events
        for event in self.event_handler.get():
            #Check to see if they clicked a button or slider
            if event['type'] == 'MOUSEBUTTONDOWN':
                self.check_click(event['pos'], self.buttons.sprites())
            elif event['type'] == 'KEYDOWN':
                #ascii 27 is escape key
                if event['ascii'] == chr(27):
                    spyral.director.pop()
                    return
                #ascii 122 is the z key
                if event['ascii'] == chr(122) or event['ascii'] == chr(13):
                    if(self.conversation != 0):
                        if(self.conversation.currentposition < len(self.conversation.ctext)-1):
                            self.conversation.quick_end()
                            return
                        if(self.conversation.currentposition >= len(self.conversation.ctext)-1):
                            self.conversation.to_next()
                            return
            elif event['type'] == 'MOUSEBUTTONUP':
                was_true = False
                for button in self.buttons.sprites():
                    was_true = was_true or button.dragging
                    button.dragging = False
                if was_true:
                    self.calculate_auto_fraction()
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
        self.vertical_lines.draw()
        self.horizontal_lines.draw()
        self.buttons.draw()
        self.auto_fraction.draw(self.camera)
        
    def check_click(self, position, group):
        local_position = self.camera.world_to_local(position)
        for sprite in group:
            if sprite.check_click(local_position):
                #This method needs to be set with a lambda function
                sprite.clicked()

    def check_drag(self, position, slider):
        lines = []
        if (slider == self.horizontal_slider):
            temp_lines = self.vertical_lines.sprites()
            for line in temp_lines:
                lines.append(line.x)
        elif (slider == self.vertical_slider):
            temp_lines = self.horizontal_lines.sprites()
            for line in temp_lines:
                lines.append(line.y)
        lines.sort()
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
            old_height = self.shaded_box.get_rect()._h
            #old_height = self.shaded_box.height
            self.shaded_box.image = spyral.Image(size=(lines[x-1]-self.bl, old_height))
            self.shaded_box.image.fill((135,206,250))
        elif slider == self.vertical_slider and slider.y != lines[x-1]:
            slider.y = lines[x-1]
            old_width = self.shaded_box.get_rect()._w
            self.shaded_box.image = spyral.Image(size=(old_width, BOX_H - (lines[x-1]-self.bt)))
            self.shaded_box.image.fill((135,206,250))

    def dragging(self, slider):
        slider.dragging = True

    def generate_fraction_image(self, fraction, image_size, position, anchor='center', layer='all'):
        group = spyral.Group(self.camera)
        width = image_size[0]
        height = image_size[1]
        numerator =   extras.Text(str(fraction.numerator), (width, 3*height/8), (width/2,0), anchor='midtop', layer=layer, font_size=200)
        middle_line = extras.Button((width/2, height/2), image_size=(width, height/12), anchor='center', layer=layer, fill=(0,0,0));
        denominator = extras.Text(str(fraction.denominator), (width, 3*height/8), (width/2, height), anchor='midbottom', layer=layer, font_size=200)
        agg_sprite = spyral.AggregateSprite(group)
        agg_sprite.image = spyral.Image(size=image_size)
        #agg_sprite.image.fill((255,255,255))
        agg_sprite.pos = position
        agg_sprite.layer = 'bottom'
        agg_sprite.anchor = anchor
        agg_sprite.add_child(numerator)
        agg_sprite.add_child(middle_line)
        agg_sprite.add_child(denominator)
        return agg_sprite

    def calculate_auto_fraction(self):
        mini_box_width = BOX_W/(self.num_of_vertical_lines-1)
        mini_box_height = BOX_H/(self.num_of_horizontal_lines-1)
        num_of_shaded_boxes = (self.shaded_box.height / mini_box_height) * (self.shaded_box.width / mini_box_width)
        num_of_total_boxes = (BOX_W / mini_box_width) * (BOX_H / mini_box_height)
        fraction_to_draw = extras.Fraction(num_of_shaded_boxes, num_of_total_boxes)

        for child in self.auto_fraction.get_children():
            self.auto_fraction.remove_child(child)
        self.auto_fraction = self.generate_fraction_image(fraction_to_draw, self.auto_fraction.image.get_size(), self.auto_fraction.position)

    def give_tutorial(self, operation, fractions):
        problem_description = self.problem_description(operation, fractions)
        

    def problem_description(self, operation, fractions):
        #Description of problem you are solving
        if operation == '+':
            operator = "add"
            preposition = "to"
        elif operation == '-':
            operator = "subtract"
            preposition = "from"
        elif operation == '*':
            operator = "multiply"
            preposition = "with"
        fraction_one = str(fractions[0].numerator) + "/" + str(fractions[0].denominator)
        fraction_two = str(fractions[1].numerator) + "/" + str(fractions[1].denominator)
        problem_description = extras.MultiLineText("You are trying to " + operator + " " + fraction_one + " " + preposition + " " + fraction_two + "\n"
                                                   "Drag the sliders to match the fractions in the equation", (700,150), (10,HEIGHT-10), font_size=30 ,anchor='bottomleft', group=self.main_group)
        
        return problem_description
