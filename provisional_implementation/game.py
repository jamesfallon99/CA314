import enchant, json
import numpy
from random import randint, shuffle


# get board from player
# check move
# update board
# update tilebag
# send updated board to the rest of the players

class Game:
    def __init__(self, players, ID):
        """
        Initializes an instance of the Game class.
        :param board: board object
        :param players: set of player objects
        :param user_data: array of user data
        :param ID: game unique id
        """
        self.board = Board()
        self.players = players
        self.ID = ID
        self.word_dict = enchant.Dict("en_US")
    
# Provisional
def check_move(board, player_board):
        """
        Check board configuration for illegal move
        """
        # - valid pos?
        # - valid word? (check_word)
        # suggestion: have a dictionary of moves mapped to each other like makemove:checkmove
        # board (matrix of tile objects)
        # [
        # [T1-1, T2-1, T3-1 ...T14-1]
        # [T21, T2, T3 ...T14]
        # [T31, T2, T3 ...T14]
        # [T41, T2, T3 ...T14]
        # [T51, T2, T3 ...T14]
        # [..................]
        # [..................]
        # [T1-14]
        # ]
        '''
        player

        ['c', 'a', 'r', 's']
        ['',   '', 'a',  '']
        ['',   '', 'c',  '']
        ['',   '', 'e',  '']

        server
        
        [['',  'a', 'r', ''],
        ['a',   'b', '',  'a'],
        ['',   '', 'c',  ''],
        ['',   '', 'e',  '']]
        '''
#        AttributeError: 'list' object has no attribute 'encode'

        
        rows = []
        word_dict = enchant.Dict("en_US")
        for y in player_board:
            rows.append("".join([tile.letter for tile in y]))           # change board generation to use " " instead of None
        
        symbols = [row.strip().split(" ") for row in rows] #joining what we just split it has to happen i swear

        for words in symbols:
            for word in words:
                print(word)
                if word_dict.check(word) == False:
                    return False

        columns = []
        player_transpose = numpy.array(player_board).transpose()
        
        for x in player_transpose:
            columns.append("".join(x))           # change board generation to use " " instead of None
        
        symbols = [column.strip().split(" ") for column in columns]
        for words in symbols:
            for word in words:
                print(word)
                if word_dict.check(word) == False:
                    return False

        # ['c', 'c', 'race', 's']

        return True
    
    def update_board(self, player_board):
        """
        Update board object with new configuration
        """
        self.board = player_board

    
    def update_tilebag(self, player_tiles, word):
        """
        Update board tile bag
        - Only happens when a successful move is made.
        - Either a word is placed successfully, or they ask for an exchange.]
        - In  the case of a word, we'll check if the move is valid first.
        - If it is, get the number of tiles on board currently (self.board before updating / calling update_board())
        - and get the difference between that and the new player board. 
        """


        
        return #void
    
    def check_word(self, word):
        """
        Check the dictionary if the word is legal
        :param word: word made by player
        """
        return self.word_dict.check(word)
    
    def update_user_data(self):
        """
        Update user data
        - updating the state of the board for every player
        - remove the tiles used from the player that made the move
        """
        # update the board for everyone

        # update the players hand

        return #void
    
    def calculate_score(self, new_words):
        """
        Calculate word score
        """
        # new words = [("cat",start_XY, end_XY)] | where start_XY = (X,Y)
        for word_data in new_words:
            word_multipliers = []
            # get start coords
            start_x = word_data[1][0]
            start_y = word_data[1][1]
            # get end coords
            end_x = word_data[2][0]
            end_y = word_data[2][1]

            # if x values of start and finish are the same, this means it's a vertical word
            if start_x == end_x:
            
            #[(tile objects), (tile objects)]
            #TODO finish this

    #     if 

    #     d
    #   c o a t
    #     g


    #     s c a r # if word in list, check the coords. If the same start_XY and end_XY, then it must somehow be a duplicate
    #     c
    #     a
    #     r
    #     s u n s h i n e
        

    #     # generate the list of all words including the new words [house, house, cat, dog, mouse]
    #     # compare that to the global list of words on the board already [cat, dog, mouse, house]

    #     # [house]


        return score
    
    def send_game_data(self):                     
        # get_game_data() since it's called by the server on it's own Game instance, or may be return_game --> whatever works best
        """
        Send updated game object to server
        """
        # will always need to pass back the newly updated state of the game, which means the updated Board, the updated score of "all" players (but this will really only be)

        return [self.board, self.players]
     
        """
    def return_state(self):
        ""
        Return state of game
        ""
        return state
        """
    def check_board_config(self, board): ### move to client 
        """
        Check if board config is valid
        :param board: board object
        """
        return  # bool

    def send_user_scores(self, players):
        """
        Send player's scores to server
        This is our leaderboard data structure i.e a sorted list/array of players integer scores
        """

        scores = [player.get_score() for player in self.players]
        scores.sort(reverse=True)

            # add players in correct order by score
            # i.e creating the leaderboard
        return scores
     
    def check_end_condition(self):
        """
        Checks if game should end
        """
        #if len(self.players[0].tiles) == 0 and len(self.players[1].tiles) == 0:
        #    return True

        # if the tilebag is empty then we need to check do the players still have tiles
        if not self.board.tilebag:
            for player in self.players:
                if player.tiles() > 0:
                    return False # game is not over

        return True


