import pdb
import spyral
import extras
import fraction_game
import MeanMedianMode
import conversation
import vocab_search
import random

WIDTH = 1200
HEIGHT = 900

class TownSquare(spyral.Scene):
    def __init__(self, town,fd=1,md=1,vd=1,gender='Hero',name="Hero"):

	super(TownSquare, self).__init__()

	self.camera = self.parent_camera.make_child(virtual_size = (WIDTH, HEIGHT), layers = ['bottom', 'top', 'all'])
	self.buttons = spyral.Group(self.camera)
	self.texts = spyral.Group(self.camera)
	self.move_on = spyral.Group(self.camera)

	self.gender = gender
	self.name = name

	FRACTION_TEXT = []
        FRACTION_TEXT.append([["Fraction Townsperson", "Fraction Townsperson", "Fraction Townsperson","Fraction Townsperson"], ["Welcome "+self.name+" you have come at the right time!", "It seems the Wizard has stopped the rain from falling!", "We've always needed the rain to water our crops.","Will you help us?"]])
        FRACTION_TEXT.append([["Fraction Townsperson", "Fraction Townsperson", "Fraction Townsperson"], ["Hooray for "+self.name+"!", "The drought continues but I think we're starting to get it.", "Can we rely on you again?"]])
        FRACTION_TEXT.append([["Fraction Townsperson", "Fraction Townsperson", "Fraction Townsperson"], ["We love you "+self.name+"!", "The drought continues and we're having a tough time this week.", "Will you help us?"]])
        
        MMM_TEXT = []
        MMM_TEXT.append([["Mean Townsperson", "Median Townsperson", "Mode Townsperson"], ["The wizard has turned everyone into boxes", "What are we going to do?!?", "Will you help us "+self.name+"!?"]])
        MMM_TEXT.append([["Mean Townsperson", "Median Townsperson", "Mode Townsperson"], ["The wizard came back and turned more people into boxes","He got more people than before!", "Please help us?"]])
        MMM_TEXT.append([["Mean Townsperson", "Median Townsperson", "Mode Townsperson"], ["The wizard has turned everyone into boxes", "He's got a lot of people this time!", "Will you help us "+self.name+"!?"]])

        VOCABSEARCH_TEXT = []
        VOCABSEARCH_TEXT.append([["Vocab Townsperson", "Vocab Townsperson", "Vocab Townsperson"], ["Oh my the town hall door has been enchanted by the wizard", "What were all those words?", "Please help us!?"]])
        VOCABSEARCH_TEXT.append([["Vocab Townsperson", "Vocab Townsperson", self.name,"Vocab Townsperson"], ["The townshall got locked again!", "How bored does a wizard have to be to bother us like this...", "I... don't know?","Will you help us?"]])
        VOCABSEARCH_TEXT.append([["Vocab Townsperson", "Vocab Townsperson", self.name,"Vocab Townsperson"], ["...", "We should just find another town hall", "He'll probably lock that one too.","Will you help us?"]])

	self.town = town
	self.popularity = 0
	#self.crowd = spyral.Image()
	self.fraction_difficulty = fd
	self.MMM_difficulty = md
	self.search_difficulty = vd
	
        if(town == 'fraction'):
            self.dif = self.fraction_difficulty
        elif(town == 'MMM'):
            self.dif = self.MMM_difficulty
        elif(town == "vocabsearch"):
            self.dif = self.search_difficulty
            
        self.VLIST = []
	for x in range(0,4*self.dif):
            fle = "images/Character Boy.png"
            self.VLIST.append(extras.Button(position=(120+random.randrange(0,800,110), 300+random.randrange(0,300,110)), layer='bottom',filename=fle))
            self.texts.add(self.VLIST[x])

	self.greetings = {'fraction': FRACTION_TEXT[self.fraction_difficulty-1], 'MMM': MMM_TEXT[self.MMM_difficulty-1], 'vocabsearch': VOCABSEARCH_TEXT[self.search_difficulty-1]}
	self.greeting = conversation.Conversation(self.greetings[town], (0, HEIGHT), self, WIDTH, HEIGHT, tcolor=(0, 255, 0))
	#self.greeting.button.draw(self.camera)
	self.texts.add(self.greeting.button)

	self.ready_button = extras.Button((WIDTH/2, HEIGHT/2), (200, 200), layer = 'top')
	self.ready_button.visible = False
	self.ready_button_text = extras.Text("< Yes >", (200, 200), (WIDTH/2, HEIGHT/2), layer = 'toptop', font_size = 26)
	self.ready_button_text.visible = False
	if town == 'fraction': 
	    self.ready_button.clicked = lambda: spyral.director.push(fraction_game.FractionGame(self.fraction_difficulty,gender=self.gender,name=self.name))
	elif town == 'MMM':
	    self.ready_button.clicked = lambda: spyral.director.push(MeanMedianMode.MeanMedianMode(self.MMM_difficulty,gender=self.gender,name=self.name))
	elif town == 'vocabsearch':
	    self.ready_button.clicked = lambda: spyral.director.push(vocab_search.VocabScene(self.search_difficulty,gender=self.gender,name=self.name))

	self.buttons.add(self.ready_button)
	self.texts.add(self.ready_button_text, self.greeting.next, self.greeting.visibletext, self.greeting.nametext)
	
    def check_click(self, position, group):
	local_position = self.camera.world_to_local(position)
	for sprite in group:
	    if sprite.check_click(local_position):
		sprite.clicked()

    def on_enter(self):
	background = spyral.Image(filename="images/townsquare.png")
	self.camera.set_background(background)

    def render(self):
	self.buttons.draw()
	self.texts.draw()

    def update(self, dt):
	#Update conversation
	if self.greeting != -1:
	    self.greeting.update_text()
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
		if event['ascii'] == chr(122) or event['ascii'] == chr(13):
		    if (self.greeting):
			if(self.greeting.currentposition < len(self.greeting.ctext)-1):
			    self.greeting.quick_end()
			    return
		    if (self.greeting.currentposition >= len(self.greeting.ctext)-1):
			moveflag = self.greeting.to_next()
			if moveflag == -1:
                            if self.town == 'fraction':
                                spyral.director.push(fraction_game.FractionGame(self.fraction_difficulty,gender=self.gender,name=self.name))
                            elif self.town == 'MMM':
                                spyral.director.push(MeanMedianMode.MeanMedianMode(self.MMM_difficulty,gender=self.gender,name=self.name))
                            elif self.town == 'vocabsearch':
                                spyral.director.push(vocab_search.VocabScene(self.search_difficulty,gender=self.gender,name=self.name))
                        self.town = self.town
			return
	    elif event['type'] == 'MOUSEBUTTONDOWN':
		self.check_click(event['pos'], self.buttons.sprites())
