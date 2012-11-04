import spyral

WIDTH = 1200
HEIGHT = 900

# The fraction tools
# Several widgets that help the kids visualize fractional operations

class FractionTools(spyral.Scene):
    def __init__(self, *args, **kwargs):

        super(FractionTools, self).__init__(*args, **kwargs)

        self.camera = self.parent_camera.make_child(virtual_size = (WIDTH, HEIGHT))

    def update(self, dt):
        
        #Check for any new/relevant events
        for event in self.event_handler.get():
            #They clicked the OS exit button at the top of the frame
            if event['type'] == 'QUIT':
                spyral.director.pop()
                return

    def on_enter(self):
        
        background = spyral.Image(size=(WIDTH, HEIGHT))
        background.fill((194,194,194))
        self.camera.set_background(background)