class Board:
    def  __init__(self, tilebag, type):
        """
        Initializes an instance of the Board class.
        :param board: the matrix (python lists)
        representation of the board.  
        :param tilebag: an array to hold a series of random
        Tile objects.
        :param type: sets the type of the current Board
        based on the game type.
        """
        
        self.tilebag = self.generate_tilebag()
        self.type = type
        self.board = self.generate_board()

    def generate_board(self):
        board = []
        multi = ["word", "letter", "None"]
        for y in range(0,14): # for each Y
            board.append([]) # append a list within the board list
            for x in range(0,14): # the list within has 14 x values
                #tile object to be placed at each x, initialises with letter=None, value=None and random multiplier
                tile = Tile(None, None, (multi[randint(0,2)], randint(1,3))) # TODO Discuss having a limit on multiplier tiles
                board[y].append(tile)
        return board

    def generate_tilebag(self):
        """
        Initializes tilebag and tiles and populates it with
        tiles with random values
        """

        tilebag = []
        # letter : (amount to be created, value)
        letters = {'a': (9,randint(0,50)),  'b': (2,randint(0,50)),  'c': (2,randint(0,50)), 'd': (4,randint(0,50)),
                 'e': (12,randint(0,50)),  'f': (2,randint(0,50)),  'g': (3,randint(0,50)), 'h': (2,randint(0,50)),
                 'i': (9,randint(0,50)),  'j': (2,randint(0,50)), 'k': (2,randint(0,50)), 'l': (4,randint(0,50)),
                 'm': (2,randint(0,50)),  'n': (6,randint(0,50)),  'o': (8,randint(0,50)), 'p': (2,randint(0,50)),
                 'q': (1,randint(0,50)), 'r': (6,randint(0,50)),  's': (4,randint(0,50)), 't': (6,randint(0,50)),
                 'u': (4,randint(0,50)),  'v': (2,randint(0,50)),  'w': (2,randint(0,50)), 'x': (1,randint(0,50)),
                 'y': (2,randint(0,50)),  'z': (1,randint(0,50))}

        for letter, values in letters.items():
            for i in range(values[0]):
                tilebag.append(Tile(letter, values[1], 1))

        return shuffle(tilebag)

    # basically a getter
    def get_tile_at_position(self, x, y):
        """
        Getter to return the Tile object at
        a particular position on the board.
        """
        return board[x][y]

    # acts like a setter 
    def place_tile(self, tile, x, y):
        """
        Place a new Tile "onto" the board.
        """
        if self.board[x][y].letter is None:
            self.board[x][y] = tile
            return True # successfully placed
        return False # not placed

class Tile:
    def __init__(self, letter, value, multiplier):
        """
        Initializes an instance of the Tile class.
        :param letter: string/char representation of a letter (A-Z)
        :param value: an integer value to represent the value
        of the letter / tile.
        :param multiplier: sets the multiplier type of the tile.
        This is used for managing multiplier tiles on the board.
        """
        self.letter = letter
        self.value = value
        self.multiplier = multiplier # (word, 3) (letter, 2)
        self.coordinates = 

    def get_value(self):
    """
    Getter to return value attribute of
    the tile object.
    """
        return self.value
        
    def get_letter(self):
    """
    Getter to return letter attribute of
    the tile object.
    """
        return self.letter
        
    def get_multiplier(self):
    """
    Getter to return the multiplier
    attribute of the tile object.
    """
        return self.multiplier



""" 
server receives a new board

game gets it

we now have the current board and the new player board

we want to check if the move is valid or not

once a valid move has been made:
- we need to calculate the score of the word placed --> this can then be tracked in game loop and used later i.e UPDATED_PLAYER_SCORE
    * will all be done using the comparison of the old and new board. Using positions (co-ords). Use multipliers from current board on tile values of the newly placed tile in new board
    We calculate the total value of the word, and any letter multipliers as we go. We add any word multipliers into a list which will be applied to the total word value (letters values + letter multipliers) at the end to get the total score


- update the tilebag
    * we still have the old and new boards. We compare the two and find the number of new tiles on the new board. This is the number of tiles placed i.e the
      number of tiles used by the player. We then remove this number of tiles randomly from the tile bag and store them i.e NEW_TILES to be given to the player
      to replace their used tiles.

- then update the players score and tiles rack
    - update the INDIVIDUAL players score --> player.score = UPDATED_player_score
    - For updating the tile rack, we have to know EXACTLY which tiles we need to remove from the players rack. So we go and compare the two boards again, finding all the new Tile objects
      which were placed on the board. We then have their letter values stored as being the tiles / letter used / placed. Then we can iterate over the player tile attribute (player.tiles),
      checking the letter attribute of those tiles, and remove the matches. 
        
          # find all the new tile objects placed and get all their letter attributes into a list
      letter_of_tiles_placed = ["c", "a", "r", "s"]

      while i < len(letter_of_tiles_placed)

- update the board
- update all the players details

"""