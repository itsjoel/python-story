"""This module contains everything you need for making a simple branching story.
"""
from __future__ import print_function

from builtins import input, object
from time import sleep

from termcolor import colored, cprint

import muffintext 


def get_user_input(prompt='> ', blink=True):
    """Prompts user for input. 
    
    Used mainly because it makes testing easier.
    
    Parameters
    ----------
    prompt : str, optional
        The text that appears next to the prompt. Defaults to >
    blink : bool, optional
        Whether the text blinks or not. Defaults to True
    
    Returns
    -------
    string
        The user's response
    """
    return input(colored('> ', attrs=["blink"])) #Makes > graphic


class Point(object):
    __parsed_list__ = []
    next_point = None

    def __init__(self, text=None, next_point=None):
        """Generic point/node in the interactive story.
        
        On initialization, formats inputted text using muffintext.bake().
        When called, displays the resulting muffintext, then returns next_point.
        
        Parameters
        ----------
        text : string, optional
            The text content of this point in the story.
        next_point : string, optional
            The next point in the narrative. Defaults to None.
        """
        if text != None:
        self.__parsed_list__ = self.__parse__(text) #Parse the raw text into muffinPtext
        else:
            self.__parsed_list__ = False
        self.next_point = next_point

    def __parse__(self, text):
        """Alias for muffintext.bake(text).
        
        Usage
        -----
        Muffintext can contain both "Formatted Text", meaning text with colors and styles, and "Parsed Functions", functions embedded in the muffintext. The boundry between these two kinds of content is denoted using the pipe (|) Control Token. The tokens are described below.
        
        Control
        -------
        |: New block.
        
        Functions
        ---------
        <x>: time.sleep(x)
        
        Formatting
        ----------
        % : Makes text red and bold. Used for choice keywords.
        * : Makes text bold.
        _ : Makes text italic.
        @ : Makes text blink.
        ` : Escapes formatting tokens, but not function tokens (yet).
        
        Parameters
        ----------
        text : string
            Raw, unformatted, unparsed text
        
        Returns
        -------
        list
            Muffintext-formatted list containing functions and formatted text.
        """
        return muffintext.bake(text)

    def __call__(self):
        """Executes the point
        
        Displays the content of the post, then returns next point. If it returns False, then this is an end point.
        
        Returns
        -------
        string
            The next point in the story. A False denotes an ending point.
        """
        self.__show__()
        return self.__go__()

    def __show__(self):
        """Displays post content
        
        Displays the content of the post by iterating through the list and executing each block.
        """
        if self.__parsed_list__:
            for parsed_block in self.__parsed_list__:  # go through each parsed block
                parsed_block()  # Excecute them, either by printing or by calling
        else:
            pass

    def __go__(self):
        """Returns the next point
        
        Returns the next point as determined by whatever the next_point variable has been sent to. If it's false, then this is an end point for the story.
        
        Returns
        -------
        string
            Whatever the `next point` variable is currently set to. Should be the name of the next point in the story. 
        """
        return self.next_point


class Decisionpt(Point):
    options = {}

    def __init__(self, text, options):
        """For decisions in the story.
        
        For parts in the story where the path forks, and the reader can directly decide which path to follow. This point will display the content of the post and then continuously ask the player for text input until it can be understood by fuzzy matching. The fuzzy matching tests whether the string that the player types in, once stripped of leading or following whitespace, case-insensitively matches any of the decision keywords, when each keyword is truncated to the length of the user input.
        
        Usage
        -----
        The `text` content of the post should be short and directly or indirectly ask the player to decide between a number of choices, which all should be mentioned. Choices are chosen by the player by typing in the choice's **keyword**. Each keyword should be in the `text` of the post using "choice" formatting, which is done using the `%` tag, and in ALL CAPS.
        
        Parameters
        ----------
        text : string
            The text content of the point. Will be formatted using muffintext.bake(). Should be short and contain the keywords for the player to type in ALL CAPS using muffintext's "choice" formatting, which makes the text red and bold and uses the `%` tag.
        options : dict
            A dictionary containing the options that the player has in this format: {"choice_keyword" : "name_of_point_to_go_to_if_this_point_is_chosen",...} 
        
        Example
        -------
        ```
        ...
        "decisionfruit": Decisionpt("Do you eat the %APPLE%, or the %PEAR%?", {"APPLE": "choseapple", "PEAR": "chosepear"}),
        ...
        """
        Point.__init__(self, text)
        self.options = options

    def __call__(self):
        """Execute the decision point
        
        Displays the text content of the point, then prompts the player for text input. If the player inputs something that can be fuzzy matched to a keyword (a key in the `options` dict), then the point returns the name of point to go to based on the player's answer. Otherwise, the point will remind the player of their options, and then will ask for input again.
        
        Returns
        -------
        string
            The name of the point in the story (Book object) to go to next. 
        """
        self.__show__()  # show the content
        # the next point we're going to is the one associated with the option that matches
        self.next_point = self.options[self.__prompt__()]
        return self.__go__()  # then go to it

    def __prompt__(self):
        """Prompts the player to enter their choice.
        
        If the player inputs something that can be fuzzy matched to a keyword (a key in the `options` dict), then it returns the name of point to go to based on the player's answer. Otherwise, it will remind the player of their options, and then will ask for input again.
        
        Returns
        -------
        string
            The name of the point in the story (Book object) to go to next.
        """
        success = False
        while not success:  # Keep going until you get an answer
            user_input = get_user_input().upper().strip()  # removes whitespace
            for choice in self.options:
                if user_input == choice[0:len(user_input)].upper():
                    """if the letters in the input match the
                    beginning letters of any of the choices
                    ex. EXPL matches EXPLODE"""
                    return choice
            success = False  # Didn't get answer, remind player of choices
            self.__remind__()

    def __remind__(self):
        """Reminds the player of their choices by displaying all available keywords.
        """
        print('Your choices are:')
        for option in self.options:
            cprint(option.upper(), 'red', attrs=['bold'])


