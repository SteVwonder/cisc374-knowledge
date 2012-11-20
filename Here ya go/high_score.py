import spyral
import start_menu
import extras

WIDTH = 1200
HEIGHT = 900

class EndScene(spyral.Scene):
    def __init__(self, *args, **kwargs):
	super(EndScene, self).__init__(*args, **kwargs)

	self.camera = self.parent_camera.make_child(virtual_size = (WIDTH, HEIGHT), layers = ['bottom', 'top'])
	self.texts = spyral.Group(self.camera)
	self.buttons = spyral.Group(self.camera)
	self.filename = '/highscores.txt'

	end_button = extras.Button(image_size = (60, 60), position = (1140, 840), layer = 'bottom')
	end_text = extras.Text("End", (60, 60), (1140, 840), layer = 'top')
	end_button.clicked = lambda: spyral.director.push(start_menu.StartMenu())

	title_text = extras.Text("High Scores", (90, 1000), (WIDTH/2, 125), layer = 'top', font_size = 36, color = (255, 255, 255))

	self.scores_list = self.get_scores('highscores.txt')
	self.scores_list.reverse()
	scorelist_text = []
	count = 0
	for score in self.scores_list:
	    new_string = '{0}. {1}'.format(count+1, score[1])
	    scorelist_text = extras.Text(new_string, (300, 50), (50, 300+(count*75)), anchor = 'topleft', layer = 'top', color = (255, 255, 255))
	    self.texts.add(scorelist_text)
	    count += 1

	self.buttons.add(end_button)
	self.texts.add(end_text, title_text)

    def check_click(self, position, group):
	local_position = self.camera.world_to_local(position)
	for sprite in group:
	    if sprite.check_click(local_position):
		sprite.clicked()

    def on_enter(self):
	background = spyral.Image(size = (WIDTH, HEIGHT))
	background.fill((0,0,0))
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
                #ascii 27 is escape key
                if event['ascii'] == chr(27):
                    spyral.director.pop()
                    return
	    elif event['type'] == 'MOUSEBUTTONDOWN':
		self.check_click(event['pos'], self.buttons.sprites())

    def get_scores(self, filename):
	scoreslist = []
	fd = open(filename, 'r')
	try:
	    
	    for line in fd.readlines():
		if "'" in line:
		    continue
		line = line.strip().upper()
		if ":" in line:
		    score, name = line.split(':', 1)
		    scoreslist.append([int(score), name + ' : ' + score])
		
	finally:
	    fd.close()

	return sorted(scoreslist, key=lambda x: x[0])

    def write_scores(self):
	fd = open(self.filename, 'w')
	for score in self.scores_list:
	    fd.write(':'.join(score) + '\n')
	fd.close()


	
