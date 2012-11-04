import spyral

WIDTH = 1200
HEIGHT = 900

# The Fraction Mini-Game
# The farmer pulls a lever to dispense water into a bucket
# You need to solve a word problem to figure out how much
# water you need in the bucket
# If you run into problems, it sends you to the Fraction Tools
# scene, where you can visulaize the fractional problem using
# the widgets in the scene

# The Fraction Mini-Game
# The farmer pulls a lever to dispense water into a bucket
# You need to solve a word problem to figure out how much
# water you need in the bucket
# If you run into problems, it sends you to the Fraction Tools
# scene, where you can visulaize the fractional problem using
# the widgets in the scene

class FractionGame(spyral.Scene):
    def __init__(self, *args, **kwargs):

        super(FractionGame, self).__init__(*args, **kwargs)

        self.camera = self.parent_camera.make_child(virtual_size = (WIDTH, HEIGHT))
        self.buttons = spyral.Group(self.camera)
        self.texts = spyral.Group(self.camera)

    def update(self, dt):

        for event in self.event_handler.get():
            if event['type'] == 'QUIT':
                spyral.director.pop()
                return
            elif event['type'] == 'MOUSEBUTTONDOWN':
                self.check_click(event['pos'], self.buttons.sprites())

    #Converts the position of the click from real to virtual
    #Then checks to see if any of the sprites in the button
    #group have been clicked, if so, call their clicked method
    def check_click(self, position, group):
        local_position = self.camera.world_to_local(position)
        for sprite in group:
            if sprite.check_click(local_position):
                #This method needs to be set with a lambda function
                sprite.clicked()

    #Sets the background to an image file store in the repo
    def on_enter(self):

        background = spyral.Image(filename="images/farmland.jpg")
        self.camera.set_background(background)
