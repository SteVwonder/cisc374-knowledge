import spyral
import village_selection
import extras

WIDTH = 1200
HEIGHT = 900

class CharacterPick(spyral.Scene):
    def __init__(self, *args, **kwargs):

	super(CharacterPick, self).__init__(*args, **kwargs)

	self.camera = self.parent_camera.make_child(virtual_size = (WIDTH, HEIGHT), layers = ['bottom', 'top'])

	self.buttons = spyral.Group(self.camera)
	self.texts = spyral.Group(self.camera)
	self.textbox = spyral.Group(self.camera)

	self.name = 'Hero'

	name_input = extras.TextBox("Name:", (WIDTH/2, 750), True, width = 200, height = 50, anchor = 'center')

	self.name = name_input.get_answer

	male_button = extras.Button(image_size = (350, 500), position = (WIDTH/4, 325), layer = 'bottom')
	female_button = extras.Button(image_size = (350, 500), position = (3*WIDTH/4, 325), layer = 'bottom')

	male_text = extras.Text("Male", (350, 500), (WIDTH/4, 325), layer = 'top', font_size = 22)
	female_text = extras.Text("Female", (350, 500), (3*WIDTH/4, 325), layer = 'top', font_size = 22)

	male_button.clicked = lambda: spyral.director.push(village_selection.VillageSelection())
	female_button.clicked = lambda: spyral.director.push(village_selection.VillageSelection())

	self.textbox.add(name_input)
	self.buttons.add(male_button, female_button)
	self.texts.add(male_text, female_text)

    def check_click(self, position, group):
	local_position = self.camera.world_to_local(position)
	for sprite in group:
	    if sprite.check_click(local_position):
		sprite.clicked()

    def on_enter(self):
	background = spyral.Image(size=(WIDTH, HEIGHT))
	background.fill((0,0,0))
	self.camera.set_background(background)

    def render(self):
	self.buttons.draw()
	self.texts.draw()
	#self.textbox.draw()	error size for image = none

    def update(self, dt):
	for event in self.event_handler.get():
	    if event['type'] == 'QUIT':
		spyral.director.pop()
		return
	    elif event['type'] == 'MOUSEBUTTONDOWN':
		self.check_click(event['pos'], self.buttons.sprites())
