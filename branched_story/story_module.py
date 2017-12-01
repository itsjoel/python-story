from __future__ import print_function

from builtins import input, object
from time import sleep

from termcolor import colored, cprint

from emb_text.embellish_parse import *

def my_input():
    return input(colored('> ', attrs=["blink"]))

class Point(object):  # Base for both story points and decision points
    parsed_list = []
    next_point = False

    def __init__(self, text):  # When initializing
        # When initializing, take the raw text, and parse it
        self.parsed_list = self.__parse__(text)

    def __format__(self, text):  # Private method for formatting text.
        return format_text(text)  # Return the output of the function

    def __parse__(self, text):
        """This parses the text into blocks of text and functions, then formats the text"""
        return embellish_text(text)

    def __show__(self):
        """Displays the content of this point"""
        for parsed_block in self.parsed_list:  # go through each parsed block
            parsed_block()  # Excecute them, either by printing or by calling

    def __go__(self):
        """Returns the point to go to next"""
        if self.next_point != False:
            return self.next_point
        else:
            return False


class Decision(Point):
    """For decision points
    Usage: decision(text, options)
    text = text to be formatted
    options = dictionary of options
    that the player has and the resulting
    point to go to for each option

    """
    options = {}

    def __init__(self, text, options):
        Point.__init__(self, text)
        self.options = options

    def do_point(self):
        """Show the text
        Get the next point
        Go to it"""
        self.__show__()  # show the content
        # the next point we're going to is the one associated with the option that matches
        self.next_point = self.options[self.__prompt__()]
        return self.__go__()  # then go to it

    def __prompt__(self):
        """Ask the player their choice"""
        success = False
        while not success:  # Keep going until you get an answer
            user_input = my_input().upper().strip() # removes whitespace
            for choice in self.options:
                if user_input == choice[0:len(user_input)].upper():
                    """if the letters in the input match the
                    beginning letters of any of the choices
                    ex. EXPL matches EXPLODE"""
                    return choice
            success = False  # Didn't get answer, remind player of choices
            self.__remind__()

    def __remind__(self):
        """Reminds the player of their choices"""
        print('Your choices are:')
        for option in self.options:
            cprint(option.upper(), 'red', attrs=['bold'])


class Story(Point):
    """For story points
    Usage: name = story(text, next_point)
    if next_point = False, the story ends there"""

    def __init__(self, text, next_point=False):
        Point.__init__(self, text)
        self.next_point = next_point

    def do_point(self):
        """Show the text of the point
        Then go to the next one"""
        self.__show__()
        return self.__go__()


class Book(object):
    """
    In order to hold an entire story
    it must be saved in a book
    usage: name = book(name, [authors], start_point, {points})
    start_point (optional)= the first point in the book
    !IMPORTANT!--NEED TO SET A START POINT BEFORE TELLING STORY
    points (optional) = a dictionary containing every point in this format:
    name: story(text, next_point),
    name: decision(text, {options}),
    this can be addded to or subtracted from later using methods:
    add_story(name, text, next_point)
    add_decision(name, text, options)
    remove_point(name)
    Can be viewed individually using this method:
    test_point(name)
    """
    title = ""
    authors = []
    points = {}
    start_point = False

    def __init__(self, title, authors=None, start_point=None, points=None):
        self.title = title  # title of book
        self.authors = authors  # authors of book
        self.points = points or {}  # dictionary of points
        self.start_point = start_point  # point to start from

    def tell(self):
        """
        Run story
        !IMPORANT - Set start_point before running
        """
        self.__title__()  # display title
        sleep(3)  # wait
        try:
            # try to do the first point
            next_point = self.points[self.start_point].do_point()
        except:  # if it fails, there's probably not a start_point set
            print("Did you forget to give the book a start point?")
            raise
        while next_point != False:  # while there is a next_point
            # do it, and get that point's next point
            next_point = self.points[next_point].do_point()
        self.__end__()  # once it's finished, show the end graphic

    def __end__(self):  # end graphic
        print(colored("====END====", "white", attrs=["bold"]))

    def add_story(self, name, text, next_point):  # add story point
        self.points[name] = Story(text, next_point)

    def add_decision(self, name, text, options):  # add decision point
        self.points[name] = Decision(text, options)

    def set_start_point(self, name):  # set the point to start from
        self.start_point = name

    def __author_text__(self):  # generate the "By Jon Doe and Don Joe" text
        author_text = ''
        if type(self.authors) == list:  # if it's a list
            if len(self.authors) <= 2:  # and there's less than or equal to two in them
                # join the items together with the word 'and'
                author_text = ' and '.join(self.authors)
            else:  # otherwise
                first_author = self.authors[0]  # first author
                mid_authors = self.authors[1:len(
                    self.authors) - 1]  # middle authors
                last_author = self.authors[len(
                    self.authors) - 1]  # last author
                author_text = first_author  # start with the first author
                for mid_author in mid_authors:
                    # add commas between all the mid_authors
                    author_text = author_text + ', ' + mid_author
                author_text = author_text + ', and ' + \
                    last_author  # use an and for the last author
        else:
            author_text = self.authors  # if it's not a list, it's just one author
        author_text += '.'  # oh, and add a period at the end
        return author_text  # return

    def __title__(self):  # display title graphic
        print(colored('===', 'white', attrs=['bold']) + colored(self.title.upper(), 'red', attrs=[
              'bold']) + colored('===', 'white', attrs=['bold']))  # white ===, red title, white ===
        print('by', self.__author_text__())  # get author text

    def remove_point(self, name):  # remove a point
        self.points.pop(name)

    def test_point(self, name):  # just run one point
        return self.points[name].do_point()
