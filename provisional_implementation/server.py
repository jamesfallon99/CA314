class Server:

    new_game = Game()

    new_game_board = new_game.get_state()

    print(new_game_board)

    init:
        self.server_socket
        self.client_sockets = {}
        self.game = Game()


# may well need more functions for server , can mention this lack of foresight was due to a lack of experience


# recieve data in some way from client over sockets    
# e.g removed methods because sockets have functionality built in


# decoded_data --> Game State --> All the player objects up to date, 
# overall, any time we receive data, it will be from a single cient. As such, this will be the most up to date state of everything for that client.
# theoretically, the main thing we should be getting back, is just the new move from any given player. Then we enact that move on the game instance.
# So all updating of the game state is happening on this side. Once it's all updated, the newly updated state is broadcast back out to all clients.

{board: Board}


    

