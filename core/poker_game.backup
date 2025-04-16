from core.deck import Deck
from core.game_state import GameState
from core.hand_evaluator import HandEvaluator

class PokerGame:
    SMALL_BLIND = 5
    BIG_BLIND = 10

    def __init__(self, players):
        self.players = players  
        self.deck = Deck()  
        self.game_state = GameState(players)  
        self.deck.shuffle()

    def start_game(self):
        self.game_state.reset_game_state()
        self.deck = Deck()
        self.deck.shuffle()
        
        self.players[0].reset_hand()
        self.players[1].reset_hand()

        # 每次开局交换两位玩家的位置，小盲（dealer）为index0
        self.players = self.players[::-1]

        # 设置小盲（SB）和大盲（BB）和下注操作
        sb,bb = self.players[0], self.players[1]
        sb.bet(self.SMALL_BLIND)
        bb.bet(self.BIG_BLIND)
        self.game_state.add_to_pot(self.SMALL_BLIND + self.BIG_BLIND)

        print(f"Dealer this round: Player {sb.name}")
        print(f'{sb.name}: {sb.chips},{bb.name}: {bb.chips},pot:{self.game_state.pot}')

        for player in self.players:
            player.receive_cards(self.deck.draw(2))

        # self.game_state.next_round()
    
    def play_round(self):

        print(f"=== current state: {self.game_state.ROUNDS[self.game_state.current_betting_round]} ===")

        for player in self.players:
            hand_str = ", ".join(str(card) for card in player.hand)
            print(f"Player {player.name} card: {hand_str} (Chips {player.chips})")
        community_cards_str = ", ".join(str(card) for card in self.game_state.community_cards)
        print(f"Community Cards: {community_cards_str if community_cards_str else 'None'}")
        
        # 在Preflop阶段，应该是小盲先行动
        # 其他阶段是大盲先行动
        if self.game_state.current_betting_round == 0:
            player_list = self.players
        else:
            player_list = self.players[::-1]


        # fold 弃牌，游戏结束
        # raise 提高筹码，在这个模型中，限制每轮最多只有一次raise
        # call 将筹码提升到和对方一样，每轮第一个人call就相当于是check（此时双方筹码已经一致）
        for player in player_list:
            if player.is_active:

                decision = player.make_decision(self.game_state)
                print(f'{player.name} choose to {decision}')
                if decision == "fold":
                    player.fold()
                    break # 防止两人同时fold
                elif decision == "call":
                    bets = [p.current_bet for p in player_list]
                    if player.current_bet != bets[0]:
                        diff = bets[0]-player.current_bet
                    else:
                        diff = bets[1]-player.current_bet
                    self.game_state.add_to_pot(diff)
                    player.bet(diff)
                    print(f'{player.name}\'s chip: {player.chips},current_bet :{player.current_bet}')
                    break # 这里应该分类讨论，如果是第一个call,那其实可以继续的；如果是对手raise后的call,则直接结束
                elif decision == "raise":
                    self.game_state.add_to_pot(self.BIG_BLIND)
                    player.bet(self.BIG_BLIND)
                    print(f'{player.name}\'s chip: {player.chips},current_bet :{player.current_bet}')
                    
                    # print(f'-------pot:{self.game_state.pot}-------')
        print(f'pot:{self.game_state.pot}')


    def next_phase(self):
        active_players = [p for p in self.players if p.is_active]
        if len(active_players) == 1: 
            print(f"Player{active_players[0].name} win, all other player fold!")
            self.game_state.current_betting_round = 4
            next_phase_name = "SHOWDOWN"
            return
    
        if self.game_state.current_betting_round == 0:
            self.game_state.deal_community_cards(self.deck, 3)  # Flop
        elif self.game_state.current_betting_round in [1, 2]:
            self.game_state.deal_community_cards(self.deck, 1)  # Turn or River

        if self.game_state.current_betting_round < 3:
            next_phase_name = self.game_state.ROUNDS[self.game_state.current_betting_round + 1]
        else:
            next_phase_name = "SHOWDOWN"
        print(f"Moving to next phase: {next_phase_name}")        

        self.game_state.next_round()
    
    def determine_winner(self):
        active_players = [p for p in self.players if p.is_active]
        if len(active_players) == 1:
            print(f"Player{active_players[0].name} win, all other player fold!")     
            active_players[0].chips += self.game_state.pot
            return active_players[0].name
    
        best_player = None
        best_hand_value = -1

        for player in self.players:
            if player.is_active:
                hand_value = HandEvaluator.evaluate_hand(player.hand, self.game_state.community_cards)
                if hand_value > best_hand_value:
                    best_hand_value = hand_value
                    best_player = player
        
        if best_player:
            best_player.chips += self.game_state.pot 

        type = {
        1:"High Card",
        2:"One Pair",
        3:"Two Pair",
        4:"Three of a Kind",
        5:"Straight",
        6:"Flush",
        7:"Full House",
        8:"Four of a Kind",
        9:"Straight Flush",
        10:"Royal Flush"
        } 
        print(f'{best_player.name} wins with {type[best_hand_value]}')
        return best_player.name
    
    def reset_game(self):
        self.start_game()