import unittest
from fastapi.testclient import TestClient
from main import app, session, Game, Move, MoveRequest

class TestFastAPI(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def tearDown(self):
        session.rollback()

    def test_start_game(self):
        response = self.client.post("/start_game/")
        self.assertEqual(response.status_code, 200)
        game_id = response.json().get("game_id")
        self.assertIsNotNone(game_id)
        self.assertEqual(response.json().get("message"), "Game started")

    def test_move(self):
        # Start a new game
        response = self.client.post("/start_game/")
        self.assertEqual(response.status_code, 200)
        game_id = response.json().get("game_id")

        # Make a move
        move_request = MoveRequest(player="white", start=(6, 0), end=(4, 0), game_id=game_id)
        response = self.client.post("/move/", json=move_request.dict())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("message"), "Move made")
        self.assertEqual(response.json().get("current_player"), "black")

    def test_end_game(self):
        # Start a new game
        response = self.client.post("/start_game/")
        self.assertEqual(response.status_code, 200)
        game_id = response.json().get("game_id")

        # End the game
        response = self.client.post(f"/end_game/?game_id={game_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("message"), "Game ended")

    def test_get_board(self):
        # Start a new game
        response = self.client.post("/start_game/")
        self.assertEqual(response.status_code, 200)
        game_id = response.json().get("game_id")

        # Get the board
        response = self.client.get(f"/get_board/{game_id}")
        self.assertEqual(response.status_code, 200)
        board_state = response.json()
        self.assertTrue(len(board_state) > 0)

    def test_initial_board(self):
        response = self.client.get("/initial_board/")
        self.assertEqual(response.status_code, 200)
        initial_board = response.json()
        self.assertTrue(len(initial_board) > 0)


if __name__ == "__main__":
    unittest.main()
