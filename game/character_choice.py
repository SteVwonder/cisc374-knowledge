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
	self.after = spyral.Group(self.camera)

	self.name = 'Hero'

	self.textbox = extras.TextBox("Name:", (500, 800), "Nice name!", width = 200, height = 50, font_size = 22, dcolor=(0,0,0), tcolor=(0,255,0))
	self.textbox.selecting = 1

	male_button = extras.Button(image_size = (350, 400), position = (WIDTH/4, 475), filename = "images/VikingMale.png", layer = 'bottom')
	female_button = extras.Button(image_size = (350, 400), position = (3*WIDTH/4, 475), filename = "images/VikingFemale.png", layer = 'bottom')

	title_text = extras.Text("Who is brave enough to save the village?", (1100, 150), (WIDTH/2, 50), layer = 'top', font_size = 36)
	#male_text = extras.Text("Male", (350, 500), (WIDTH/4, 325), layer = 'top', font_size = 22)
	#female_text = extras.Text("Female", (350, 500), (3*WIDTH/4, 325), layer = 'top', font_size = 22)

	male_button.clicked = lambda: self.char_chosen()
	female_button.clicked = lambda: self.char_chosen()
	#self.textbox.button.clicked = lambda: self.textbox.button.select(self)

	self.buttons.add(male_button, female_button)
	self.texts.add(self.textbox.description, self.textbox.btext, title_text)

    def char_chosen(self):
	for sprite in self.buttons.sprites():
	    sprite.visible = False
	for sprite in self.texts.sprites():
	    sprite.visible = False

	name = self.textbox.get_text()
	if (name):
	    self.name = name

	move_on_text = extras.Text("< Yes >", (150, 100), (975, 650), layer = 'top', font_size = 22, color = (0,0,0))
	chosen_text = extras.MultiLineText(["Congratulations, {0}!".format(self.name), "You have been chosen to save the kingdom", "Are you ready?"], (850, 400), (WIDTH/2, 450), anchor='center', layer = 'top', font_size = 34)

	move_on_button = extras.Button(image_size = (900, 500), position = (WIDTH/2, HEIGHT/2), anchor = 'center', layer = 'bottom')
	move_on_button.clicked = lambda: spyral.director.push(village_selection.VillageSelection())

	self.texts.add(chosen_text, move_on_text)
	self.buttons.add(move_on_button)
	self.render()

    def check_click(self, position, group):
	local_position = self.camera.world_to_local(position)
	for sprite in group:
	    if sprite.check_click(local_position):
		sprite.clicked()
	
    def on_enter(self):
	background = spyral.Image(size=(WIDTH,HEIGHT))
	background.fill((255,255,255))
	self.camera.set_background(background)

    def render(self):
	self.buttons.draw()
	self.texts.draw()

    def update(self, dt):
	for event in self.event_handler.get():
	    if event['type'] == 'QUIT':
		spyral.director.pop()
		return
	    elif event['type'] == 'KEYDOWN':
		character = event['ascii']
		self.ntext = self.textbox.get_text()+character
		self.textbox.set_text(self.ntext)
                #ascii 27 is escape key
                if event['ascii'] == chr(27):
                    spyral.director.pop()
                    return
		if event['ascii'] == chr(13):
		    return self.textbox.get_answer()
		if event['ascii'] == chr(8):
                    txt = self.textbox.get_text() 
		    txt = txt[:len(txt)-2]
		    self.textbox.set_text(txt)
	    elif event['type'] == 'MOUSEBUTTONDOWN':
		self.check_click(event['pos'], self.buttons.sprites())
