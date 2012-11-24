import spyral
import fraction_game
import vocab_search
import extras
import MeanMedianMode

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
        self.main_group = spyral.Group(self.camera)
        self.fraction_difficulty = 1

        #Add in our button for the fraction game, notice how I set the layer
        fraction_game_button = extras.Button(image_size=(200, 50), position=(522, 725), layer='bottom')
        play_MMM = extras.Button(image_size=(200, 50), position=(304, 320), layer = 'bottom')
	vocab_search_button = extras.Button(image_size=(200, 50), position=(629, 320), layer='bottom')        

        #Need to assign an action to the button for when it is clicked
        #We do this by using lambda functions.  So when the button is
        #clicked, the method clicked is called, which points to this
        #lambda function.  As you can see, I'm using this button to push
        #a new scene onto the stack
        fraction_game_button.clicked = lambda: spyral.director.push(fraction_game.FractionGame(1))
        play_MMM.clicked = lambda: spyral.director.push(MeanMedianMode.MeanMedianMode())
	vocab_search_button.clicked = lambda: spyral.director.push(vocab_search.VocabScene())
        
        #Add text over the button, notice how I set the layer
        self.fraction_game_text = extras.Text("Fraction Game - Level 1", (200, 50), (522, 725), layer='top')
        play_MMMtext = extras.Text("Mean Median Mode", (200, 50), (304, 320), layer = 'top')
	vocab_search_text = extras.Text("Vocabulary Search", (200, 50), (629, 320), layer='top')

        #Using two different groups for text and buttons
        #That way we only have to check for clicks on the buttons
        self.buttons.add(fraction_game_button, vocab_search_button,play_MMM)

        fraction_game_button.clicked = lambda: spyral.director.push(fraction_game.FractionGame(self.fraction_difficulty))
        
        #Using two different groups for text and buttons
        #That way we only have to check for clicks on the buttons
        
        self.buttons.add(fraction_game_button, vocab_search_button, play_MMM)
        self.texts.add(self.fraction_game_text, vocab_search_text, play_MMMtext)
    #Converts the position of the click from real to virtual
    #Then checks to see if any of the sprites in the button
    #group have been clicked, if so, call their clicked method
    def check_click(self, position, group):
        local_position = self.camera.world_to_local(position)
        for sprite in group:
            if sprite.check_click(local_position):
                #This method needs to be set with a lambda function
                sprite.clicked()
                
    #Set the background of the scene
    def on_enter(self):
        if self.fraction_difficulty > 4:
            self.fraction_game_text.image = extras.Text("Fraction Game - Done!", (200, 50), (WIDTH/2, HEIGHT/6), anchor="midtop", color=(0,0,0), group=self.texts).image
        else:
            self.fraction_game_text.image = extras.Text("Fraction Game - Level " + str(self.fraction_difficulty), (200, 50), (WIDTH/2, HEIGHT/6), anchor="midtop", color=(0,0,0), group=self.texts).image
        self.fraction_game_text._expire_static()
        background = spyral.Image(filename="images/BG.png")
        self.camera.set_background(background)

    def render(self):
        self.main_group.draw()
        self.buttons.draw()
        self.texts.draw()

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
                print event['pos']
