import json
import random
import socket
from threading import Thread

class Player:
    def __init__(self, name, tiles, score, client_host_id, board=None):
        """
        Initializes an instance of the Player class.
        :param name: player unique name
        :param tiles: instantiates player tiles as empty list
        :param score: instantiates player score as 0
        :param client_host_id: the player's client id
        """
        self.name = name
        self.tiles = tiles
        self.score = 0
        self.client_host_id = client_host_id
        self.board = board

    def get_score(self):
        """
        Return player score
        """
        return self.score

    def exchange_tiles(self, tiles):
        """
        Send request to exchange tiles
        """
        
        payload = {
            "exchange_tiles": tiles
        }
        self.client_socket.send(json.dumps(payload).encode("ascii"))

        '''
        # Test data
        tiles = [1,5,4,8]
        new_tiles = [9,9,9,9]
        self.tiles = [1,5,4,8,0,2,6]
        '''
        
        for i in range(len(self.tiles)): #Loop through the player's tiles
            for j in range(len(tiles)):#Loop through the tiles the player selected to be exchanged
                try:
                    if self.tiles[i] == tiles[j]:#if the value in the player's tiles equals the value in the tiles selected
                        self.tiles[i] = new_tiles[j] #Replace the tiles
                except IndexError:
                    continue

        return

    def shuffle(self):
        """
        Shuffles tiles on screen
        """
        random.shuffle(self.tiles)

        return #void

    def make_move(self):
        """
        Send updated board to client
        """
        payload = {
            "new_board": self.board
        }

        self.client_socket.send(json.dumps(payload).encode("ascii"))

        return #void

    def get_name(self):
        """
        Return player name
        """
        return self.name

    def get_ID(self):
        """
        Return id
        """
        return self.id

    def get_tiles(self):
        """
        Return player's tiles
        """
        return self.tiles

    def skip_turn(self):       
        """
        send request to server to move to next player
        """
        payload = {
            'skip_turn': True,  #Client sends data to server, the server will then handle the skipping turn
        }
        
        self.client_socket.send(json.dump(payload).encode("ascii"))
        
        return #void

    def set_tiles(self, tiles):
        """
        Update player tiles
        :param tiles: new tile list to be switched
        """
        self.tiles = tiles
        return #void

    def set_score(self, score):
        """
        Update player score
        :param score: new player score
        """
        self.score = score
        return #void

    def place_tiles(self, coord_x, coord_y, tile):
        """
        Update game board
        """
        self.board[coord_x][coord_y] = tile
        return #void

    def concede(self):
        payload = {
            'concede': True,  #Client sends data to server, the server will then handle the ending the game
        }
        
        self.client_socket.send(jason.dump(payload).encode("ascii"))

        return #void

# for testing
'''
def main():
    
    host, port = '127.0.0.1', 8000
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    server_socket, address = server.accept()

    # Player(id, name, tiles, score, client_socket, board)
    tiles = ['c', 'a', 'r']

    board = [
        [None, None, None],
        [None, None, None],
        [None, None, None]
    ]

    player = Player(1, 'Bob', tiles, 0, client, board)
    player.make_move()

    message = server_socket.recv(1024).decode('ascii')
    print('Test make_move():')
    print(f'{message}\n')

    player.exchange_tiles(['c', 'r'])

    server_response = {
        'exchange_tiles': ['d', 'f'],
    }

    server_socket.send(json.dumps(server_response).encode('ascii'))

    message = server_socket.recv(1024).decode('ascii')
    print('Test exchange_tiles():')
    print(f'{message}\n')


    client.close()
    server_socket.close()
    server.close()

if __name__ == "__main__":
    main()

'''