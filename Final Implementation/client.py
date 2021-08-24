from game import Board, Tile
from player import Player
import threading
import socket, pickle
import copy
import json
from json import JSONEncoder

# NOTE: in our presentation we can mention that the changes we have made i.e: adding threading was necessary in order to making it run locally for the demo.
# NOTE: because user input and GUI are yet to be implemented we are testing using threads and the terminal.

class Client(threading.Thread):
    def __init__(self, socket, data_out=None, data_in=None, player=None):
        """
        Initializes an instance of the client class.
        :param socket: socket object for the client.
        :param data_out: JSON object
        :param data_in: JSON object
        :player: Player object
        """
        super().__init__()
        self.socket = socket
        self.data_out  = data_out
        self.data_in = data_in
        self.player = player

    def con(self, host , port):
        self.socket.connect((host, port))

    def run(self):
        while True:
            received = pickle.loads(self.socket.recv(8192))
            if type(received) == Board:
                self.player.board = received
            elif type(received) == int:
                self.player.score += received
            elif type(received) == str:
                if received == 'invalid word':
                    print(received)
                else:
                    self.player.client_host_id = int(received)
            elif type(tuple):
                print(received)

    def send_game_data(self, data, target):
        """
        Sends updated and encoded game state data to the server,'
        packaged/structured correctly for being
        interpreted by the Server.
        :param data: JSON object
        :param target: server socket object
        """
        return # void

    def encode(self, data):
        """
        :param data: Encoding data to be sent via
        socket to server.
        """
        return encoded_data

    def decode(self, data):
        """
        :param data: Converts data into the correct
        format/structure to be parsed and then utilised.
        """
        return decoded_data

    def input_name(self, name):
        """
        Updates player object's name
        :param name: player inputted name
        """
        return #void

    def input_game_code(self, code):
        """
        :param code: player inputted code
        """
        return code

    def display(self):
        """
        Render board object to users screen
        """
        return #void

    def join_game(self, code, target):
        """
        Passes player name and code to the server
        :param code: player inputted code
        :param target: object for code to be sent to
        """
        return #void

    def start_game(self):
        """
        Send game creation request to server
        """
        return #void

    def create_game(self, name):
        """
        Creates a game
        :param name: player name to be set
        """
        return #void


# substitution for GUI due to time constraint
# function runs inside a thread
# use the commands to test various tasks that would normally require an GUI
def handle_input(client):
    commands = [
        '!help',
        '!place_tile',
        '!display',
        '!end_turn',
    ]
    
    print(f'For a list of commands use !help')
    
    while True:
        player_input = input('')
        if player_input == '!help':
            print('Here are all the commands available:')
            print(commands)

        elif player_input == '!place_tile':
            print(f'Format for inserting is => letter y x e.g: a 4 1')
            print('Please type the move you wish to make using the above format')

            tile_placement_input = input('Move: ')
            letter, y, x = tile_placement_input.split(' ')
            corresponding_tile = [tile for tile in client.player.tiles if tile.letter == letter]

            client.player.board.place_tile(corresponding_tile[0], int(y), int(x))
            print(f'You inserted {letter} into position [{y}][{x}] on the board')

        elif player_input == '!display':
            client.player.board.printing()

        elif player_input == '!end_turn':
            client.socket.send(pickle.dumps(client.player.board))

        elif player_input == '!send_test':
            client.socket.send(pickle.dumps(client.socket.getsockname()))

        elif player_input == '!see_players':
            client.socket.send(pickle.dumps('see_players'))

        elif player_input == '!see_score':
            print(client.player.score)

        elif player_input == '!join_game':
            client.socket.send(pickle.dumps('join_game'))
            client.socket.send(pickle.dumps(client.player))

        elif player_input == '!see_tiles':
            print([tile.letter for tile in client.player.tiles])

def main():
    # client socket
    # make socket use TCP for reliable communication
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # player board
    player_board = Board()
    # player_board.board[4][1] = Tile('c', 2, (None, 0))
    # player_board.board[4][2] = Tile('a', 4, ('L', 2))
    # player_board.board[4][3] = Tile('t', 5, ('W', 3))

    # tiles
    player_tiles = [
            Tile("c", 2, (None, 0)),
            Tile("a", 4, ("L", 2)),
            Tile("t", 5, ("W", 3)),
            Tile("s", 9, ("L", 2)),
            Tile("d", 2, (None, 0)),
            Tile("o", 7, ("L", 2)),
            Tile("g", 3, ("W", 3)),
        ]
        
    client = Client(sock)
    ligma = Player("ligma", player_tiles, 0, client.socket.getsockname())  #(self, id, name, tiles, score, client_socket, board):

    client.player = ligma
    client.con('127.0.0.1', 8000)
    client.start()

    terminal_input = threading.Thread(target=handle_input, args=(client, )) # please note player_board is the "server" board at the moment ofr testing purposes
    terminal_input.start()

if __name__ == "__main__":
    main()