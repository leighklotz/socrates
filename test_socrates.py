import contextlib
import io
import unittest
from unittest.mock import patch

import socrates as game


class MemoryTests(unittest.TestCase):
    def setUp(self):
        self.memory = game.Memory()
        self.memory.start()

    def test_replay_then_deal_without_replaying_new_cards(self):
        self.memory.stack = [0, 1, 2, 3, 0, 1, 2]
        with contextlib.redirect_stdout(io.StringIO()), \
                patch.object(game.deck, "deal", side_effect=[2, 3]) as deal:
            self.memory.replay()
            self.assertEqual([self.memory.pick() for _ in range(4)], [0, 1, 2, 3])
        self.assertEqual(deal.call_count, 2)
        self.assertEqual(self.memory.stack, [0, 1, 2, 3])
        self.assertIsNone(self.memory.point)

    def test_empty_replay_deals_normally(self):
        with contextlib.redirect_stdout(io.StringIO()), \
                patch.object(game.deck, "deal", side_effect=[0, 1]) as deal:
            self.memory.replay()
            self.assertEqual([self.memory.pick() for _ in range(2)], [0, 1])
        self.assertEqual(deal.call_count, 2)
        self.assertIsNone(self.memory.point)

    def test_stack_display_uses_direction_labels_and_split(self):
        self.memory.stack = [0, 1, 2, 3]
        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch.object(game.deck, "deal", return_value=None):
            self.memory.pick()
        self.assertIn("stack DLRU \n", output.getvalue())

        self.memory.point = 0
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.memory.pick()
        self.assertIn("stack D LRU\n", output.getvalue())


class BoardTests(unittest.TestCase):
    def test_hound_capture_prevents_socrates_from_moving(self):
        game.deck.start()
        game.memory.start()
        board = game.Board()

        def capture():
            game.hound.position = game.socrates.position[:]

        def finish():
            game.deck.cards = [0, 0, 0, 0]

        with contextlib.redirect_stdout(io.StringIO()), \
                patch.object(board, "show"), patch.object(board, "clear"), \
                patch.object(board, "pause"), patch.object(board, "long_pause"), \
                patch.object(game.hound, "turn", side_effect=capture), \
                patch.object(game.socrates, "turn") as turn, \
                patch.object(game.memory, "replay", side_effect=finish) as replay:
            board.play()
        turn.assert_not_called()
        replay.assert_called_once()

    def test_overlapping_players_render_as_one_cell(self):
        board = game.Board()
        game.socrates.position = [4, 4]
        game.hound.position = [4, 4]
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            board.show()
        rows = output.getvalue().splitlines()[1:]
        self.assertEqual(len(rows), board.YMAX)
        self.assertTrue(all(len(row) == board.XMAX for row in rows))
        self.assertEqual(rows[4], "....X....")


if __name__ == "__main__":
    unittest.main()
