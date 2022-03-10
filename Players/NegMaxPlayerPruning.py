import numpy as np
from Players.Player import Player
from grid import Grid
import copy
import datetime
import math


class NegMaxPlayer(Player):
    def __init__(self, size, player_number, adv_number):
        super().__init__(size, player_number, adv_number)
        self.name = "Negmax"
        self._possible_moves = []
        self.node = Grid(size)
        self.store_average_action_time = []
        self.average_action_time = 0
        self.best_moves_player = []
        self.best_moves_opponent = []

    def step(self):
        """
        Calculate the best action to execute and execute it.
        :return: Action executed
        """
        start_time = datetime.datetime.now()
        best_move = self.node.free_moves()[0]
        best = -np.inf
        alpha = best
        for move in self.node.free_moves():
            new_node = copy.deepcopy(self.node)
            new_node.set_hex(self.player_number, move)
            value = -self.negMax(new_node, 2, -np.inf, -alpha, self.adv_number)
            if value > best:
                best = value
                best_move = move
            alpha = max(alpha, best)
        self.node.set_hex(self.player_number, best_move)
        return best_move

    def update(self, move_other_player):
        """
        Update the state of the problem with the action of the other player.
        :param move_other_player: Move played by the other player.
        """
        self.best_moves_opponent.append(move_other_player)
        self.node.set_hex(self.adv_number, move_other_player)

    def negMax(self, node, depth, alpha, beta, player):
        """
        Implement a simple version of NegMax with alpha-beta.
        :param node: Node to evaluate.
        :param depth: depth remaining.
        :param alpha: value of alpha.
        :param beta: value of beta.
        :return: The value of node.
        """

        turn = -1 if player == self.adv_number else 1
        if node.check_win(self.player_number):
            return np.inf * turn
        if node.check_win(self.adv_number):
            return -np.inf * turn
        if depth == 0:
            return self.heuristic_chase(node) * turn
        evaluation = -np.inf
        opponent = self.adv_number if player == self.player_number else self.player_number
        for move in node.free_moves():
            new_node = copy.deepcopy(node)
            new_node.set_hex(player, move)
            evaluation = max(evaluation, -self.negMax(new_node, depth - 1, -beta, -alpha, opponent))
            alpha = max(alpha, evaluation)
            if alpha >= beta:
                break

        return evaluation


    def manhattan(self, a, b):
        return sum(abs(val1 - val2) for val1, val2 in zip(a, b))

    def euclidean_distance(self, a, b):
        return math.sqrt(sum((val1 - val2) ** 2 for val1, val2 in zip(a, b)))

    def heuristic_chase(self, player):
        if (len(self.best_moves_opponent) == 0): return 0
        max = 0
        for i in self.best_moves_player:
            for j in self.best_moves_opponent:
                value = self.euclidean_distance(i, j)
                if value > max:
                    max = value
        return max

    def default_heuristic(self, node):
        """
        Heurisitic function. Be careful this heuristic is far from being good or optimized.
        :param node: Current node/state
        :return: Heuristic value
        """
        return self._value_player(node, self.player_number)

    def _value_player(self, node, player):
        """ Calculate the value of the node for the current player."""
        coordinates = []
        value = 0
        for x in range(node.get_size()):
            for y in range(node.get_size()):
                if ([x, y] not in coordinates) and (node.get_hex([x, y]) == player):
                    n = self._number_connected(player, [x, y], node)
                    coordinates += n[1]
                    if n[0] > value:
                        value = n[0]
        return value

    def _number_connected(self, player, coordinate, node):
        """
        Number of hex connected to a specific hex for a specific player
        :param player: Player
        :param coordinate: coordinate of the hex
        :param node: Node/state of the game
        :return: number of hex connected
        """
        neighbors = [coordinate]
        for neighbor in neighbors:
            n = node.neighbors(neighbor)
            for next_neighbor in n:
                if self.node.get_hex(next_neighbor) == player and (next_neighbor not in neighbors):
                    neighbors.append(next_neighbor)
        return len(neighbors), []

