from .muffin_parse import get_muffin_block_list
class MuffinSequence(object):
    __muffin_blocks__ = []

    def __init__(self, blocks):
        self.__muffin_blocks__ = blocks

    def __call__(self):
        for __block__ in self.__muffin_blocks__:
            __block__()

    @classmethod
    def bake(cls, text):
        """This parses the text into blocks of text and functions, then formats the text"""
        __muffin_blocks__ = get_muffin_block_list(text)
        __baked_muffin__ = cls(__muffin_blocks__)
        return __baked_muffin__
