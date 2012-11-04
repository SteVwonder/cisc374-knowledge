import spyral
import extras
import fraction_tools
from fractions import Fraction

WIDTH = 1200
HEIGHT = 900

# The Fraction Mini-Game
# The farmer pulls a lever to dispense water into a bucket
# You need to solve a word problem to figure out how much
# water you need in the bucket
# If you run into problems, it sends you to the Fraction Tools
# scene, where you can visulaize the fractional problem using
# the widgets in the scene

class FractionGame(spyral.Scene):
    def __init__(self, *args, **kwargs):

        super(FractionGame, self).__init__(*args, **kwargs)

        self.camera = self.parent_camera.make_child(virtual_size = (WIDTH, HEIGHT), layers=['bottom', 'top'])
        self.buttons = spyral.Group(self.camera)
        self.texts = spyral.Group(self.camera)

        #Some variables used in the game
        self.water_in_bucket = 0
        
        #Button to move to the fractional tools scene
        fraction_tools_button = extras.Button((200, 50), (WIDTH-5, 5), anchor='topright', layer='bottom')
        increase_water_button = extras.Button((150,150), (5, HEIGHT-5), anchor='bottomleft', layer='bottom')
        
        #Need to assign an action to the button for when it is clicked
        fraction_tools_button.clicked = lambda: spyral.director.push(fraction_tools.FractionTools())
        increase_water_button.clicked = lambda: self.increase_water_in_bucket()
        
        #Add text over the button, notice how I set the layer
        fraction_tools_text = extras.Text("Fraction Tools", (200, 50), (WIDTH-105, 30), layer='top')
        self.increase_water_text = extras.Text("Add Water (0)", (150,150), (75, HEIGHT-75), layer='top')
        
        #Using two different groups for text and buttons
        #That way we only have to check for clicks on the buttons
        self.buttons.add(fraction_tools_button, increase_water_button)
        self.texts.add(fraction_tools_text, self.increase_water_text)

    def increase_water_in_bucket(self):
        self.water_in_bucket += 1
        self.increase_water_text.set_text("Add Water (" + str(self.water_in_bucket) + ")")

    def update(self, dt):
        #Check for any new/relevant events
        for event in self.event_handler.get():
            #They clicked the OS exit button at the top of the frame
            if event['type'] == 'QUIT':
                spyral.director.pop()
                return
            #They clicked somewhere
            elif event['type'] == 'MOUSEBUTTONDOWN':
                self.check_click(event['pos'], self.buttons.sprites())

    def render(self):
        self.buttons.draw()
        self.texts.draw()
        
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

        background = spyral.Image(filename="images/farmland.jpg")
        self.camera.set_background(background)
