import spyral
import village_selection
import extras

WIDTH = 1200
HEIGHT = 900

class CharacterPick(spyral.Scene):
    def __init__(self, *args, **kwargs):

	super(CharacterPick, self).__init__(*args, **kwargs)

	self.camera = self.parent_camera.make_child(virtual_size = (WIDTH, HEIGHT), layers = ['bottom', 'top', 'after'])

	self.buttons = spyral.Group(self.camera)
	self.texts = spyral.Group(self.camera)
	self.after = spyral.Group(self.camera)

	self.name = 'Nice Name'

	self.textbox = extras.TextBox("Name:", (500, 800), self.name, width = 200, height = 50, font_size = 22)
	self.textbox.selecting = 1

	male_button = extras.Button(image_size = (350, 500), position = (WIDTH/4, 325), layer = 'bottom')
	female_button = extras.Button(image_size = (350, 500), position = (3*WIDTH/4, 325), layer = 'bottom')

	male_text = extras.Text("Male", (350, 500), (WIDTH/4, 325), layer = 'top', font_size = 22)
	female_text = extras.Text("Female", (350, 500), (3*WIDTH/4, 325), layer = 'top', font_size = 22)

	male_button.clicked = lambda: spyral.director.push(village_selection.VillageSelection())
	female_button.clicked = lambda: spyral.director.push(village_selection.VillageSelection())

	self.buttons.add(male_button, female_button)
	self.texts.add(male_text, female_text, self.textbox.description, self.textbox.btext)

    def char_chosen(self):
	background = spyral.Image(size=(WIDTH, HEIGHT))
	background.fill((255,255,255))
	self.camera.set_background(background)	
	move_on_button = extras.Button(image_size = (150, 100), position = (1050, HEIGHT/2), layer = 'after')
	move_on_text = extras.Text("Yes >", (150, 100), (1050, HEIGHT/2), layer = 'after', font_size = 22, color = (0,0,0))
	chosen_text = extras.Text("Congratulations {0}!\nYou have been chosen to save the kingdom,\nAre you ready?".format(self.name), (1000, 750), (WIDTH/2, HEIGHT/2), layer = 'after', font_size = 32, color = (0,0,0))
	move_on_button.clicked = lambda: spyral.director.push(village_selection.VillageSelection())
	self.after.add(chosen_text, move_on_text, move_on_button)
	self.after.draw()

    def check_click(self, position, group):
	local_position = self.camera.world_to_local(position)
	for sprite in group:
	    if sprite.check_click(local_position):
		sprite.clicked()

    def on_enter(self):
	background = spyral.Image(filename="images/Title Screen.png")
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
