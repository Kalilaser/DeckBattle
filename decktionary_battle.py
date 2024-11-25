import random

class DecktionaryBattle:
    def __init__(self):
        self.deck = self.create_deck()

    def create_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = list(range(2,15)) # 2 to Ace (Ace = 14)
        deck = [(rank, suit) for suit in suits for rank in ranks if rank != 13] # This removes the kings
        random.shuffle(deck)
        return deck
    
    def deal_cards(self):
        self.player1_hand = [self.deck.pop() for _ in range(8)]
        self.player2_hand = [self.deck.pop() for _ in range(8)]
        print("Player 1 Hand:", self.player1_hand)
        print("Player 2 Hand:", self.player2_hand)

    def lead_round(self, player1_card, player2_card):
        lead_suit = player1_card[1]
        print(f"Player 1 plays: {player1_card}, Player 2 plays: {player2_card}")
        print(f"Lead suit: {lead_suit}")
       
        if player2_card[1] == lead_suit:
            winner = 1 if player1_card[0] > player2_card[0] else 2
            print(f"Both players followed the suit. Winner: Player {winner}")
        
        else:
            winner = 1
            print(f"Player 2 did not follow suit. Winner: Player 1")
        
        if winner == 1:
            print("Player 1 wins this round!")
        else:
            print("Player 2 wins this round!")
    

game = DecktionaryBattle()
game.deal_cards()
game.lead_round(game.player1_hand[0], game.player2_hand[0])