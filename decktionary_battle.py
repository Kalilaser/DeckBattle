import random

class DecktionaryBattle:
    def __init__(self):
        self.deck = self.create_deck()
        self.revealed_cards = []
        self.player1_score = 0
        self.player2_score = 0
        self.debug = False

    def create_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = list(range(2,15)) # 2 to Ace (Ace = 14)
        deck = [(rank, suit) for suit in suits for rank in ranks if rank != 13] # This removes the kings
        random.shuffle(deck)
        return deck
    
    def deal_cards(self):
        self.player1_hand = [self.deck.pop() for _ in range(8)]
        self.player2_hand = [self.deck.pop() for _ in range(8)]
        if self.debug:
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

        # This allows players to choose a card from their hand with controls for privacy
        hidden = True
        while True:
            if hidden:
                print(f"Player {player_num}'s hand is hidden. Type 'show' (s) to display it.")
            else:
                print(f"Player {player_num}'s turn. Your hand:")
                for idx, card in enumerate(player_hand):
                    print(f"{idx}: {card}")
        
            choice = input(f"Player {player_num}, choose an action (show/s, hide/h, or pick a card): ").lower()

            if choice in ['show', 's']:
                hidden = False
            elif choice in ['hide', 'h']:
                hidden = True
            elif choice.isdigit() and not hidden:
                card_idx = int(choice)
                if 0 <= card_idx < len(player_hand):
                    return player_hand.pop(card_idx)
                else:
                    print("Invalid card index. Please try again.")
            else:
                print("Invalid input. Please try again.")


    def print_instructions(self):
    # This is to print the rules and instructions of the game.
        print("\n--- Rules of Decktionary Battle ---")
        print("""
        1. The game uses a standard deck of playing cards with Kings removed (48 cards).
        2. Each player starts with 8 cards in their hand.
        3. Player 1 always leads the first round.
        4. The player who leads sets the suit for the round (the lead suit).
        5. The other player must follow the lead suit if possible.
        6. If the player cannot follow the lead suit, they may play any card.
        7. The highest-value card in the lead suit wins the round.
        8. The player who wins the round earns a point and leads the next round.
        9. After every 8 rounds, if enough cards are left in the deck, each player is dealt 8 new cards.
        10. The game ends when:
            - One player scores 16-0 and "shoots the moon," winning with 17 points.
            - One player scores 9+ points while the other player has at least 1 point.
            - The deck runs out of cards to deal.
        11. The player with the most points at the end of the game wins.

        Instructions:
        - Players will take turns selecting cards from their hand.
        - Follow the prompts to choose a card to play each round.
        - Have fun and strategize to win!       
        """)
    
    def get_game_length(self):
        # Prompts user to choose the length of the game.
        print("Choose game length:")
        print("short (s) - Play one hand (8 rounds)")
        print("long (l) - Play the entire deck (Default)")
        while True:
            choice = input("Enter your choice (short/s or long/l}: ").lower()
            if choice in ['short', 's']:
                return "short"
            if choice in ['long', 'l']:
                return "long"
            else:
                print("Invalid input. Please type 'short' or 's' fpr a short game, or 'long' or 'l' for a long game.")

    def play_game(self):
        print("Welcome to Decktionary Battle!")
        self.print_instructions() # Runs the print_instructions
        
        # Choose game length
        game_length = self.get_game_length()
        
        self.deal_cards() # Deals out the initial 8 cards
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
            
            if game_length == "short":
                print("\n--- Short game completed ---")
                break

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