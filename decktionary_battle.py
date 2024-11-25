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

    

game = DecktionaryBattle()
print("Shuffled Deck: ", game.deck)
game.deal_cards()