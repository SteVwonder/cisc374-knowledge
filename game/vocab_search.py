import spyral
import extras
import random
import wordsearch_generator

WIDTH = 1200
HEIGHT = 900

class VocabScene(spyral.Scene):
    def __init__(self, *args, **kwargs):
	super(VocabScene, self).__init__(*args, **kwargs)

	self.camera = self.parent_camera.make_child(virtual_size = (WIDTH, HEIGHT), layers = ['background', 'playing'])
	#self.wordsearch = spyral.Group(self.camera)
	self.texts = spyral.Group(self.camera)

	self.words, self.definitions = wordsearch_generator.getvocab('vocablist.txt')
	self.difficulty = "medium"
	self.grid = wordsearch_generator.make_grid(self.difficulty, self.words, 100, 9, 9)
	#self.choice_grid = self.format_grid_data('choices')

	if self.grid == None:
	    spyral.director.pop()

	wordsearch_text = []
	for row in xrange(self.grid.height):
	    wordsearch_text = extras.Text('          '.join(self.grid.data[row*self.grid.width : (row+1) * self.grid.width]), (800, (600/self.grid.height)), (WIDTH/2, 30 + (row*(600/self.grid.height))), layer='background', font_size = 24, color = (255, 255, 255))
	    self.texts.add(wordsearch_text)

	definitions_text = []
	text = []
	remaining_width = 1140		    #30 on either side for border
	row = 0
	for definition in xrange(len(self.definitions)):
	    definition_string = ' {0}. {1} '.format(definition+1, self.definitions[definition])
	    projected_width = remaining_width - 10*len(definition_string)
	    if projected_width >= 1:
		text.append(definition_string) 
		remaining_width = projected_width
	    else:
		definitions_text = extras.Text('    '.join(text), (1140, 65), (30, 600+(row*80)), anchor = 'topleft', layer='background', font_size = 18, color = (255, 255, 255))
		self.texts.add(definitions_text)
		del text[:]
		text.append(definition_string)
		if definition == len(self.definitions)-1: # Last definition
		    definitions_text = extras.Text(text, (1140, 50), (30, 600+((row+1)*55)), anchor = 'topleft', layer='background', color = (255, 255, 255))
		else:
		    remaining_width = 1140 - len(definition_string)
		    row += 1

	self.texts.add(definitions_text)

    
    def update(self, dt):

	for event in self.event_handler.get():
	    if event['type'] == 'QUIT':
		spyral.director.pop()
		return
	    elif event['type'] == 'MOUSEBUTTONDOWN':
		self.check_click(event['pos'])

    def render(self):
	self.texts.draw()
	#self.wordsearch.draw()

    def check_click(self, position):
	local_position = self.camera.world_to_local(position)
	#dotdotdot

    def on_enter(self):
	background = spyral.Image(size = (WIDTH, HEIGHT))
	background.fill((0,0,0))
	self.camera.set_background(background)

'''    def format_grid_data(self, grid_to_format):
	
	data = []
	if grid_to_format == 'choices':
	    data = self.grid.choices
	else:
	    data = self.grid.data

	f_grid = []
	for row in xrange(self.grid.height):
	    f_grid.append('  '.join(data[row * self.grid.width : (row + 1) * self.grid.width]))

	return '\n'.join(f_grid)

    def format_clues(self):
	shuffle_list = self.definitions
	random.shuffle(shuffle_list)
	cluetext = list(enumerate(shuffle_list))
	clues = []
	for definition in cluetext:
	    clues.append('{0}. {1}'.format(definition[0], definition[1]))

	del cluetext[:]
	for row in xrange(len(clues)/4):
	    cluetext.append('    '.join(clues[row*4:(row*4)+1]))

	return '\n'.join(cluetext)
'''
