import typing
from pyrsistent import PClass, field, pset_field, pvector, v, s

class Position(PClass):
    x = field(type=int)
    y = field(type=int)
    board_size = field(type=int)
    __invariant__ = lambda r: (Position.position_logic(r.x, r.y, r.board_size), 'x,y on board')

    def position_logic(x, y, board_size):
        return (x >= 0) &\
          (y >= 0) &\
          (x < board_size) &\
          (y < board_size)

class Game(PClass):
    black_positions = pset_field(Position)
    white_positions = pset_field(Position)


class OthelloGame():
    def __init__(self, board_size):
        self.board_size=6

    def initial_game(self) -> Game:
        lower = int(self.board_size/2) - 1
        upper = int(self.board_size/2)

        black_positions = s(Position(x=lower, y=lower, board_size=self.board_size),
            Position(x=upper, y=upper, board_size=self.board_size))
        white_positions = s(Position(x=lower, y=upper, board_size=self.board_size),
            Position(x=lower, y=lower, board_size=self.board_size))

        return Game(black_positions=black_positions, white_positions=white_positions)

    def new_position(self, x: int, y: int) -> Position:
        return Position(x=x, y=y, board_size=self.board_size)

    def get_neighbors(self, p):
        all_coordinates = [(x_offset + p.x, y_offset + p.y) for
            x_offset in range(-1, 2) for y_offset in range(-1, 2)
            if not x_offset == y_offset == 0]

        return [Position(x=x, y=y, board_size=self.board_size)
            for x, y in all_coordinates
            if Position.position_logic(x,y, self.board_size)]

    def possible_black_moves(self, game: Game):
        return None

    def perimeter_positions(self, game: Game):
        all_positions_set = pset(game.black_positions.union(game.white_positions))
        all_positions = plist(all_positions_set)

        horizon = s()
        while all_positions.length > 0:
            head = all_positions.first
            all_positions = all_positions.rest
            neighbors = self.get_neighbors(head)
            horizon = horizon.union(neighbors)

        return horizon.difference(all_positions_set)



