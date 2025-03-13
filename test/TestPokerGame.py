import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from unittest.mock import patch
from io import StringIO
from core.poker_game import PokerGame
from core.player import Player

class TestPokerGame(unittest.TestCase):

    def test_game_consistency(self):
        """ 运行 1000 次游戏，并检查筹码总和是否始终为 2000 """
        with patch('sys.stdout', new=StringIO()):
            for _ in range(1000):
                players = [Player(name=1, chips=1000), Player(name=2, chips=1000)]
                game = PokerGame(players)
                game.start_game()

                while game.game_state.current_betting_round < 4:
                    game.play_round()
                    if game.game_state.current_betting_round < 4:
                        game.next_phase()
                
                game.determine_winner()

                total_chips = sum(player.chips for player in players)
                self.assertEqual(total_chips, 2000, f"Total chips mismatch! Found: {total_chips}")

if __name__ == "__main__":
    unittest.main()