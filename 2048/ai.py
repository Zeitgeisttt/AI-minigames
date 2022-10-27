from __future__ import absolute_import, division, print_function
import copy, random
from re import L
from game import Game

MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
MAX_PLAYER, CHANCE_PLAYER = 0, 1 

# Tree node. To be used to construct a game tree. 
class Node: 
    # Recommended: do not modify this __init__ function
    def __init__(self, state, player_type):
        self.state = (copy.deepcopy(state[0]), state[1])

        # to store a list of (direction, node) tuples
        self.children = []

        self.player_type = player_type

    # returns whether this is a terminal state (i.e., no children)
    def is_terminal(self):
        #TODO: complete this
        if len(self.children) == 0:
            return True
        else:
            return False


# AI agent. Determine the next move.
class AI:
    # Recommended: do not modify this __init__ function
    def __init__(self, root_state, search_depth=3): 
        self.root = Node(root_state, MAX_PLAYER)
        self.search_depth = search_depth
        self.simulator = Game(*root_state)

    # (Hint) Useful functions: 
    # self.simulator.current_state, self.simulator.set_state, self.simulator.move

    # current_state(self)      return (self.tile_matrix, self.score)
    # set_state(self, init_tile_matrix = None, init_score = 0)
    # move(self, direction)    return moved

    # TODO: build a game tree from the current node up to the given depth
    def build_tree(self, node = None, depth = 0):
        if depth == 0 or node == None:
            return
        else:
            if node.player_type == MAX_PLAYER:
                for i in range(4):
                    self.simulator.move(i)
                    newNode = Node(self.simulator.current_state(), CHANCE_PLAYER)
                    node.children.append(newNode)
                    self.build_tree(newNode, depth - 1)
                    self.simulator.undo()
            else:
                for i, j in self.simulator.get_open_tiles():
                    self.simulator.addToUndo()
                    self.simulator.tile_matrix[i][j] = 2
                    newNode = Node(self.simulator.current_state(), MAX_PLAYER)
                    node.children.append(newNode)
                    self.build_tree(newNode, depth - 1)
                    self.simulator.undo()

        

    # TODO: expectimax calculation.
    # Return a (best direction, expectimax value) tuple if node is a MAX_PLAYER
    # Return a (None, expectimax value) tuple if node is a CHANCE_PLAYER
    def expectimax(self, node = None):
        # TODO: delete this random choice but make sure the return type of the function is the same
        if node == None:
            raise Exception("Neither Max nor Chance player")
        elif node.is_terminal():
            # print("Terminal")
            return (None, node.state[1])
        elif node.player_type == MAX_PLAYER:
            # print("Max")
            value = float('-inf')
            direction = 0
            for i in range(len(node.children)):
                moved = self.simulator.move(i)
                if (moved == False):
                    self.simulator.undo()
                    continue
                else:
                    self.simulator.undo()
                
                childValue = self.expectimax(node.children[i])[1]
                if value < childValue:
                    value = childValue
                    direction = i
            return (direction, value)
        elif node.player_type == CHANCE_PLAYER:
            # print("Chance")
            value = 0.0
            for n in node.children:
                value += float(self.expectimax(n)[1]) / len(node.children)
            return (None, value)
        else:
            raise Exception("Neither Max nor Chance player")


    # Return decision at the root
    def compute_decision(self):
        self.build_tree(self.root, self.search_depth)
        direction, _ = self.expectimax(self.root)
        # print (MOVES[direction])
        return direction

    # TODO (optional): implement method for extra credits
    def compute_decision_ec(self):
        self.ec_build_tree(self.root, 5)
        direction, _ = self.ec_expectimax(self.root)
        return direction



    def ec_build_tree(self, node = None, depth = 0):
        if depth == 0 or node == None:
            return
        else:
            if node.player_type == MAX_PLAYER:
                for i in range(4):
                    self.simulator.move(i)
                    newNode = Node(self.simulator.current_state(), CHANCE_PLAYER)
                    node.children.append(newNode)
                    self.ec_build_tree(newNode, depth - 1)
                    self.simulator.undo()
            else:
                openTiles = [[0 for i in range(self.simulator.board_size)] for j in range(self.simulator.board_size)]
                for i, j in self.simulator.get_open_tiles():
                    openTiles[i][j] = 1
                


                keptTiles = []
                evaluated = 2
                for i in range(self.simulator.board_size):
                    if len(keptTiles) >= evaluated:
                        break

                    if (i % 2 == 0):
                        for j in range(self.simulator.board_size):
                            if len(keptTiles) >= evaluated:
                                break
                            else:
                                if openTiles[i][j] == 1:
                                    keptTiles.append((i, j))
                    else:
                        for j in range(self.simulator.board_size):
                            if len(keptTiles) >= evaluated:
                                break
                            else:
                                if openTiles[i][3-j] == 1:
                                    keptTiles.append((i, 3-j))


                for i, j in keptTiles:
                    self.simulator.addToUndo()
                    self.simulator.tile_matrix[i][j] = 2
                    newNode = Node(self.simulator.current_state(), MAX_PLAYER)
                    node.children.append(newNode)
                    self.ec_build_tree(newNode, depth - 1)
                    self.simulator.undo()

    def heuristic_value(self, board):
        # print(board)
        value = 0
        for i in range(self.simulator.board_size):
            if (i % 2 == 0):
                for j in range(self.simulator.board_size):
                    value += board[i][j] * (4**((self.simulator.board_size**2 - 1) - self.simulator.board_size*i - j))
            else:
                for j in range(self.simulator.board_size):
                    value += board[i][j] * (4**((self.simulator.board_size**2 - 1) - self.simulator.board_size*i - (self.simulator.board_size - 1 - j)))
        return value

    def ec_expectimax(self, node = None):
        if node == None:
            raise Exception("Neither Max nor Chance player")
        elif node.is_terminal():
            value = self.heuristic_value(node.state[0])
            return (None, value)
        elif node.player_type == MAX_PLAYER:
            # print("Max")
            value = float('-inf')
            direction = 0
            for i in range(len(node.children)):
                moved = self.simulator.move(i)
                if (moved == False):
                    self.simulator.undo()
                    continue
                else:
                    self.simulator.undo()
                
                childValue = self.ec_expectimax(node.children[i])[1]
                if value < childValue:
                    value = childValue
                    direction = i
            return (direction, value)
        elif node.player_type == CHANCE_PLAYER:
            # print("Chance")
            value = 0.0
            for n in node.children:
                value += float(self.ec_expectimax(n)[1]) / len(node.children)
            return (None, value)
        else:
            raise Exception("Neither Max nor Chance player")