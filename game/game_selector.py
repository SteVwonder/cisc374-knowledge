import spyral

WIDTH = 1200
HEIGHT = 900

class Text(spyral.Sprite):
    def __intit__(self, position, text):

        super(Text, self).__init__()
        self.image = spyral.Image(size=(200, 50))
        self.image = spyral.Font("fonts/bertoltbrecht.ttf", 14, (0,0,0)).render(text)
        self.pos = position


class GameSelector(spyral.Scene):
    def __init__(self, *args, **kwargs):
        super(GameSelector, self).__init__(*args, **kwargs)

        self.camera = self.parent_camera.make_child(virtual_size = (WIDTH, HEIGHT))
        self.group = spyral.Group(self.camera)

        button_image = spyral.Image(size=(100,50))
        button_image.fill((255,255,255))

        self.fraction_game_button = spyral.Sprite()
        self.fraction_game_button.image = button_image
        self.fraction_game_button.anchor = 'center'
        self.fraction_game_button.pos = (WIDTH/2, HEIGHT/2)
        
        self.group.add(self.fraction_game_button)

    def on_enter(self):
        background = spyral.Image(size=(WIDTH, HEIGHT))
        background.fill((0,0,0))
        self.camera.set_background(background)
        
    def render(self):
        self.group.draw()
