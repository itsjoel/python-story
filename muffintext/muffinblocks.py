class MuffinBlockFunction(object):
    function = False
    arguments = ()

    def __init__(self, function, arguments=None):  # Take the functions and the arguments
        self.function = function
        if arguments != None:
            self.arguments = arguments

    def __call__(self):  # Run then when it is time
        if self.arguments:
            return self.function(self.arguments)
        else:
            return self.function()


class MuffinBlockText(object):  # Holds parsed text
    text = ""
    text_animation = False

    def __init__(self, text, animation=False):
        self.text = text
        self.text_animation = animation

    def __call__(self):  # Display the text
        print(self.text)