from termcolor import colored, cprint
from time import sleep

class parsed_function(object): #Holds parsed functions
	function = False 
	arguments = ()
	def __init__(self, function, arguments): #Take the functions and the arguments
		self.function = function
		self.arguments = arguments
	def do(self):  #Run then when it is time
		self.function(self.arguments)

class parsed_text(object): #Holds parsed text
	text = ""
	text_animation = False
	def __init__(self,text,animation=False):
		self.text = text
		self.text_animation = animation
	def do(self): #Display the text
		if self.text_animation:
			if self.text_animation == "placeholder":
				pass
			else:
				pass
		else:
			print self.text
	def __typing__(self):
		print text #placeholder

class point(object): #Base for both story points and decision points
	parsed_list = []
	next_point = False
	def __init__(self, text): #When initializing
		self.parsed_list = self.__parse__(text) #When initializing, take the raw text, and parse it
	def __format__(self, text): #Private method for formatting text. 
		return format_text(text) #Return the output of the function 
	def __parse__(self, text):
		"""This parses the text into blocks of text and functions, then formats the text"""
		animation = False
		raw_list = text.split('|') #pipes break the text into blocks
		parsed_list = [] #not self.parsed_list
		for raw_block in raw_list: #go though each raw block
			if any(x in raw_block for x in '<>'): #If there are function tokens in the text,
				if '<' in raw_block: #<n> means sleep for n seconds
					sleep_time = float(raw_block.strip('<>'))
					parsed_list += [parsed_function(sleep, sleep_time)] #Make it into a parsed function that sleeps for that many seconds
			else: #if these tokens aren't there, it's just text that needs formatting
				#may add in text animations later, but not now
				formatted_text =  self.__format__(raw_block) #format the text
				parsed_list += [parsed_text(formatted_text, False)] #add it to the list
		return parsed_list
	def __show__(self):
		"""Displays the content of this point"""
		for parsed_block in self.parsed_list: #go through each parsed block
			parsed_block.do() #Excecute them, either by printing or by calling
	def __go__(self):
		"""Returns the point to go to next"""
		if self.next_point != False:
			return self.next_point
		else:
			return False

class decision(point):
	"""For decision points
	Usage: decision(text, options)
	text = text to be formatted
	options = dictionary of options 
	that the player has and the resulting
	point to go to for each option"""
	options = {}
	def __init__(self,text,options):
		point.__init__(self,text)
		self.options = options
	def do_point(self):
		"""Show the text
		Get the next point
		Go to it"""
		self.__show__() #show the content
		self.next_point = self.options[self.__prompt__()] #the next point we're going to is the one associated with the option that matches
		return self.__go__() #then go to it
	def __prompt__(self):
		"""Ask the player their choice"""
		success = False
		while success == False: #Keep going until you get an answer
			user_input = raw_input('>').upper().strip() #removes whitespace
			for choice in self.options:
				if user_input == choice[0:len(user_input)].upper():
					"""if the letters in the input match the
					beginning letters of any of the choices
					ex. EXPL matches EXPLODE"""
					return choice
					success = True #Got an answer, stop while loop
			else:
				success = False #Didn't get answer, remind player of choices
				self.__remind__()
	def __remind__(self):
		"""Reminds the player of their choices"""
		print 'Your choices are:'
		for option in self.options:
			cprint(option.upper(), 'red', attrs=['bold'])
	
class story(point):
	"""For story points
	Usage: name = story(text, next_point)
	if next_point = False, the story ends there"""
	def __init__(self, text, next_point=False):
		point.__init__(self,text)
		self.next_point = next_point
	def do_point(self):
		"""Show the text of the point
		Then go to the next one"""
		self.__show__()
		return self.__go__()


class book():
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
	def __init__(self, title, authors=None, start_point=None, points={}):  
		self.title = title #title of book
		self.authors = authors #authors of book
		self.points = points #dictionary of points
		self.start_point = start_point #point to start from
	def tell(self):
		"""
		Run story
		!IMPORANT - Set start_point before running
		"""
		self.__title__() #display title
		sleep(3) #wait
		try:
			next_point = self.points[self.start_point].do_point() #try to do the first point
		except: #if it fails, there's probably not a start_point set
			print "Did you forget to give the book a start point?"
			raise 
		while next_point != False: #while there is a next_point
			next_point = self.points[next_point].do_point() #do it, and get that point's next point
		self.__end__() #once it's finished, show the end graphic
	def __end__(self): #end graphic
		print colored("====END====", "white", attrs=["bold"]) 
	def add_story(self, name, text, next_point): #add story point
		self.points[name] = story(text, next_point)
	def add_decision(self, name, text, options): #add decision point
		self.points[name] = decision(text, options)
	def set_start_point(self, name): #set the point to start from
		self.start_point = name
	def __author_text__(self): # generate the "By Jon Doe and Don Joe" text
		author_text = ''
		if type(self.authors) == list: #if it's a list
			if len(self.authors) <= 2: #and there's less than or equal to two in them
				author_text = ' and '.join(self.authors) #join the items together with the word 'and'
			else:  #otherwise
				first_author = self.authors[0] #first author
				mid_authors = self.authors[1:len(self.authors)-1] #middle authors
				last_author = self.authors[len(self.authors)-1] #last author
				author_text = first_author #start with the first author
				for mid_author in mid_authors:
					author_text = author_text + ', ' + mid_author #add commas between all the mid_authors
				author_text = author_text + ', and ' + last_author #use an and for the last author
		else: 
			author_text = self.authors #if it's not a list, it's just one author
		author_text += '.' #oh, and add a period at the end
		return author_text #return
	def __title__(self): #display title graphic
		length = len(self.title) #plaeholder for potental adaption to terminal size in future
		print colored('===', 'white', attrs=['bold']) + colored(self.title.upper(), 'red', attrs=['bold']) + colored('===', 'white', attrs=['bold']) #white ===, red title, white ===
		print 'by', self.__author_text__() #get author text
	def remove_point(self, name): #remove a point
		self.points.pop(name)
	def test_point(self, name): #just run one point
		return self.points[name].do_point()

def format_text(text):
	"""Formats text given to it
	% makes text red and bold
	* makes text bold
	_ make text underlined
	@ makes text blink
	` escapes characters (so they don't make the text do anything)
	"""
	ftext_str = "" #init variable for holding formatted text
	ftext_list = []
	text_list = text.split('|')
	text_key = False #doesn't start key colored
	text_bold = False 
	text_under = False
	text_blink = False
	text_escape = False
	for char in text:
		text_attrs = []
		text_color = ''
		if char == '%' and text_escape != True: #a % makes it either turn red or stop being red
			text_key = not text_key #by inverting it
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
				text_attrs +=["blink"]
			if text_color:
				ftext_str += colored(char, text_color, attrs=text_attrs)
			else:
				ftext_str += colored(char, attrs=text_attrs)
		if char == '`' or text_escape:
			text_escape = not text_escape
	return ftext_str
