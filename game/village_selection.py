import spyral
import fraction_game

WIDTH = 1200
HEIGHT = 900
FONT_PATH = "fonts/bertoltbrecht.ttf"

class Button(spyral.Sprite):
    def __init__(self, position):

        super(Button, self).__init__()
        self.image = spyral.Image(size=(200, 50))
        self.image.fill((255,255,255))
        self.layer = 'bottom'
        self.anchor = 'center'
        self.pos = position

    def clicked(self):
        spyral.director.push(fraction_game.FractionGame())
        
    def check_click(self, position):
        return self.get_rect().collide_point(position)
    
class Text(spyral.Sprite):
    def __init__(self, position, text):

        super(Text, self).__init__()
        self.image = spyral.Image(size=(200, 50))
        self.image = spyral.Font(FONT_PATH, 14, (0,0,255)).render(text)
        self.layer = 'top'
        self.anchor = 'center'
        self.pos = position

class VillageSelection(spyral.Scene):
    def __init__(self, *args, **kwargs):
        
        super(VillageSelection, self).__init__(*args, **kwargs)

        self.camera = self.parent_camera.make_child(virtual_size = (WIDTH, HEIGHT), layers= ['bottom', 'top'])
        self.buttons = spyral.Group(self.camera)
        self.texts = spyral.Group(self.camera)
        
        fraction_game_button = Button((WIDTH/2, HEIGHT/2))
        fraction_game_text = Text(position=(WIDTH/2, HEIGHT/2), text="Fraction Game")
        
        self.buttons.add(fraction_game_button)
        self.texts.add(fraction_game_text)

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
        
    def update(self, dt):

        for event in self.event_handler.get():
            if event['type'] == 'QUIT':
                spyral.director.pop()
                return
            elif event['type'] == 'MOUSEBUTTONDOWN':
                self.check_click(event['pos'], self.buttons.sprites())
