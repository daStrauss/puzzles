import unittest
from game import Position, OthelloGame
from pyrsistent import InvariantException

class PositionTestCase(unittest.TestCase):
    def test_asserts(self):
        self.assertTrue(Position.position_logic(1, 2, 5))
        self.assertFalse(Position.position_logic(48, 2, 6))
        self.assertTrue(Position.position_logic(2, 3, 66))

    def test_initialization(self):
        with self.assertRaises(InvariantException):
            Position(x_position=47, y_position=1, board_size=6)

class GameTestCase(unittest.TestCase):
    def test_get_neighbors(self):
        game = OthelloGame(board_size=6)
        a_position = game.new_position(2,2)

        neighbors = set(game.get_neighbors(a_position))
        valid_neighbors = [
            (1,1),
            (1,2),
            (1,3),
            (2,1),
            (2,3),
            (3,1),
            (3,2),
            (3,3)]

        true_neighbors = set([Position(x_position=x, y_position=y, board_size=6)
            for x, y in valid_neighbors])

        self.assertEqual(neighbors, true_neighbors)

    def test_corner_neighbors(self):
        game = OthelloGame(board_size=6)
        a_position = game.new_position(5,5)
        neighbors = set(game.get_neighbors(a_position))

        valid_neighbors = [(5, 4), (4, 4), (4, 5)]
        true_neighbors = set([Position(x_position=x, y_position=y, board_size=6)
            for x, y in valid_neighbors])

        self.assertEqual(neighbors, true_neighbors)


class OthelloTestCase(unittest.TestCase):
    def test_empties(self):
        othelloGame = OthelloGame(board_size=6)
        initial = othelloGame.initial_game()
        perimeter = othelloGame.perimeter_positions(initial)
        border = [
            (1,1), (1,2),(1,3), (1,4),
            (2,1), (2,4),
            (3,1), (3,4),
            (4,1), (4,2), (4,3), (4,4)]
        border_positions = set([Position(x_position=x, y_position=y, board_size=6)
            for x, y in border])

        self.assertEqual(border_positions, set(perimeter))

    def test_search(self):
        othelloGame = OthelloGame(board_size=6)
        initial = othelloGame.initial_game()
        start_pos = othelloGame.new_position(4, 4)
        searchd = othelloGame.search_list(start_pos, (-1, -1), initial)
        print(searchd)
        self.assertTrue(True)
