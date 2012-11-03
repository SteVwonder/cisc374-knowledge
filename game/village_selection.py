import spyral
import fraction_game
import extras

WIDTH = 1200
HEIGHT = 900

class VillageSelection(spyral.Scene):
    def __init__(self, *args, **kwargs):
        
        super(VillageSelection, self).__init__(*args, **kwargs)

        self.camera = self.parent_camera.make_child(virtual_size = (WIDTH, HEIGHT), layers= ['bottom', 'top'])
        self.buttons = spyral.Group(self.camera)
        self.texts = spyral.Group(self.camera)
        
        fraction_game_button = extras.Button((200, 50), (WIDTH/2, HEIGHT/2), layer='bottom')
        fraction_game_button.clicked = lambda: spyral.director.push(fraction_game.FractionGame())
        fraction_game_text = extras.Text("Fraction Game", (200, 50), (WIDTH/2, HEIGHT/2), layer='top')
        
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
