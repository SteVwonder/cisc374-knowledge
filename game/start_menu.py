import spyral
import extras
import village_selection
import character_choice
#import vocab_input
import high_score

WIDTH = 1200
HEIGHT = 900

# The basic Start Menu
# Standard interface for the intro of a game
# Can choose to enter the game, check high scores
# (potentially) enter vocabulary, and quit the game
# Choosing play pushes the gender and name entry scene
# onto the director's stack

class StartMenu(spyral.Scene):
    def __init__(self, *args, **kwargs):
        super(StartMenu, self).__init__(*args, **kwargs)
        
	#Making layers for the buttons and their text separately to display one over the other
	self.camera = self.parent_camera.make_child(virtual_size = (WIDTH, HEIGHT), layers = ['bottom', 'top'])
	self.buttons = spyral.Group(self.camera)
	self.texts = spyral.Group(self.camera)


	#The play, vocab input, high score, and quit buttons to be used, layer = 'bottom'
	play_button = extras.Button(image_size=(200, 50), position=(WIDTH/2, HEIGHT/2), layer = 'bottom',filename="images/Buttons/Start Game 1.png")
	quit_button = extras.Button(image_size=(200, 50), position=(WIDTH/2, HEIGHT/2 + 75), layer = 'bottom',filename="images/Buttons/Quit 1.png")

	#Assigning the actions to be taken when each of the buttons are clicked
	#using lambda functions.
	#All but the quit pushes a new scene onto the stack
	play_button.clicked = lambda: spyral.director.push(character_choice.CharacterPick())
        #vocab_input_button.clicked = lambda: self.toggle_menu()
        #high_score_button.clicked = lambda: spyral.director.push(high_score.EndScene())
        quit_button.clicked = lambda: spyral.director.pop()

        #Adding the text over the buttons, layer = 'top'
        #play_text = extras.Text("Play", (200, 50), (WIDTH/2, HEIGHT/2 - 75), layer = 'top')
        #vocab_input_text = extras.Text("Input Vocab", (200, 50), (WIDTH/2, HEIGHT/2), layer = 'top')
        #high_score_text = extras.Text("High Scores", (200, 50), (WIDTH/2, HEIGHT/2 + 75), layer = 'top')
        #quit_text = extras.Text("Quit", (200, 50), (WIDTH/2, HEIGHT/2 + 150), layer = 'top')

        #Adding the buttons and text to their respective groups
        self.buttons.add(play_button, quit_button)
        #self.texts.add(play_text, vocab_input_text, high_score_text, quit_text)

    def toggle_menu(self):
	pass	

    #Converts the position of the click from real to virtual
    #Then checks to see if any of the sprites in the button group have been clicked
    #calling their 'clicked' method if they have
    def check_click(self, position, group):
        local_position = self.camera.world_to_local(position)
        for sprite in group:
            if sprite.check_click(local_position):
                sprite.clicked()
                
    #Sets the background, currently a blank fill
    def on_enter(self):
        background = spyral.Image(filename="images/Title Screen.png")
        self.camera.set_background(background)

    #Draws the sprites, currently just the buttons and text
    def render(self):
        self.buttons.draw()
        self.texts.draw()
        
    #Checks for mouse clicks and if it was a button click
    def update(self, dt):
        for event in self.event_handler.get():
            if event['type'] == 'MOUSEBUTTONDOWN':
                self.check_click(event['pos'], self.buttons.sprites())
            elif event['type'] == 'KEYDOWN':
                #ascii 27 is escape key
                if event['ascii'] == chr(27):
                    spyral.director.pop()
                    return
            elif event['type'] == 'QUIT':
                spyral.director.pop()
