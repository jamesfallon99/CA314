import enchant, json
import numpy
from random import randint, shuffle
from player import Player
import copy

global_words_on_board = []

class Game:
    def __init__(self, ID, players=None):
        """
        Initializes an instance of the Game class.
        :param board: board object
        :param players: set of player objects
        :param user_data: array of user data
        :param ID: game unique id
        """
        self.board = Board()
        self.players = []
        self.ID = ID
        self.word_dict = enchant.Dict("en_US")
        
    
    def check_move(self, player_board):
        """
        Check board configuration for illegal move
        """

        for y in range(len(self.board.board)):
            for x in range(len(self.board.board[y])):
                player_board[y][x].multiplier = self.board.board[y][x].multiplier
        
        rows = []
        row_tiles = []
        tile_word_groupings = []

        #Go through the rows and append each word in the rows both as a tile and a string
        for y in player_board:
            rows.append("".join([tile.letter for tile in y]))
            row_tiles.append([tile for tile in y if tile.letter != " "])
        
        symbols_rows = [row.strip().split(" ") for row in rows] #creating each individual word

        #Check if the words are valid in the english language
        for words in symbols_rows: 
            for word in words:
                if word != "" and len(word) > 1:
                    if self.word_dict.check(word) == False:
                        return []

        columns = []
        column_tiles = []
        
        #transposing the matrix to have columns as rows and iterate same as above
        player_transpose = numpy.array(player_board).transpose()
        
        for x in player_transpose:
            columns.append("".join([tile.letter for tile in x]))
            column_tiles.append([tile for tile in x if tile.letter != " "])
        
        symbols_columns = [column.strip().split(" ") for column in columns]
        for words in symbols_columns:
            for word in words:
                if word != "" and len(word) > 1:
                    if self.word_dict.check(word) == False:
                        return []

        # group the tiles accordingly when multiple words are on the same row/collumn
        symbols = symbols_rows + symbols_columns
        all_tiles = row_tiles + column_tiles

        for i in range(len(symbols)):
            for j in range(len(symbols[i])):
                if len(symbols[i][j]) != 1:     # ignore if it is a one letter word
                    tile_word_groupings.append(all_tiles[i][j:len(symbols[i][j])])

        duplicate = 0
        new_words = []
        global global_words_on_board
        
        #going through words found on playerboard and comparing against words on the board,
        #if new words have been found, add to newwords and update global board
        for tile_lists in tile_word_groupings:
            if len(global_words_on_board) == 0:
                global_words_on_board =  [tile_lists for tile_lists in tile_word_groupings if len(tile_lists) != 0]
                new_words = [tile_lists for tile_lists in tile_word_groupings if len(tile_lists) != 0]
                break
            for old_tiles in global_words_on_board:
                if tile_lists == old_tiles:
                    duplicate = 1
                else:
                    duplicate = 0
                    continue
            if duplicate != 1 and len(tile_lists) != 0:
                global_words_on_board.append(tile_lists)
                new_words.append(tile_lists)
        
        if new_words != []:
            self.update_board(player_board)

        return new_words
    
    def update_board(self, player_board):
        """
        Update board object with new configuration
        """
        self.board.board = player_board

    
    def update_tilebag(self, player_board, client_socket):
        """
        Update board tile bag
        - Only happens when a successful move is made.
        - Either a word is placed successfully, or they ask for an exchange.]
        - In  the case of a word, we'll check if the move is valid first.
        - If it is, get the number of tiles on board currently (self.board before updating / calling update_board())
        - and get the difference between that and the new player board. 
        """
        # calculate the number of tiles to be taken out

        # important that we pass the PORT as the client_socket argument
        # PORT is acting as the ID now pretty much
        removed_tiles = []

        for player in self.players:
            print(player.client_host_id, client_socket)
            if player.client_host_id == client_socket:
                print("hello")
                newly_placed_tiles = len(self.board.get_new_player_tiles(player_board))
                for tile in range(newly_placed_tiles):
                    curr_tile = player_board.get_tilebag().pop()
                    removed_tiles.append(curr_tile)
        
        return removed_tiles
    
    def check_word(self, word):
        """
        Check the dictionary if the word is legal
        :param word: word made by player
        """
        return self.word_dict.check(word)
    
    def calculate_score(self, new_words):
        """
        Calculate word score
        """

        total_score = 0

        for word in new_words:
            word_score = 0
            word_multipliers = []
            for tile in word:
                # get values to use
                multiplier_type, multiplier_value  = tile.get_multiplier()
                tile_value = tile.get_value()

                # our 3 cases
                if multiplier_type is None:
                    word_score += tile_value
                elif multiplier_type == "L":
                    word_score += (tile_value * multiplier_value)
                else: # type is "W"
                    word_score += tile_value
                    word_multipliers.append(multiplier_value)

            # apply word multipliers
            for num in word_multipliers:
                word_score = word_score * num
            
            # update the total score gained from this
            # move by the current new word score
            total_score += word_score
        
        self.remove_tile_multipliers(new_words)

        return total_score

    def remove_tile_multipliers(self, new_words):
        """
        :param tiles: List of tuples. Each tuple
        contains N Tile objects to form a word.
        """
        for word in new_words:
            for tile in word:
                tile.set_multiplier((None, 1))
    
    def send_game_data(self):                     
        # get_game_data() since it's called by the server on it's own Game instance, or may be return_game --> whatever works best
        # Send updated game object to server
        # will always need to pass back the newly updated state of the game, which means the updated Board, the updated score of "all" players (but this will really only be)

        return [self.board, self.players]

    def get_board(self):
        return self.board
    
    def get_players(self):
        return self.players

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

        # if the tilebag is empty then we need to check do the players still have tiles
        if not self.board.tilebag:
            for player in self.players:
                if player.tiles() > 0:
                    return False # game is not over

        return True

    def add_player(self, player):
        self.players.append(player)


