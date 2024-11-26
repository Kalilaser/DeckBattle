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
        
        # Determines the lead suit
        lead_suit = player1_card[1] if leader == 1 else player2_card[1]
        print(f"Player 1 plays: {player1_card}, Player 2 plays: {player2_card}")
        print(f"Lead suit: {lead_suit}")
        
        # Initilization of the winner variable
        winner = None

        # Follow Suit Rule Check: Checks to see if anyone did not follow the suit
        if follower == 2 and player2_card[1] != lead_suit and any(card[1] == lead_suit for card in self.player2_hand):
            print("Player 2 broke the rules by not following suit!")
            winner = 1 # Player 1 automatically wins
        elif follower == 1 and player1_card[1] != lead_suit and any(card[1] == lead_suit for card in self.player1_hand):
            print("Player 1 broke the rules by not following suit!")
            winner = 2 # Player 2 automatically wins
            
        if winner is None:   
            # Determines the winner normally if no rules have been broken
            if (player2_card[1] == lead_suit and leader == 1) or (player1_card[1] == lead_suit and leader == 2):
                winner = 1 if player1_card[0] > player2_card[0] else 2
                print(f"Both players followed the suit. Winner: Player {winner}")
            else:
                winner = leader
                print(f"Player {follower} did not follow suit. Winner: {leader}")
        
        # Updates the scores
        if winner == 1:
            self.player1_score += 1
            print("Player 1 wins this round!")
        else:
            self.player2_score += 1
            print("Player 2 wins this round!")
        
        # Reveals the next card from the deck
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
        print("Welcome to Decktionary Battle!")
        self.deal_cards()
        # Player 1 leads the first round
        leader = 1

        while True: # Loops until the game ends
            for round_num in range(1,9): # Play 8 rounds
                print(f"\n--- Round {round_num} ---")
                print(f"Player {leader} is leading this round.")
                leader = self.lead_round(leader, 2 if leader == 1 else 1)

                # Checks the game-ending criteria after each round
                if self.check_game_end():
                    return
        
            # Deals new cards
            if len(self.deck) >= 16:
                print("\n--- Dealing New Cards ---")
                self.deal_cards()
            else:
                print("\nNot enough cards to deal. Game over.")
                break
        
        self.print_final_scores()
    
    def check_game_end(self):
        # Checks if the game should end based off the set rules

        # If a player has shot the moon
        if self.player1_score == 16 and self.player2_score == 0:
            self.print_final_scores("Player 1 has shot the moon and wins with 17 points!")
            return True
        if self.player2_score == 16 and self.player1_score == 0:
            self.print_final_scores("Player 2 has shot the moon and wins with 17 points!")
            return True
        
        # If a player is guaranteed to win
        if self.player1_score >= 9 and self.player2_score >= 1:
            self.print_final_scores("Player 1 is guaranteed to win. Ending game early.")
            return True
        if self.player2_score >= 9 and self.player1_score >= 1:
            self.print_final_scores("Player 2 is guaranteed to win. Ending game early.")
            return True
        
        return False # Continues game if moon or guaranteed win criteria has not been met
         
    def print_final_scores(self, message=None):   
        if message:
            print(f"\n{message}")
        print("\n--- Final Scores ---")
        print("Player 1:", self.player1_score)
        print("Player 2:", self.player2_score)

        if self.player1_score > self.player2_score:
            print("Player 1 wins the game!")
        elif self.player2_score > self.player1_score:
            print("Player 2 winds the game!")
        else:
            print("The game is a tie!")
        
        
        

game = DecktionaryBattle()
game.play_game()