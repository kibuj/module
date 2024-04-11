import unittest
from Logic import Board, King, Rook, Knight, Bishop, Queen, Pawn


class TestChessLogic(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_initial_board_setup(self):
        # Test initial setup of the board
        expected = [
            [Rook("black"), Knight("black"), Bishop("black"), Queen("black"), King("black"), Bishop("black"),
             Knight("black"), Rook("black")],
            [Pawn("black")] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [Pawn("white")] * 8,
            [Rook("white"), Knight("white"), Bishop("white"), Queen("white"), King("white"), Bishop("white"),
             Knight("white"), Rook("white")],
        ]
        self.assertEqual(self.board.board, expected)

    def test_valid_move_king(self):
        # Test valid moves for king
        self.assertTrue(King("white").valid_move((0, 4), (1, 4), self.board.board))
        self.assertFalse(King("white").valid_move((0, 4), (2, 4), self.board.board))

    def test_valid_move_rook(self):
        # Test valid moves for rook
        self.assertTrue(Rook("white").valid_move((7, 0), (7, 3), self.board.board))
        self.assertFalse(Rook("white").valid_move((7, 0), (6, 0), self.board.board))

    def test_valid_move_knight(self):
        # Test valid moves for knight
        self.assertTrue(Knight("white").valid_move((7, 1), (5, 2), self.board.board))
        self.assertFalse(Knight("white").valid_move((7, 1), (6, 1), self.board.board))

    def test_valid_move_bishop(self):
        # Test valid moves for bishop
        self.assertTrue(Bishop("white").valid_move((7, 2), (5, 0), self.board.board))
        self.assertFalse(Bishop("white").valid_move((7, 2), (6, 3), self.board.board))

    def test_valid_move_queen(self):
        # Test valid moves for queen
        self.assertTrue(Queen("white").valid_move((7, 3), (4, 0), self.board.board))
        self.assertTrue(Queen("white").valid_move((7, 3), (7, 5), self.board.board))

    def test_valid_move_pawn(self):
        # Test valid moves for pawn
        self.assertTrue(Pawn("white").valid_move((6, 0), (5, 0), self.board.board))
        self.assertFalse(Pawn("white").valid_move((6, 0), (4, 0), self.board.board))

    def test_invalid_move(self):
        # Test invalid move
        self.assertFalse(self.board.is_valid_move((7, 0), (5, 0)))
        self.assertFalse(self.board.is_valid_move((0, 0), (2, 0)))

    def test_move_piece(self):
        # Test moving a piece
        self.board.move_piece((1, 0), (3, 0))
        self.assertIsNone(self.board.board[1][0])
        self.assertIsNotNone(self.board.board[3][0])


if __name__ == "__main__":
    unittest.main()
