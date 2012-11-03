import spyral

HEIGHT = 1200
WIDTH = 900

class FractionGame(spyral.Scene):
    def __init__(self, *args, **kwargs):

        super(FractionGame, self).__init__(*args, **kwargs)

        self.camera = self.parent_camera.make_child(virtual_size = (WIDTH, HEIGHT))
        self.buttons = spyral.Group(self.camera)
        self.texts = spyral.Group(self.camera)
