import spyral
import extras
import fraction_tools
import random
import time

WIDTH = 1200
HEIGHT = 900
FRACTION_SIZE = (50,150)
RESULTS_TIME_ON_SCREEN = 2
NUMBER_TO_COMPLETE = 3

# The Fraction Mini-Game
# The farmer pulls a lever to dispense water into a bucket
# You need to solve a word problem to figure out how much
# water you need in the bucket
# If you run into problems, it sends you to the Fraction Tools
# scene, where you can visulaize the fractional problem using
# the widgets in the scene

class FractionGame(spyral.Scene):
    def __init__(self, difficulty):
        super(FractionGame, self).__init__()

        self.camera = self.parent_camera.make_child(virtual_size = (WIDTH, HEIGHT), layers=['bottom', 'top', 'toptop'])
        self.buttons = spyral.Group(self.camera)
        self.texts = spyral.Group(self.camera)
        self.others = spyral.Group(self.camera)
        
        #Some variables used in the game
        self.water_in_bucket = extras.Fraction(0,0)
        self.increment_bucket_by = 0
        #self.difficulty = 4
        self.difficulty = difficulty
        self.problem_fractions = None
        self.results_timer = RESULTS_TIME_ON_SCREEN
        self.operation = None
        self.completed = 0
        #Button to move to the fractional tools scene
        fraction_tools_button = extras.Button(image_size=(200, 50), position=(WIDTH-5, 5), anchor='topright', layer='bottom', fill=(194, 194, 194))
        increase_water_button = extras.Button(filename="images/red_button_300x300.png", position=(5, HEIGHT-5), anchor='bottomleft', layer='bottom')
        done_button = extras.Button(image_size=(200, 50), position=(WIDTH - 5, HEIGHT - 5), anchor='bottomright', layer='bottom', fill=(194, 194, 194))
        self.results_button = extras.Button(image_size=(600,250), position=(WIDTH/2, HEIGHT/2), layer='top', fill=(255,255,255), group=self.others)
        self.results_button.visible = False
        
        #Need to assign an action to the button for when it is clicked
        fraction_tools_button.clicked = lambda: spyral.director.push(fraction_tools.FractionTools(self.difficulty, self.problem_fractions, self.operation))
        increase_water_button.clicked = lambda: self.increase_water_in_bucket()
        done_button.clicked = lambda: self.check_answer()
        
        #Add text over the button, notice how I set the layer
        fraction_tools_text = extras.Text("Fraction Tools", (200, 50), (WIDTH-105, 30), layer='top')
        self.increase_water_text = extras.Text("Add Water (0)", (150,150), (150, HEIGHT-150), layer='top', font_size=30)
        done_text = extras.Text("Done!", (200, 50), (WIDTH - 105, HEIGHT - 30), layer='top')
        self.great_job_text = extras.Text("Great Job!", (600, 450), (WIDTH/2, HEIGHT/2), layer='toptop', font_size=110)
        self.great_job_text.visible = False
        self.try_again_text = extras.Text("Try Again", (600, 450), (WIDTH/2, HEIGHT/2), layer='toptop', font_size=110)
        self.try_again_text.visible = False
        self.operation_text = extras.Text(self.operation, (50, 50), (WIDTH/2, HEIGHT/2), layer='bottom', font_size=70)

        if self.difficulty < 3:
            fraction_tools_button.visible = False
            fraction_tools_text.visible = False
        else:
            fraction_tools_button.visible = True
            fraction_tools_text.visible = True
        
        #Using two different groups for text and buttons
        #That way we only have to check for clicks on the buttons
        #Only put clickables in here
        self.buttons.add(fraction_tools_button, increase_water_button, done_button)
        self.texts.add(fraction_tools_text, self.increase_water_text, done_text, self.great_job_text, self.try_again_text, self.operation_text)

        self.fractions_tuple = self.generate_problem()
        
    def increase_water_in_bucket(self):
        self.water_in_bucket = self.water_in_bucket + self.increment_bucket_by
        self.increase_water_text.set_text("Add Water (" + str(self.water_in_bucket) + ")")

    def update(self, dt):
        #Check for any new/relevant events
        for event in self.event_handler.get():
            #They clicked the OS exit button at the top of the frame
            if event['type'] == 'QUIT':
                spyral.director.pop()
    	    elif event['type'] == 'KEYDOWN':
                #ascii 27 is escape key
                if event['ascii'] == chr(27):
                    spyral.director.pop()
                    return
            #They clicked somewhere
            elif event['type'] == 'MOUSEBUTTONDOWN':
                self.check_click(event['pos'], self.buttons.sprites())

        if self.great_job_text.visible or self.try_again_text.visible:
            self.results_timer -= dt
            if self.results_timer <= 0:
                if self.completed >= NUMBER_TO_COMPLETE:
                    village_selection_scene = spyral.director._stack[-2]
                    village_selection_scene.fraction_difficulty = self.difficulty + 1
                    spyral.director.pop()
                else:
                    self.great_job_text.visible = False
                    self.try_again_text.visible = False
                    self.results_button.visible = False
                    self.results_timer = RESULTS_TIME_ON_SCREEN

    def render(self):
        self.buttons.draw()
        self.texts.draw()
        self.others.draw()
        for fraction in self.fractions_tuple:
            fraction.draw(self.camera)
        
    #Converts the position of the click from real to virtual
    #Then checks to see if any of the sprites in the button
    #group have been clicked, if so, call their clicked method
    def check_click(self, position, group):
        local_position = self.camera.world_to_local(position)
        for sprite in group:
            if sprite.check_click(local_position):
                #This method needs to be set with a lambda function
                sprite.clicked()

    #Sets the background to an image file store in the repo
    def on_enter(self):
        background = spyral.Image(filename="images/farmland-short.jpg")
        self.camera.set_background(background)

    def generate_fraction_image(self, fraction, image_size, position, anchor='center', layer='all'):
        group = spyral.Group(self.camera)
        width = image_size[0]
        height = image_size[1]
        numerator =   extras.Text(str(fraction.numerator), (width, 3*height/8), (width/2,0), anchor='midtop', layer=layer, font_size=70)
        middle_line = extras.Button((width/2, height/2), image_size=(width, height/12), anchor='center', layer=layer, fill=(0,0,0));
        denominator = extras.Text(str(fraction.denominator), (width, 3*height/8), (width/2, height), anchor='midbottom', layer=layer, font_size=70)
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

    def generate_same_denominator_fractions(self, min, max):
        denominator = random.randint(min+1,max)
        numerator1 = random.randint(min,denominator-1)
        numerator2 = random.randint(min,denominator-1)
        return extras.Fraction(numerator1, denominator), extras.Fraction(numerator2, denominator)

    def generate_different_denominator_fractions(self, min, max):
        denominator1 = random.randint(min+1,max)
        denominator2 = random.randint(min+1,max)        
        numerator1 = random.randint(min,denominator1-1)
        numerator2 = random.randint(min,denominator2-1)
        while denominator1 == denominator2:
            denominator1 = random.randint(min+1,max)
            denominator2 = random.randint(min+1,max)        
            numerator1 = random.randint(min,denominator1-1)
            numerator2 = random.randint(min,denominator2-1)
            
        return extras.Fraction(numerator1, denominator1), extras.Fraction(numerator2, denominator2)

    def generate_simple_same_denominator_problem(self, min, max):
        self.problem_fractions = self.generate_same_denominator_fractions(min, max)
        operation = random.randint(0,1)
        if(operation):
            self.operation = "+"
            self.answer = self.problem_fractions[0] + self.problem_fractions[1]
        else:
            self.operation = "-"
            self.answer = self.problem_fractions[0] - self.problem_fractions[1]
            while(self.answer.numerator < 1):
                self.problem_fractions = self.generate_same_denominator_fractions(min, max)
                self.answer = self.problem_fractions[0] - self.problem_fractions[1]
        self.operation_text.set_text(self.operation)
        a = self.generate_fraction_image(self.problem_fractions[0], FRACTION_SIZE, (WIDTH/3, HEIGHT/2), layer='bottom')
        b = self.generate_fraction_image(self.problem_fractions[1], FRACTION_SIZE, (2*WIDTH/3, HEIGHT/2), layer='bottom')
        self.increment_bucket_by = extras.Fraction(1, self.problem_fractions[0].denominator)
        self.water_in_bucket = extras.Fraction(0, self.increment_bucket_by.denominator)
        return a, b

    def generate_simple_different_denominator_problem(self, min, max):
        self.problem_fractions = self.generate_different_denominator_fractions(min, max)
        operation = random.randint(0,1)
        if(operation):
            self.operation = "+"
            self.answer = self.problem_fractions[0] + self.problem_fractions[1]
        else:
            self.operation = "-"
            self.answer = self.problem_fractions[0] - self.problem_fractions[1]
            while(self.answer.numerator < 1):
                self.problem_fractions = self.generate_different_denominator_fractions(min, max)
                self.answer = self.problem_fractions[0] - self.problem_fractions[1]
        self.operation_text.set_text(self.operation)
        a = self.generate_fraction_image(self.problem_fractions[0], FRACTION_SIZE, (WIDTH/3, HEIGHT/2), layer='bottom')
        b = self.generate_fraction_image(self.problem_fractions[1], FRACTION_SIZE, (2*WIDTH/3, HEIGHT/2), layer='bottom')

        def lcm(a, b):
            def gcd(a, b):
                while b:
                    b, a = a%b, b
                return a
            return ( a * b ) / gcd(a, b)

        self.increment_bucket_by = extras.Fraction(1, lcm(self.problem_fractions[0].denominator, self.problem_fractions[1].denominator))
        self.water_in_bucket = extras.Fraction(0, self.increment_bucket_by.denominator)
        return a, b

    def generate_multiply_same_denominator_problem(self, min, max):
        self.problem_fractions = self.generate_same_denominator_fractions(min, max)
        self.operation = "*"
        self.answer = self.problem_fractions[0] * self.problem_fractions[1]
        self.operation_text.set_text(self.operation)
        a = self.generate_fraction_image(self.problem_fractions[0], FRACTION_SIZE, (WIDTH/3, HEIGHT/2), layer='bottom')
        b = self.generate_fraction_image(self.problem_fractions[1], FRACTION_SIZE, (2*WIDTH/3, HEIGHT/2), layer='bottom')
        common_denominator = self.problem_fractions[0].denominator * self.problem_fractions[1].denominator
        self.increment_bucket_by = extras.Fraction(1, common_denominator)
        self.water_in_bucket = extras.Fraction(0, self.increment_bucket_by.denominator)
        return a, b

    def generate_multiply_different_denominator_problem(self, min, max):
        self.problem_fractions = self.generate_different_denominator_fractions(min, max)
        self.operation = "*"
        self.answer = self.problem_fractions[0] * self.problem_fractions[1]
        self.operation_text.set_text(self.operation)
        a = self.generate_fraction_image(self.problem_fractions[0], FRACTION_SIZE, (WIDTH/3, HEIGHT/2), layer='bottom')
        b = self.generate_fraction_image(self.problem_fractions[1], FRACTION_SIZE, (2*WIDTH/3, HEIGHT/2), layer='bottom')
        common_denominator = self.problem_fractions[0].denominator * self.problem_fractions[1].denominator
        self.increment_bucket_by = extras.Fraction(1, common_denominator)
        self.water_in_bucket = extras.Fraction(0, self.increment_bucket_by.denominator)
        return a, b

    def generate_problem(self):
        if self.difficulty == 1:
            return self.generate_simple_same_denominator_problem(1, 6)
        elif self.difficulty == 2:
            return self.generate_simple_different_denominator_problem(1, 6)
        elif self.difficulty == 3:
            return self.generate_multiply_same_denominator_problem(1, 6)
        elif self.difficulty == 4:
            return self.generate_multiply_different_denominator_problem(1, 5)
        else:
            raise ValueError("Unrecognized Difficulty Level")

    def check_answer(self):
        print self.answer, self.water_in_bucket
        self.results_timer = RESULTS_TIME_ON_SCREEN
        if self.water_in_bucket == self.answer:
            self.try_again_text.visible = False
            self.great_job_text.visible = True
            self.results_button.visible = True
            self.completed += 1
            if self.completed != NUMBER_TO_COMPLETE:
                for fraction in self.fractions_tuple:
                    #fraction.visible = False
                    for sprite in fraction.get_children():
                        fraction.remove_child(sprite)
                    #fraction.draw(self.camera)
                self.fractions_tuple = self.generate_problem()
                self.increase_water_text.set_text("Add Water (" + str(self.water_in_bucket) + ")")
        else:
            self.great_job_text.visible = False
            self.try_again_text.visible = True
            self.results_button.visible = True
            self.water_in_bucket = extras.Fraction(0, self.water_in_bucket.denominator)
            self.increase_water_text.set_text("Add Water (" + str(self.water_in_bucket) + ")")
            #show hint
