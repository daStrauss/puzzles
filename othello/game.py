import typing
from pyrsistent import PClass, field, pset_field, pset, s, plist, InvariantException

class Position(PClass):
    x_position = field(type=int)
    y_position = field(type=int)
    board_size = field(type=int)
    __invariant__ = lambda r: (Position.position_logic(
        r.x_position,
        r.y_position,
        r.board_size), 'x,y on board')

    def position_logic(x_pos, y_pos, board_size):
        return (x_pos >= 0) &\
          (y_pos >= 0) &\
          (x_pos < board_size) &\
          (y_pos < board_size)

class Game(PClass):
    black_positions = pset_field(Position)
    white_positions = pset_field(Position)


class OthelloGame():
    def __init__(self, board_size):
        self.board_size = board_size

    def initial_game(self) -> Game:
        lower = int(self.board_size/2) - 1
        upper = int(self.board_size/2)

        black_positions = s(
            Position(x_position=lower, y_position=lower, board_size=self.board_size),
            Position(x_position=upper, y_position=upper, board_size=self.board_size))

        white_positions = s(
            Position(x_position=lower, y_position=upper, board_size=self.board_size),
            Position(x_position=upper, y_position=lower, board_size=self.board_size))

        return Game(black_positions=black_positions, white_positions=white_positions)

    def new_position(self, x_position: int, y_position: int) -> Position:
        return Position(x_position=x_position, y_position=y_position, board_size=self.board_size)

    def get_neighbors(self, position):
        all_coordinates = [(x_offset + position.x_position, y_offset + position.y_position) for
                           x_offset in range(-1, 2) for y_offset in range(-1, 2)
                           if not x_offset == y_offset == 0]

        return [Position(x_position=x, y_position=y, board_size=self.board_size)
                for x, y in all_coordinates
                if Position.position_logic(x, y, self.board_size)]

    def perimeter_positions(self, game: Game):
        all_positions_set = pset(game.black_positions.union(game.white_positions))
        all_positions = plist(all_positions_set)

        horizon = s()
        while len(all_positions) > 0:
            head = all_positions.first
            all_positions = all_positions.rest
            neighbors = self.get_neighbors(head)
            horizon = horizon.union(neighbors)

        return horizon.difference(all_positions_set)

    def is_valid_black_move(self, position: Position, game: Game):
        drs = [(1,0), (0,1), (1,1), (-1, 1), (-1, -1), (1, -1), (-1,0), (0, -1)]
        return None
        

    def search_list(self, position: Position, direction, game):
        on_board = True
        offset = 1
        values = []
        x, y = direction
        while on_board:
            try:
                testPosition = Position(
                    x_position=position.x_position+offset*x,
                    y_position=position.y_position+offset*y,
                    board_size=position.board_size)

                if testPosition in game.white_positions:
                    values.append("white")
                elif testPosition in game.black_positions:
                    values.append("black")
                else:
                    values.append(None)
                offset += 1
            except InvariantException:
                on_board = False

        return values



