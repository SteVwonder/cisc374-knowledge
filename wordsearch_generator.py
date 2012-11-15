import random

# Reads the words out of a file into a set of words to be used
# for the generator
def getvocab(filename = '/vocablist.txt'):
    words = []
    definitions = []
    fd = open(filename, 'r')
    try:
	for line in fd.readlines():
	    if "'" in line:
		continue
	    line = line.strip().lower()	    #change .lower()
	    if ":" in line:
		word, definition = line.split(' : ', 1)
		words.append(word)
		definitions.append(definition)
    finally:
	fd.close()
    return words, definitions

# A few utilities to be used in positioning the words and making the grid
alphabet = "abcdefghijklmnopqrstuvwxyz"

# Easy only has words going to the right and down
# Medium has those of easy as well as reverse order words and forward diagonals up and down
# Hard has those of medium but the diagonals can be reversed order now
difficulties = { 'easy': ([1, 0], [0, 1]), 'medium' : ([1, -1], [1, 0], [1, 1], [0, 1], [0, -1], [-1, 0]), 'hard' : ([1, -1], [1, 0], [1, 1], [0, 1], [0, -1], [-1, -1], [-1, 0], [-1, 1]) }

class Grid(object):
    def __init__(self, width, height):
	self.width = width
	self.height = height
	self.data = ['.'] * (width * height)
	self.words = []
	self.choices = ['0'] * (width * height)

    # Determines the placement of the word at random
    # The length of an existing word can be input to determine 
    # the starting or finish point of the word
    def word_placement(self, word_length, level_directions):
	x_dir, y_dir = random.choice(level_directions)
	min_x = (word_length - 1, 0, 0)[x_dir + 1]
	max_x = (self.width - 1, self.width - 1, self.width - word_length)[x_dir + 1]
	min_y = (word_length - 1, 0, 0)[y_dir + 1]
	max_y = (self.height - 1, self.height - 1, self.height - word_length)[y_dir + 1]
	x = random.randint(min_x, max_x)
	y = random.randint(min_y, max_y)
	return x, y, x_dir, y_dir

    # Checks if word can be written to desired spot by cycling
    # through the to-be positions for empty spaces or letters that
    # match other letters to implement overlapping, then places them
    def write_word(self, word, pos_x, pos_y, x_inc, y_inc):
	
	x, y = pos_x, pos_y
	for letter in word:
	    pos = x + self.width * y
	    check = self.data[pos]
	    if check != '.' and check != letter:
		return False
	    x += x_inc
	    y += y_inc

	x, y = pos_x, pos_y
	for letter in word:
	    pos = x + self.width * y
	    self.data[pos] = letter
	    x += x_inc
	    y += y_inc

	return True
    
    # Cycles through the list of words placing the longest first, second
    # longest second, etc. Cycles through the list up to 100 times to
    # chance upon a working placement
    def place_words(self, words, level_directions, tries = 100):
	
	# Gets the list of words in descending order of length
	word_list = list(words)
	word_list.sort(key = lambda x: len(x), reverse = True)

	for word in word_list:
	    word_len = len(word)
	    while True:
		x, y, x_dir, y_dir = self.word_placement(word_len, level_directions)
		if self.write_word(word, x, y, x_dir, y_dir):
		    self.words.append((word, x, y, x_dir, y_dir))
		    break
		tries -= 1
		if tries <= 0:
		    return False
	return True

    # Fills all the empty ('.') grid spots with random letters
    # while also marking where the words are on the overlay grid
    def fill(self):
        for pos in xrange(self.width * self.height):
	    if self.data[pos] == '.':
		self.data[pos] = random.choice(alphabet)
	    else:
		self.choices[pos] = '1'

''' # Prints screen to stdout for testing purposes
    def print_to_screen(self):
	if '.' in self.data:
	    return False

	for row in xrange(self.height):
	    print ' '.join(self.data[row * self.width : (row + 1) * self.width]) + "\n"
	return True
'''

# Puts the grid together calling the function to lay the words on the grid
# and then fills the rest of the grid with random letters, then returns grid
def make_grid(difficulty = "medium", words = [], tries = 100, height = None, width = None):
    
    if height != None and width != None:
	height = height
	width = width
    else:
	width = height = len(max(words, key=len)) + 2

    # Makes a grid and tries up to 100 times to place the words
    while True:
	grid = Grid(width, height)
	if grid.place_words(words, difficulties[difficulty]):
	    break
	tries -= 1
	if tries <= 0:
	    return None

    grid.fill()
    return grid
