import random

class DecktionaryBattle:
    def __init__(self):
        self.deck = self.create_deck()
        self.revealed_cards = []
        self.player1_score = 0
        self.player2_score = 0

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

    def lead_round(self, leader, follower):
        if leader == 1:
            player1_card = self.choose_card(self.player1_hand, 1)
            player2_card = self.choose_card(self.player2_hand, 2)
        else:
            player2_card = self.choose_card(self.player2_hand, 2)
            player1_card = self.choose_card(self.player1_hand, 1)

        lead_suit = player1_card[1] if leader == 1 else player2_card[1]

        print(f"Player 1 plays: {player1_card}, Player 2 plays: {player2_card}")
        print(f"Lead suit: {lead_suit}")
       
        if follower == 2 and player2_card[1] != lead_suit and any(card[1] == lead_suit for card in self.player2_hand):
            print("Player 2 broke the rules by not following suit!")
            winner = 1
        elif follower == 1 and player1_card[1] != lead_suit and any(card[1] == lead_suit for card in self.player1_hand):
            print("Player 2 broke the rules by not following suit!")
            winner = 2
            
        else:   
            
            if (player2_card[1] == lead_suit and leader == 1) or (player1_card[1] == lead_suit and leader == 2)
                winner = 1 if player1_card[0] > player2_card[0] else 2
                print(f"Both players followed the suit. Winner: Player {winner}")
            else:
                winner = leader
                print(f"Player 2 did not follow suit. Winner: Player 1")
        
        if winner == 1:
            self.player1_score += 1
            print("Player 1 wins this round!")
        else:
            self.player2_score += 1
            print("Player 2 wins this round!")
        
        self.revealed_cards.append(self.deck.pop())
        print("Revealed Card:", self.revealed_cards[-1])
        return winner
    
    def choose_card(self, player_hand, player_num):
        print(f"Player {player_num}'s turn. Your hand: {player_hand}")
        while True:
            try:
                choice = int(input(f"Player {player_num}, choose a card to play (0-{len(player_hand)-1}): "))
                if 0 <= choice < len(player_hand):
                    return player_hand.pop(choice)
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def play_game(self):
        self.deal_cards()
        for _ in range(8):
            player1_card = self.player1_hand.pop()
            player2_card = self.player2_hand.pop()
            self.lead_round(player1_card, player2_card)
        print("Final Scores:")
        print("Player 1:", self.player1_score)
        print("Player 2:", self.player2_score)    

game = DecktionaryBattle()
game.deal_cards()
game.play_game()