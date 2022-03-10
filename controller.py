from grid import Grid
from gui import GUI
from timeit import default_timer

class Controller:
    """
    Class Controller.
    The controller manage the Hex game itself, ad how the player plays one after each other.
    """
    def __init__(self, size, player1, player2):
        self._grid = Grid(size)
        self._player1 = player1
        self._player2 = player2
        self._current_player = 1
        self._winner = 0
        self.player1TotalTime = 0.0
        self.player2TotalTime = 0.0

    def update(self):
        """
        Update method.
        This method check which player is supposed to play
        and call the function :func:`~Player.Player.step`
        of the class Player that decide what moves will be played.
        """
        if self._current_player == 1:
            # Call the methods steps that will return the move of Player 1.
            start = default_timer()
            coordinates = self._player1.step()
            self.player1TotalTime = self.player1TotalTime +  (default_timer() - start)
            print('took %.2f seconds for player 1' % (default_timer() - start))
            # Modify the grid with the new move.
            self._grid.set_hex(self._current_player, coordinates)
            self._current_player = 2
            self._player2.update(coordinates)
        else:
            # Call the methods steps that will return the move of Player 2.
            start = default_timer()
            coordinates = self._player2.step()
            self.player2TotalTime = self.player2TotalTime + (default_timer() - start)
            print('took %.2f seconds for player 2' % (default_timer() - start))
            # Modify the grid with the new move.
            self._grid.set_hex(self._current_player, coordinates)
            self._current_player = 1
            self._player1.update(coordinates)

        self._check_win()

    def _check_win(self):
        """
        Check the winning condition for both player.
        """

        neighbors1 = []
        neighbors2 = []
        for y in range(self._grid.get_size()):
            if self._grid.get_hex([0, y]) == 1:
                neighbors1.append([0, y])

        for x in range(self._grid.get_size()):
            if self._grid.get_hex([x, 0]) == 2:
                neighbors2.append([x, 0])

        if len(neighbors1) == 0 and len(neighbors2) == 0:
            return

        # Checking if Player 1 won
        for neighbor in neighbors1:
            neighbors = self._grid.neighbors(neighbor)
            for next_neighbor in neighbors:
                if self._grid.get_hex(next_neighbor) == 1 and (next_neighbor not in neighbors1):
                    if next_neighbor[0] == self._grid.get_size()-1:
                        self._winner = 1

                        countPlayer1 = 0
                        countPlayer2 = 0
                        for x in range(self._grid.get_size()):
                            for y in range(self._grid.get_size()):
                                if self._grid.get_hex([x, y]) == 1:
                                    countPlayer1 = countPlayer1 + 1
                                if self._grid.get_hex([x, y]) == 2:
                                    countPlayer2 = countPlayer2 + 1
                        print("player 1 total moves", countPlayer1)
                        print("player 2 total moves", countPlayer2)
                        print("Player 1 average time for each move:" , self.player1TotalTime/countPlayer1)
                        print("Player 2 average time for each move:" , self.player2TotalTime/countPlayer2)
                        return
                    else:
                        neighbors1.append(next_neighbor)

        # Check if Player 2 won.
        for neighbor in neighbors2:
            neighbors = self._grid.neighbors(neighbor)
            for next_neighbor in neighbors:
                if self._grid.get_hex(next_neighbor) == 2 and (next_neighbor not in neighbors2):
                    if next_neighbor[1] == self._grid.get_size()-1:
                        self._winner = 2

                        countPlayer1 = 0
                        countPlayer2 = 0
                        for x in range(self._grid.get_size()):
                            for y in range(self._grid.get_size()):
                                if self._grid.get_hex([x, y]) == 1:
                                    countPlayer1 = countPlayer1 + 1
                                if self._grid.get_hex([x, y]) == 2:
                                    countPlayer2 = countPlayer2 + 1
                        print("player 1 total moves", countPlayer1)
                        print("player 2 total moves", countPlayer2)
                        print("Player 1 average time for each move:", self.player1TotalTime / countPlayer1)
                        print("Player 2 average time for each move:", self.player2TotalTime / countPlayer2)
                        return
                    else:
                        neighbors2.append(next_neighbor)



