import spyral
import town_square
import extras

WIDTH = 1200
HEIGHT = 900

# The Village Selection Scene
# Used to choose what mini-game you want to play
# When you click on a village, it sends you to the village square
# From there you are sent to the mini-game
# Clicking on one of the villages pushes the village square onto the
# director's stack

class VillageSelection(spyral.Scene):
    def __init__(self, *args, **kwargs):
        
        super(VillageSelection, self).__init__(*args, **kwargs)

        #Notice how I'm using non-default layers, this is needed to display text over the buttons
        self.camera = self.parent_camera.make_child(virtual_size = (WIDTH, HEIGHT), layers= ['bottom', 'top', 'all'])
        #Do not draw this layer, just used to group together clickable buttons
        self.buttons = spyral.Group(self.camera)
        self.texts = spyral.Group(self.camera)
        self.stars = spyral.Group(self.camera)
        
        self.main_group = spyral.Group(self.camera)
        
        self.fraction_difficulty = 1
        self.MMM_difficulty = 1
        self.Vocab_difficulty = 1

        self.fstars = []
        self.mstars = []
        self.vstars = []

        self.setupstars()

        #Add in our button for the fraction game, notice how I set the layer
        fraction_game_button = extras.Button(image_size=(200, 50), position=(522, 725), layer='bottom',filename="images/Buttons/Fraction Game 1.png")
        play_MMM_button = extras.Button(image_size=(200, 50), position=(304, 320), layer = 'bottom',filename="images/Buttons/Mean Median Mode 1.png")
	vocab_search_button = extras.Button(image_size=(200, 50), position=(629, 320), layer='bottom',filename="images/Buttons/Vocab Search 1.png")

        #Need to assign an action to the button for when it is clicked
        #We do this by using lambda functions.  So when the button is
        #clicked, the method clicked is called, which points to this
        #lambda function.  As you can see, I'm using this button to push
        #a new scene onto the stack
        fraction_game_button.clicked = lambda: spyral.director.push(town_square.TownSquare('fraction'))
        play_MMM_button.clicked = lambda: spyral.director.push(town_square.TownSquare('MMM'))
	vocab_search_button.clicked = lambda: spyral.director.push(town_square.TownSquare('vocabsearch'))
         
        #Using two different groups for text and buttons
        #That way we only have to check for clicks on the buttons
        
        self.buttons.add(fraction_game_button, vocab_search_button, play_MMM_button)

    #Converts the position of the click from real to virtual
    #Then checks to see if any of the sprites in the button
    #group have been clicked, if so, call their clicked method
    def check_click(self, position, group):
        local_position = self.camera.world_to_local(position)
        for sprite in group:
            if sprite.check_click(local_position):
                #This method needs to be set with a lambda function
                sprite.clicked()

    def setupstars(self):
        #Add stars under Buttons
        for x in range(self.fraction_difficulty):
            self.fstars.append(extras.Button(filename="images/Star.png",layer='bottom',position=(430+(90*x),775)))
            self.stars.add(self.fstars[x])
        for x in range(0,self.MMM_difficulty):
            self.mstars.append(extras.Button(filename="images/Star.png",layer='bottom',position=(212+(90*x),370)))
            self.stars.add(self.mstars[x])
        for x in range(0,self.Vocab_difficulty):
            self.vstars.append(extras.Button(filename="images/Star.png",layer='bottom',position=(537+(90*x),370)))
            self.stars.add(self.vstars[x])

    def purgestars(self):
        self.fstars = []
        self.mstars = []
        self.vstars = []
        self.stars.empty()
        
    #Set the background of the scene
    def on_enter(self):
        #self.fraction_game_text._expire_static()
        background = spyral.Image(filename="images/BG.png")
        self.camera.set_background(background)
        self.purgestars()
        self.setupstars()

    def render(self):
        self.main_group.draw()
        self.buttons.draw() 
        self.stars.draw()

    #Check for someone trying to quit
    #Also check for mouse clicks, if you detect one, check if
    #the user clicked a button
    def update(self, dt):
        for event in self.event_handler.get():
            if event['type'] == 'QUIT':
                spyral.director.pop()
                return
            elif event['type'] == 'KEYDOWN':
                #ascii 27 is escape key
                if event['ascii'] == chr(27):
                    spyral.director.pop()
                    return
            elif event['type'] == 'MOUSEBUTTONDOWN':
                self.check_click(event['pos'], self.buttons.sprites())
