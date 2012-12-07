import pdb
import spyral
import extras
import fraction_game
import MeanMedianMode
import conversation
import vocab_search

WIDTH = 1200
HEIGHT = 900

FRACTION_TEXT = [" ", " ", " "]
MMM_TEXT = [" ", " ", " ",]
VOCABSEARCH_TEXT = [" ", " ", " "]

class TownSquare(spyral.Scene):
    def __init__(self, town):

	super(TownSquare, self).__init__()

	self.camera = self.parent_camera.make_child(virtual_size = (WIDTH, HEIGHT), layers = ['bottom', 'top', 'all'])
	self.buttons = spyral.Group(self.camera)
	self.texts = spyral.Group(self.camera)

	self.town = town
	self.popularity = 0
	#self.crowd = spyral.Image()
	self.fraction_difficulty = 1
	self.MMM_difficulty = 1
	self.search_difficulty = 'easy'

	self.greetings = {'fraction': FRACTION_TEXT, 'MMM': MMM_TEXT, 'vocabsearch': VOCABSEARCH_TEXT}
	#self.greeting = conversation.Conversation(self.greetings[town], (0, HEIGHT), self, WIDTH, HEIGHT, tcolor=(0, 255, 0))

	ready_button = extras.Button((WIDTH/2, HEIGHT/2), (200, 200), layer = 'bottom')
	#ready_button.visible = False
	ready_button_text = extras.Text("< Yes >", (200, 200), (WIDTH/2, HEIGHT/2), layer = 'top', font_size = 26)
	#ready_button_text.visible = False
	if town == 'fraction': 
	    ready_button.clicked = lambda: spyral.director.push(fraction_game.FractionGame(self.fraction_difficulty))
	elif town == 'MMM':
	    ready_button.clicked = lambda: spyral.director.push(MeanMedianMode.MeanMedianMode(self.MMM_difficulty))
	elif town == 'vocabsearch':
	    ready_button.clicked = lambda: spyral.director.push(vocab_search.VocabScene(self.search_difficulty))

	self.buttons.add(ready_button)#self.greeting.button, ready_button)
	self.texts.add(ready_button_text)#self.greeting.next, self.greeting.visibletext, ready_button_text)
	
    def check_click(self, position, group):
	local_position = self.camera.world_to_local(position)
	for sprite in group:
	    if sprite.check_click(local_position):
		sprite.clicked()

    def on_enter(self):
	background = spyral.Image(filename="images/oldtownsquare.png")
	self.camera.set_background(background)

    def render(self):
	self.buttons.draw()
	self.texts.draw()

    def update(self, dt):
	#Update conversation
	#if (self.greeting):
	    #self.greeting.update_text()
	for event in self.event_handler.get():
	    #Clicked on OS exit button
	    if event['type'] == 'QUIT':
		spyral.director.pop()
		return
	    #Clicked somewhere
	    elif event['type'] == 'KEYDOWN':
		#ascii 27 is escape key
		if event['ascii'] == chr(27):
		    spyral.director.pop()
		    return
		#ascii 13 is enter key - move conversation along
		#if event['ascii'] == chr(13):
		    #if (self.conversation.currentposition < len(self.conversation.ctext)-1):
		    	#self.conversation.quick_end()
			#return
		    #if (self.conversation.currentposition >= len(self.conversation.ctext)-1):
			#self.conversation.to_next()
			#return
	    elif event['type'] == 'MOUSEBUTTONDOWN':
		self.check_click(event['pos'], self.buttons.sprites())
