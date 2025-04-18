# # import math
# # import random
# # from copy import deepcopy
# # from core.card import Card
# # from core.hand_evaluator import HandEvaluator
# # from core.player import Player
# # from players.rule_based import RuleBased
# # from core.poker_game import PokerGame

# # ACTIONS = ["fold", "call", "raise"]

# # class Node:
# #     def __init__(self, raise_thres, call_thres, parent=None):
# #         self.raise_thres = raise_thres
# #         self.call_thres = call_thres
# #         self.parent = parent
# #         self.children = []
# #         self.visits = 0
# #         self.total_reward = 0

# #     def is_fully_expanded(self):
# #         return len(self.children) == 0  # All combinations pre-generated

# #     def uct(self, total_simulations, c=1.4):
# #         if self.visits == 0:
# #             return float('inf')
# #         avg_reward = self.total_reward / self.visits
# #         return avg_reward + c * math.sqrt(math.log(total_simulations) / self.visits)


# # class MCTSPlayer(Player):
# #     def __init__(self, name, chips, simulations=100):
# #         super().__init__(name, chips)
# #         self.simulations = simulations
# #         self.raise_call_thresholds = [
# #             (0.7, 0.1), (0.75, 0.2), (0.8, 0.2), (0.85, 0.2), (0.9, 0.2)
# #         ]

# #     def make_decision(self, game_state):
# #         if game_state.current_betting_round <= 1:
# #             return "call"

# #         root_nodes = [Node(rt, ct) for rt, ct in self.raise_call_thresholds]
# #         total_simulations = 0

# #         for _ in range(self.simulations):
# #             total_simulations += 1
# #             node = max(root_nodes, key=lambda n: n.uct(total_simulations))
# #             reward = self._simulate_strategy(node.raise_thres, node.call_thres)
# #             node.visits += 1
# #             node.total_reward += reward

# #         best = max(root_nodes, key=lambda n: n.total_reward / n.visits)
# #         win_rate = self._estimate_win_rate(game_state)

# #         if win_rate > best.raise_thres:
# #             return "raise"
# #         elif win_rate > best.call_thres:
# #             return "call"
# #         else:
# #             return "fold"

# #     def _estimate_win_rate(self, game_state, simulations=300):
# #         deck = [Card(suit, rank) for suit in Card.SUITS for rank in Card.RANKS]
# #         for card in self.hand + game_state.community_cards:
# #             deck.remove(card)

# #         wins = ties = 0
# #         for _ in range(simulations):
# #             random.shuffle(deck)
# #             opp_hand = deck[:2]
# #             needed = 5 - len(game_state.community_cards)
# #             full_community = game_state.community_cards + deck[2:2+needed]

# #             my_score = HandEvaluator.evaluate_hand(self.hand, full_community)
# #             opp_score = HandEvaluator.evaluate_hand(opp_hand, full_community)

# #             if my_score > opp_score:
# #                 wins += 1
# #             elif my_score == opp_score:
# #                 ties += 1

# #         return (wins + 0.5 * ties) / simulations

# #     def _simulate_strategy(self, raise_thres, call_thres):
# #         player1 = SimpleThresholdPlayer("TMP", 1000, raise_thres, call_thres)
# #         player2 = RuleBased("RB", 1000)
# #         game = PokerGame([player1, player2])
# #         game.start_game()
# #         while game.game_state.current_betting_round < 4:
# #             game.play_round()
# #             if game.game_state.current_betting_round < 4:
# #                 game.next_phase()
# #         winner = game.determine_winner()
# #         profit = player1.chips - 1000
# #         return profit


# # class SimpleThresholdPlayer(Player):
# #     def __init__(self, name, chips, raise_thres, call_thres):
# #         super().__init__(name, chips)
# #         self.raise_thres = raise_thres
# #         self.call_thres = call_thres

# #     def make_decision(self, game_state):
# #         if game_state.current_betting_round <= 1:
# #             return "call"

# #         win_rate = self._estimate_win_rate(game_state)
# #         if win_rate > self.raise_thres:
# #             return "raise"
# #         elif win_rate > self.call_thres:
# #             return "call"
# #         else:
# #             return "fold"

# #     def _estimate_win_rate(self, game_state, simulations=100):
# #         deck = [Card(suit, rank) for suit in Card.SUITS for rank in Card.RANKS]
# #         for card in self.hand + game_state.community_cards:
# #             deck.remove(card)