class Board:
    def  __init__(self):
        """
        Initializes an instance of the Board class.
        :param board: the matrix (python lists)
        representation of the board.  
        :param tilebag: an array to hold a series of random
        Tile objects.
        """
        
        self.tilebag = self.generate_tilebag()
        self.board = self.generate_board()

    def printing(self):
        x = []
        for y in self.board:
            x += [tile.letter for tile in y]

        npboard = numpy.array(x)
        print(npboard)

    def generate_board(self):
        board = []
        multi = ["word", "letter", None]
        for y in range(0,14): # for each Y
            board.append([]) # append a list within the board list
            for x in range(0,14): # the list within has 14 x values
                #tile object to be placed at each x, initialises with letter=" ", value=None and random multiplier
                tile = Tile(" ", None, (multi[randint(0,2)], randint(1,3)))
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
        if self.board[x][y].value is None:
            self.board[x][y] = tile
            return True # successfully placed
        return False # not placed

    # helper function
    def get_number_tiles(self):
        """
        Get the number of player tiles on the board
        """
        count = 0

        for row in self.board:
            for tile in row:
                if tile.value is not None:
                    count += 1

        return count

    def get_new_player_tiles(self, player_board):
        new_tiles = []
        for current_row, player_row in zip(self.board, player_board):
            for current_tile, player_tile in zip(current_row, player_row):
                if (current_tile.value is '') and (player_tile.value is not ''):
                    new_tiles.append(player_tile)

        return new_tiles

    def get_tilebag(self):
        """
        getter
        """
        return self.tilebag

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
        self.multiplier = multiplier

    def __str__(self):
      return f'{self.letter} {self.value} {self.multiplier}'

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

    # needed to create a setter to reset tile multiplier for placed tiles after score calculation
    def set_multiplier(self, new_multiplier):
        """
        :param multiplier: tuple
        """
        self.multiplier = new_multiplier
