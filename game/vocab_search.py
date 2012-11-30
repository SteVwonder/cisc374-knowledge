import spyral
import extras
import random
import wordsearch_generator

WIDTH = 1200
HEIGHT = 900

class VocabScene(spyral.Scene):
    def __init__(self, *args, **kwargs):
	super(VocabScene, self).__init__(*args, **kwargs)

	self.camera = self.parent_camera.make_child(virtual_size = (WIDTH, HEIGHT), layers = ['bottom', 'top', 'all'])
	self.texts = spyral.Group(self.camera)
	self.button = spyral.Group(self.camera)

	self.words, self.definitions = wordsearch_generator.getvocab('vocablist.txt')
	self.difficulty = "hard"
	self.grid = wordsearch_generator.make_grid(self.difficulty, self.words, 100)
	if self.grid == None:
	    spyral.director.pop()

	wordsearch_text = extras.MultiLineText(self.grid.data, (600, 600), (WIDTH/2, 370), anchor='center', columns = self.grid.width, layer="top", font_size=24, color=(255,255,255))
	definitions_text = extras.MultiLineText(self.definitions, (1050, 250), (75, 680), spacing = 0, columns = 2, order="leftright", layer="top", font_size = 18, color=(255,255,255))
	#definitions_text.image.draw_rect((255,255,255), (75, 630), (1050, 250), border_width = 10, anchor="topleft")
	#ws_img = spyral.Image(filename="images/scroll.png").scale((700, 700))
	#ws_img.draw_image(wordsearch_text, (350, 350), anchor = 'center')

	self.texts.add(wordsearch_text, definitions_text)   
 
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
		self.check_click(event['pos'])

    def render(self):
	self.texts.draw()

    def check_click(self, position):
	local_position = self.camera.world_to_local(position)
	#dotdotdot

    def on_enter(self):
	background = spyral.Image(size = (WIDTH, HEIGHT))
	background.fill((0,0,0))
	self.camera.set_background(background)