class Storypt(Point):
    """For story points.
    
    This is for story points, which contain only text content. The `text` content of the story will be displayed, then it will return `next_point`.
    
    
    Parameters
    ----------
    text : string
        The text of the story, formatted using the Muffintext format
        
    next_point : string
        The name of the next point in the story/The key chorresponding to the next point as in the `points` dictionary in the `Book` object.
    """

    def __init__(self, text, next_point=False):
        Point.__init__(self, text, next_point)


class Book(object):
    """Holds interactive fiction stories
    
    This object holds all the points and some metadata of the story, and can be called in order to display the story for a reader.

    Parameters
    ----------
    title : string
        The title of the book.
    authors : string or list of strings, optional
        The author(s) of the book. If 1 author, just a string containing the name. If there are multiple, a list of the names of the authors.
    start_point : string, optional
        The key of the first point in the story. While optional, if there is still none at runtime, then the story will fail.
    points : dict
        A dictionary containing every point in the story. Should use this format: `{..."name_of_point": PointObject(point, parameters),...}` Can be added to later.

    Callable
    --------
    When called, this will tell the story. It will display the title, run each point, go to the point returned by each point, and continue until it hits an end.
    """
    title = ""
    authors = []
    points = {}
    start_point = False
    next_point = ""

    def __init__(self, title, authors=None, start_point=None, points=None):
        self.title = title  # title of book
        self.authors = authors  # authors of book
        self.points = points or {}  # dictionary of points
        self.start_point = start_point  # point to start from

    def __call__(self):
        """Runs the story.

        This will tell the story to the user, complete with title graphic. It starts by calling the object located at points[`start_point`], then goes to the point returned by that point, until it reaches an end point.
        **!IMPORTANT! Make sure that a `start_point` is set before running this.**
        """
        self.__title__()  # display title
        sleep(3)  # wait
        try:
            # try to do the first point
            self.next_point = self.points[self.start_point]()
        except AttributeError:  # if it fails, there's probably not a start_point set
            print("Did you forget to give the book a start point?")
        while self.next_point != False:  # while there is a next_point
            # do it, and get that point's next point
            self.next_point = self.points[self.next_point]()
        self.__end__()  # once it's finished, show the end graphic

    def __end__(self):  # end graphic
        """Called when an end point is reached. Displays end graphic.
        """
        print(colored("====END====", attrs=["bold"]))

    def add_story(self, name, text, next_point):  # add story point
        """Add a story point
        
        Parameters
        ----------
        name : string
            Name of point.
        text : string
            Text content of point
        next_point : string
            Name of next point to go to after this one.
        """
        self.points[name] = Storypt(text, next_point)

    def add_decision(self, name, text, options):  # add decision point
        """Add a decision point
        
        Parameters
        ----------
        name : string
            Name of point.
        text : string
            Text content of point. Should be short and contain decision keywords. 
        options : dict
            Dictionary of points to go to depending on keyword typed in in this format: `{..."decision_keyword", "name_of_point_to_go_to_if_keyword_typed_in"}.
        """
        self.points[name] = Decisionpt(text, options)

    def set_start_point(self, name):  # set the point to start from
        """Set start point of the story.

        The start point is the name of the first point in the story, AKA the key corresponding to the first point in the `points` dict.
        
        Parameters
        ----------
        name : string
            The name of the start point of the story.
        """
        self.start_point = name

    def __author_text__(self):  # generate the "By Jon Doe and Don Joe" text
        """Creates author sentence
        
        Returns
        -------
        string
            Name of authors in sentence format. Ex. By Jon Doe and Adam Berns.
        """
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
        """Prints out title graphic.
        """
        print(colored('===', attrs=['bold']) + colored(self.title.upper(), 'red', attrs=[
            'bold']) + colored('===', attrs=['bold']))  # white ===, red title, white ===
        print('by', self.__author_text__())  # get author text

    def remove_point(self, name):  # remove a point
        """Removes a point from the story.
        
        Parameters
        ----------
        name : string
            Name of / key corresponding to the point to be removed.
        """
        self.points.pop(name)

    def test_point(self, name):  # just run one point
        """Runs a single point.
        
        Parameters
        ----------
        name : string
            Name of the point
        
        Returns
        -------
        string
            Next to go to after this point
        """
        return self.points[name]()
