import spyral
import fraction_game
import vocab_search
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
        self.main_group = spyral.Group(self.camera)
        self.fraction_group = spyral.Group(self.camera)
        self.fraction_difficulty = 1

        #Add in our button for the fraction game, notice how I set the layer
        fraction_game_button = extras.Button(image_size=(200, 50), position=(WIDTH/2, HEIGHT/2), layer='bottom')
<<<<<<< HEAD
	vocab_search_button = extras.Button(image_size=(200, 50), position=(WIDTH/2, HEIGHT/2 + 75), layer='bottom')        
=======
>>>>>>> 1f773ca9ef495be940c8996a88201e0a1e61393c

        #Need to assign an action to the button for when it is clicked
        #We do this by using lambda functions.  So when the button is
        #clicked, the method clicked is called, which points to this
        #lambda function.  As you can see, I'm using this button to push
        #a new scene onto the stack
<<<<<<< HEAD
        fraction_game_button.clicked = lambda: spyral.director.push(fraction_game.FractionGame(1))
	vocab_search_button.clicked = lambda: spyral.director.push(vocab_search.VocabScene())
        
        #Add text over the button, notice how I set the layer
        fraction_game_text = extras.Text("Fraction Game", (200, 50), (WIDTH/2, HEIGHT/2), layer='top')
	vocab_search_text = extras.Text("Vocabulary Search", (200, 50), (WIDTH/2, HEIGHT/2 + 75), layer='top')

        #Using two different groups for text and buttons
        #That way we only have to check for clicks on the buttons
        self.buttons.add(fraction_game_button, vocab_search_button)
        self.texts.add(fraction_game_text, vocab_search_text)

=======
        fraction_game_button.clicked = lambda: spyral.director.push(fraction_game.FractionGame(self.fraction_difficulty))
        
        #Add text over the button, notice how I set the layer
        fraction_game_text = extras.Text("Fraction Game", (200, 50), (WIDTH/2, HEIGHT/2), layer='top')
        self.fraction_difficulty_text = spyral.Sprite()
        #Using two different groups for text and buttons
        #That way we only have to check for clicks on the buttons
        self.fraction_group.add(fraction_game_text, fraction_game_button)
        self.buttons.add(fraction_game_button)
>>>>>>> 1f773ca9ef495be940c8996a88201e0a1e61393c
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
        self.fraction_difficulty_text.visible = False
        self.fraction_difficulty_text.draw(self.camera)
        if self.fraction_difficulty > 4:
            for sprite in self.fraction_group.sprites():
                self.buttons.remove(sprite)
            self.fraction_group.empty()
            self.fraction_difficulty_text = extras.Text("You completed every level of the fraction game!", (400, 100), (WIDTH/2, HEIGHT/6), anchor="midtop", font_size=30, color=(255,255,255), group=self.main_group)
        else:
            self.fraction_difficulty_text = extras.Text("You are currently on level " + str(self.fraction_difficulty) + " of the fraction game", (400, 100), (WIDTH/2, HEIGHT/6), anchor="midtop", font_size=30, color=(255,255,255), group=self.main_group)
        self.fraction_difficulty_text.visible = True
        background = spyral.Image(size=(WIDTH, HEIGHT))
        background.fill((0,0,0))
        self.camera.set_background(background)

    def render(self):
        self.main_group.draw()
        self.fraction_group.draw()

    #Check for someone trying to quit
    #Also check for mouse clicks, if you detect one, check if
    #the user clicked a button
    def update(self, dt):

        for event in self.event_handler.get():
            if event['type'] == 'QUIT':
                spyral.director.pop()
                return
            elif event['type'] == 'MOUSEBUTTONDOWN':
                self.check_click(event['pos'], self.buttons.sprites())
