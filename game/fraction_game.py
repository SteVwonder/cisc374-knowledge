import spyral

HEIGHT = 1200
WIDTH = 900

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
