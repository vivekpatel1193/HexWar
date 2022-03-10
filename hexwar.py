from Players.MinimaxPruning import MinimaxPlayer
from Players.MinimaxWithoutPruning import MinimaxWithoutPruning
from Players.NegMaxPlayerPruning import NegMaxPlayer
from Players.NegMaxWithoutPruning import NegMaxWithoutPruningPlayer
from Players.RandomPlayer import RandomPlayer
from controller import Controller
from gui import GUI

# player1 = MinimaxPlayer(9, 1, 2)
# player2 = RandomPlayer(9)


# with Alpha-beta pruning
player1 = MinimaxPlayer(7, 1, 2)
player2 = NegMaxPlayer(7,2,1)

# player1 = MinimaxWithoutPruning(7, 1, 2)
# player2 = NegMaxWithoutPruningPlayer(7,2,1)
#player2 = RandomPlayer(7)

controller = Controller(7, player1, player2)
gui = GUI(controller)