# #         wins = ties = 0
# #         for _ in range(simulations):
# #             random.shuffle(deck)
# #             opp_hand = deck[:2]
# #             needed = 5 - len(game_state.community_cards)
# #             full_community = game_state.community_cards + deck[2:2+needed]

# #             my_score = HandEvaluator.evaluate_hand(self.hand, full_community)
# #             opp_score = HandEvaluator.evaluate_hand(opp_hand, full_community)

# #             if my_score > opp_score:
# #                 wins += 1
# #             elif my_score == opp_score:
# #                 ties += 1

# #         return (wins + 0.5 * ties) / simulations


# import random
# from core.player import Player
# from core.card import Card
# from core.hand_evaluator import HandEvaluator
# from players.rule_based import RuleBased
# from copy import deepcopy
# import math

# class Node:
#     def __init__(self, parent=None, action=None):
#         self.parent = parent
#         self.action = action
#         self.children = []
#         self.visits = 0
#         self.total_reward = 0.0

#     def is_fully_expanded(self):
#         return len(self.children) == len(["fold", "call", "raise"])

#     def best_child(self, c_param=1.41):
#         return max(self.children, key=lambda child: child.total_reward / child.visits + 
#                    c_param * math.sqrt(math.log(self.visits) / child.visits))

#     def expand(self):
#         tried_actions = [child.action for child in self.children]
#         for action in ["fold", "call", "raise"]:
#             if action not in tried_actions:
#                 new_node = Node(parent=self, action=action)
#                 self.children.append(new_node)
#                 return new_node
#         raise Exception("No more actions to expand")

# class MCTSPlayer(Player):
#     def __init__(self, name, chips, num_simulations=1000):
#         super().__init__(name, chips)
#         self.num_simulations = num_simulations

#     def make_decision(self, game_state):
#         if game_state.current_betting_round <= 1:
#             return "call"

#         root = Node()

#         for _ in range(self.num_simulations):
#             node = self._select(root)
#             reward = self._simulate(node.action, game_state)
#             self._backpropagate(node, reward)

#         best = max(root.children, key=lambda c: c.visits)
#         return best.action

#     def _select(self, node):
#         while node.is_fully_expanded() and node.children:
#             node = node.best_child()
#         if not node.is_fully_expanded():
#             return node.expand()
#         return node

#     def _simulate(self, action, game_state):

#         from core.poker_game import PokerGame

#         start_chips = 1000
#         my_clone = RuleBased(self.name, start_chips)
#         oppo = RuleBased("opponent", start_chips)

#         if action == "fold":
#             return -my_clone.current_bet
        
#         my_clone.hand = deepcopy(self.hand)
#         used_cards = game_state.community_cards + my_clone.hand
#         full_deck = [Card(suit, rank) for rank in Card.RANKS for suit in Card.SUITS]
#         remain_deck = [c for c in full_deck if c not in used_cards]

#         random.shuffle(remain_deck)
#         oppo.receive_cards([remain_deck.pop(), remain_deck.pop()])

#         players = [my_clone, oppo]
#         game = PokerGame(players)
#         game.game_state.community_cards = deepcopy(game_state.community_cards)


#         while game.game_state.current_betting_round < 4:
#             game.play_round()
#             if game.game_state.current_betting_round < 4:
#                 game.next_phase()

#         game.determine_winner()

#         profit = my_clone.chips - start_chips
#         return profit

#     def _backpropagate(self, node, reward):
#         while node is not None:
#             node.visits += 1
#             node.total_reward += reward
#             node = node.parent


import random
from core.player import Player
from core.card import Card
from core.hand_evaluator import HandEvaluator
from players.rule_based import RuleBased
from copy import deepcopy
from core.poker_game import PokerGame
from core.game_state import GameState

