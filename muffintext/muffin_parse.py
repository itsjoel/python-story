from time import sleep
from muffintext.muffin_types import *
from termcolor import colored


def format_text(text):
    """Formats text given to it
    % makes text red and bold
    * makes text bold
    _ make text underlined
    @ makes text blink
    ` escapes characters (so they don't make the text do anything)
    """
    ftext_str = ""  # init variable for holding formatted text
    text_key = False  # doesn't start key colored
    text_bold = False
    text_under = False
    text_blink = False
    text_escape = False
    for char in text:
        text_attrs = []
        text_color = ''
        if char == '%' and text_escape != True:  # a % makes it either turn red or stop being red
            text_key = not text_key  # by inverting it
        elif char == '*' and text_escape != True:
            text_bold = not text_bold
        elif char == '_' and text_escape != True:
            text_under = not text_under
        elif char == '@' and text_escape != True:
            text_blink = not text_blink
        elif char == '`' and (text_escape != True):
            pass
        else:
            if text_key:
                text_attrs += ['bold']
                text_color = 'red'
                char = char.upper()
            if text_bold:
                text_attrs += ['bold']
            if text_under:
                text_attrs += ["underline"]
            if text_blink:
                text_attrs += ["blink"]
            if text_color:
                ftext_str += colored(char, text_color, attrs=text_attrs)
            else:
                ftext_str += colored(char, attrs=text_attrs)
        if char == '`' or text_escape:
            text_escape = not text_escape
    return ftext_str


def bake(text):
    """This parses the text into blocks of text and functions, then formats the text"""
    raw_list = text.split('|')  # pipes break the text into blocks
    emb_list = []  # not self.parsed_list
    for raw_block in raw_list:  # go though each raw block
        if any(x in raw_block for x in '<>'):  # If there are function tokens in the text,
            if '<' in raw_block:  # <n> means sleep for n seconds
                sleep_time = float(raw_block.strip('<>'))
                # Make it into a parsed function that sleeps for that many seconds
                emb_list += [StoredFunction(sleep, sleep_time)]
        else:  # if these tokens aren't there, it's just text that needs formatting
            # may add in text animations later, but not now
            formatted_text = format_text(raw_block)  # format the text
            # add it to the list
            emb_list += [StoredText(formatted_text, False)]
    return emb_list
