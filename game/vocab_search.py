import spyral
import extras
import random
import wordsearch_generator

WIDTH = 1200
HEIGHT = 900

class VocabScene(spyral.Scene):
    def __init__(self, difficulty,gender='Hero',name='Hero'):
	super(VocabScene, self).__init__()

	self.camera = self.parent_camera.make_child(virtual_size = (WIDTH, HEIGHT), layers = ['bottom', 'middle', 'top', 'all'])
	self.texts = spyral.Group(self.camera)
	self.buttons = spyral.Group(self.camera)
	self.highlights = spyral.Group(self.camera)
    

	self.gender = gender
	self.name = name

	self.words, self.definitions = wordsearch_generator.getvocab('vocablist.txt')
	self.difficulty = "hard"
	self.grid = wordsearch_generator.make_grid(self.difficulty, self.words, 100)
	if self.grid == None:
	    spyral.director.pop()

	self.wordsearch_text = extras.MultiLineText(self.grid.data, (600, 600), (WIDTH/2 + 20, 500), anchor='center', columns = self.grid.width, layer="top", font_size=24, color=(255,255,255))
	#definitions_text = extras.MultiLineText(self.definitions, (1050, 250), (75, 680), spacing = 0, columns = 2, order="leftright", layer="top", font_size = 18, color=(255,255,255))

	#self.goodjob = extras.Text("Good Job! You've solved the puzzle.", (800, 300), (WIDTH/2, HEIGHT/2), anchor = 'center', layer = 'top', font_size = 48, color = (255, 255, 255))
	#self.goodjob.visible = False
	self.words.reverse()
	self.words.append("WORD BANK:")
	self.words.reverse()
	wordbank = extras.MultiLineText(self.words, (300, 800), (50, 50), spacing = 0, columns = 1, layer = 'top', font_size = 18)
	self.answercount = 0

	self.last_clicked = 0
	self.current_choices = []
	self.cellsize = 600/self.grid.width
	self.build_choices()
	
	self.texts.add(self.wordsearch_text, wordbank)


    def build_choices(self):

	for row in xrange(self.grid.height):
	    for column in xrange(self.grid.width):

		new_button = extras.Button(image_size=(self.cellsize, self.cellsize), position=(320+(self.cellsize/4)+column*self.cellsize, 200+(self.cellsize/4)+row*self.cellsize), anchor = 'center', layer='middle', fill=(0,0,255))
		new_button.visible = False
		new_button.clicked = lambda: self.button_clicked()
		self.buttons.add(new_button)
		self.grid.buttons.append(new_button)

    def button_clicked(self):
	sprite = self.last_clicked
	if self.highlights.has(sprite):
	    return
	if sprite == 0:
	    return
	sprite.visible = not sprite.visible
	#sprite.draw(self.camera)
	if sprite.visible == False:
	    self.current_choices.remove(self.grid.buttons.index(sprite))
	    print "Removed sprite at index: {0} from choices".format(self.grid.buttons.index(sprite))
	elif len(self.current_choices) < 2:
	    self.current_choices.append(self.grid.buttons.index(sprite))
	    print "Added sprite at index: {0} to choices".format(self.grid.buttons.index(sprite))
	else:
	    old_choice = self.current_choices.pop(0)
	    self.grid.buttons[old_choice].visible = False
	    #self.grid.buttons[old_choice].draw(self.camera)
	    self.current_choices.append(self.grid.buttons.index(sprite))
	    print "Replaced sprite at {0} with sprite at {1}".format(old_choice, self.grid.buttons.index(sprite))

    def enter_answer(self):
	print "enter key received"
	self.current_choices.sort()	
	for coord in self.grid.words:
	    if self.current_choices == coord[1]:
		print "correct answer"
		#horizontal word
		if (self.current_choices[0]/self.grid.width) == (self.current_choices[1]/self.grid.width):
		    increment = 1		    
		else:
		    choices = [(self.current_choices[0]%self.grid.width), (self.current_choices[1]%self.grid.width)]
		    #diag to right
		    if choices[0] < choices[1]:
			increment = self.grid.width+1
		    #diag to left
		    elif choices[0] > choices[1]:
			increment = self.grid.width-1
		    #vertical
		    else:
			increment = self.grid.width		

		self.grid.buttons[self.current_choices[0]].visible = False
		self.grid.buttons[self.current_choices[1]].visible = False
		for box in xrange(self.current_choices[0], self.current_choices[1]+1, increment):
		    sprit = self.grid.buttons[box]
		    highlight = extras.Button(sprit.position, (self.cellsize, self.cellsize), anchor='center', layer='bottom', fill=(0,255,255))
		    self.highlights.add(highlight)
		
		self.last_clicked = 0
		self.answercount += 1
		return
	    if self.answercount == len(self.words)-1:
		background = spyral.Image(size=(WIDTH, HEIGHT))
		background.fill((0,0,0))
		self.camera.set_background(background)
		#self.goodjob.visible = True
		#self.goodjob.draw(self.camera)
		spyral.director.pop()
		spyral.director.pop()
		return	
 

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
		#ascii 13 is enter key
		if event['ascii'] == chr(13):
		    self.enter_answer()
		    return
	    elif event['type'] == 'MOUSEBUTTONDOWN':
		self.check_click(event['pos'], self.buttons.sprites())

    def render(self):
	self.buttons.draw()
	self.highlights.draw()
	self.texts.draw()

    def check_click(self, position, group):
	local_position = self.camera.world_to_local(position)
	for sprite in group:
	    if sprite.check_click(local_position):
		self.last_clicked = sprite
		sprite.clicked()

    def on_enter(self):
	background = spyral.Image(filename='images/door.png')
	#background = spyral.Image(size = (WIDTH, HEIGHT))
	#background.fill((0,0,0))
	self.camera.set_background(background)