class MCTSPlayer(Player):
    action_paths_2 = [
        ["fold"],
        ["call","fold"],
        ["call","call"],
        ["call","raise"],
        ["raise","fold"],
        ["raise","call"],
        ["raise","raise"],
    ]
    action_paths_3 = [
        ["fold"],
        ["call"],
        ["raise"]
    ]
    def make_decision(self, game_state, simulations=500):
        if game_state.current_betting_round <= 1:
            return "call"
        elif game_state.current_betting_round == 2:
            action_paths = self.action_paths_2
        elif game_state.current_betting_round == 3:
            action_paths = self.action_paths_3
        else:
            raise Exception("decision shouldn't reach here, current_betting_round > 3")

        best_action = "fold"
        best_avg_reward = float("-inf")

        for path in action_paths:
            total_reward = 0
            for _ in range(simulations):
                reward = self._simulate_first_action(path, game_state)
                total_reward += reward
            avg_reward = total_reward / simulations

            if avg_reward > best_avg_reward:
                best_avg_reward = avg_reward
                best_action = path[0]

        return best_action

    def _am_i_first(self, game_state):
        players = game_state.players
        my_index = 0 if players[0].name == self.name else 1

        if game_state.current_betting_round == 0:
            return my_index == 0  # Preflop：小盲先
        else:
            return my_index == 1  # Flop+：大盲先
        
            
    def _simulate_first_action(self, path, game_state):
        from core.hand_evaluator import HandEvaluator
        players = game_state.players

        is_first = self._am_i_first(game_state)
        round_now = game_state.current_betting_round
        path_iter = iter(path)

        # 初始化底池和发对手手牌
        pot = game_state.pot
        my_stack, oppo_stack = 1000, 1000
        used = self.hand + game_state.community_cards
        full_deck = [Card(s, r) for s in Card.SUITS for r in Card.RANKS]
        remain_deck = [c for c in full_deck if c not in used]
        random.shuffle(remain_deck)
        oppo_hand = [remain_deck.pop(), remain_deck.pop()]

        board = game_state.community_cards + [remain_deck.pop() for _ in range(4 - len(game_state.community_cards))]
        if round_now == 3:
            board = game_state.community_cards + [remain_deck.pop() for _ in range(5 - len(game_state.community_cards))]

        if is_first:
            my_bet = players[0].current_bet
            oppo_bet = players[1].current_bet
        else:
            my_bet = players[1].current_bet
            oppo_bet = players[0].current_bet


        # my_bet = 0
        # oppo_bet = 0

        def act(player, action):
            nonlocal pot, my_stack, oppo_stack, my_bet, oppo_bet

            if action == "fold":
                return "fold"

            if player == "me":
                current_bet = my_bet
                opponent_bet = oppo_bet
                stack = my_stack
            else:
                current_bet = oppo_bet
                opponent_bet = my_bet
                stack = oppo_stack

            if action == "call":
                diff = abs(opponent_bet - current_bet)
            elif action == "raise":
                diff = 10
            else:
                diff = 0

            stack -= diff
            pot += diff

            # 更新下注额
            if player == "me":
                my_stack = stack
                my_bet += diff
            else:
                oppo_stack = stack
                oppo_bet += diff

            return "ok"


        def simulate_oppo(oppo_hand, board, round_num):
            if round_num < 3:
                return "call"
            
            val = HandEvaluator.evaluate_hand(oppo_hand, board)
            if val == 1:
                return "fold"
            elif val <= 3:
                return "call"
            else:
                return "raise"

        # ============================= simulation =============================
        try:
            if is_first:
                if round_now == 2:
                    # state2
                    a1 = next(path_iter, "call")
                    if act("me", a1) == "fold": return -pot
                    if act("oppo", simulate_oppo(oppo_hand, board, round_now)) == "fold": return pot
                    # state3
                    a2 = next(path_iter, "call")
                    if act("me", a2) == "fold": return -pot
                    if act("oppo", simulate_oppo(oppo_hand, board, round_now)) == "fold": return pot

                elif round_now == 3:
                    # state3
                    a1 = next(path_iter, "call")
                    if act("me", a1) == "fold": return -pot
                    if act("oppo", simulate_oppo(oppo_hand, board, round_now)) == "fold": return pot

            else:
                if round_now == 2:
                    a1 = next(path_iter, "call")
                    if act("me", a1) == "fold": return -pot
                    # state3
                    if act("oppo", simulate_oppo(oppo_hand, board, round_now)) == "fold": return pot
                    a2 = next(path_iter, "call")
                    if act("me", a2) == "fold": return -pot

                elif round_now == 3:
                    a1 = next(path_iter, "call")
                    if act("me", a1) == "fold": return -pot

            # showdown
            my_score = HandEvaluator.evaluate_hand(self.hand, board)
            oppo_score = HandEvaluator.evaluate_hand(oppo_hand, board)
            if my_score > oppo_score:
                return pot
            elif my_score < oppo_score:
                return -pot
            else:
                return 0

        except StopIteration:
            print("StopIterationStopIterationStopIteration")
            return -10 


