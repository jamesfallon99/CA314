import socket
import threading
import pickle
from game import Game, Board, Tile
from player import Player
import copy

# NOTE: in our presentation we can mention that the changes we have made i.e: adding threading was necessary in order to making it run locally for the demo.

class Server(threading.Thread):
    def __init__(self, socket, game=None):
        """
        Initializes an instance of the server class.
        :param socket: socket object for the server
        :param clients: a list of client objects
        :param game: a game object which handles the logic
        """
        super().__init__()
        self.socket = socket
        self.clients = []
        self.game = game

    def run(self):
        # listen to up to 5 connections
        self.socket.listen(2)
        print(f'Listening at {self.socket.getsockname()}..')
        self.game = Game(1)
        print(f'Game {self.game.ID} has been created..')

        while True:
            # accept any incomming connection
            client, sockname = self.socket.accept()
            print(f'Accepted a new connection from {client.getpeername()} to {sockname}')

            server_socket = ServerSocket(client, sockname, self)

            server_socket.start()

            self.clients.append(server_socket)


    def encode(self, data):
        """
        :param data: Encoding data to be sent via
        socket to either a Client or Game object.
        """
        return encoded_data

    def decode(self, data):
        """
        :param data: Converts data into the correct
        format/structure to be parsed and then utilised.
        """
        return decoded_data

    def send_game_data(self, data):
        """
        Sends updated and encoded game state data to the client,'
        packaged/structured correctly for being
        interpreted by the Client.
        :param data: JSON object
        ####:param target: Client socket object
        """
        data = pickle.dumps(data)
        for sock in self.clients:
            sock.send(data)
        #return # HTTP JSON data i.e status codes for whether the data was  sent successfully

    def send_player_data(self, data, target):
        """
        Sends data to the game, packaged/structured
        correctly for being interpreted by the recipient class.
        :param data: JSON Object
        :param target: Game instance for that Player.
        """
        return # does not return anything i.e Void

    def make_name_unique(self, name):
        """
        Takes an entered Player username that already exists
        in the target game, and makes it unique (by appending
        digits).
        :param name: String representation of username.
        """
        return unique_name

    def check_capacity(self):
        """
        Checks whether there is sufficient server
        capacity for a new client connection / game.
        """
        return # boolean

    def create_code(self):
        """
        Generates a unique ID code to represent
        the game and allow users to join.
        """
        return game_code

    def send_result_info(self):
        """
        Only used when game is ending, sends final results
        of game to client and also let's client know that
        the connection can be closed and the game has ended.
        """
        return # JSON object

    def create_game(self):
        """
        Initializes a game object when a game creation
        request is received.
        """
        return # void

class ServerSocket(threading.Thread):
    '''
    ServerSocket class: responsible for handling communication between the clients and the server sided sockets
    '''
    def __init__(self, sc, sockname, server):
        '''
        Server class constructor, calls super() on threading.Thread

        :param sc: the socket object that connected to the server
        :param sockname: name of the socket
        :param server: the server object which has this ServerSocket object in it's connections1024
        '''
        super().__init__()
        self.sc = sc
        self.sockname = sockname
        self.server = server
        #self.chatroom = None        # this will be assigned once the thread starts

    def run(self):
        '''
        Called by threading.Thread upon start()
        While the thread is running receive any messages from the clients
        Pass the message to the server for broadcasting
        '''
        # the first message a ServerSocket will receive from a client is
        # the chatroom that client belongs to so we set the chatroom attribute here
        # chatroom = self.sc.recv(1024).decode('ascii')
        # self.chatroom = chatroom


        while True:
            # receive any incoming messages
            payload = pickle.loads(self.sc.recv(8192))
            if type(payload) == Board:
                # print said message server side 
                #print(f'{self.sockname} says {pickle.loads(payload)}')
                current_board = copy.deepcopy(self.server.game.board)
                new_tiles = self.server.game.check_move(payload.board)
                if new_tiles != []:
                    player_score = self.server.game.calculate_score(new_tiles)
                    self.sc.send(pickle.dumps(player_score))
 
                    
                    # getting tiles from tilebag and tiles used by player
                    # sending them to update hand and tilebag for player
                    used_tiles = self.server.game.board.get_new_player_tiles(current_board.board)
                    new_tiles_from_tilebag = self.server.game.update_tilebag(current_board, self.sockname[1])
                    print(used_tiles, new_tiles_from_tilebag)
                    self.sc.send(pickle.dumps((used_tiles, new_tiles_from_tilebag)))

                    self.server.send_game_data(self.server.game.board)

                    self.server.game.board.printing()
                else:
                    self.sc.send(pickle.dumps('invalid word'))
                    self.sc.send(pickle.dumps(self.server.game.board))
                    self.server.game.board.printing()
            elif type(payload) == str:
                if payload == 'join_game':
                    payload = pickle.loads(self.sc.recv(8192))
                    self.server.game.add_player(payload)
                    self.sc.send(pickle.dumps(copy.deepcopy(self.server.game.board)))
                    self.sc.send(pickle.dumps(str(self.sockname[1])))
                elif payload == 'see_players':
                    print(self.server.game.players)
            else:
                print(payload)


    def send(self, data):
        '''
        Send the encoded message to all other sockets

        :param message: message to be sent
        '''
        self.sc.sendall(data)

def main():
    # make socket use TCP for reliable communication
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('127.0.0.1', 8000))
    
    #game = Game()
    server = Server(sock)
    server.start()

    # Thread(target=handle_client, args=(client, username, chatroom)).start()

if __name__ == "__main__":
    main()