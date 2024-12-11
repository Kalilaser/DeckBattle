import random
import csv
import time
import pandas as pd
import hashlib
from profiles import ProfileManager

class DecktionaryBattle:
    def __init__(self):
        self.debug = True        
        self.deck = self.create_deck()
        self.revealed_cards = []
        self.player1_score = 0
        self.player2_score = 0
        self.game_log = []
        self.game_number = 1
        self.playing_against_bot = False
        self.bot_difficulty = None
        self.profile_manager = ProfileManager()
        self.player1_profile = None
        self.player2_profile = None
        self.card_memory = pd.DataFrame(columns=["rank", "suit", "player"])
        self.bot_decision_time = 0
        self.game_mode = 'long' 

    def main_menu(self):
        while True:
            print("\n--- Main Menu ---")
            print("1. Play Game")
            print("2. Log In")
            print("3. Leaderboard")
            print("4. Settings")
            print("5. Quit")
            choice = input("Enter your choice: ").strip()

            if choice == '1':
                self.play_game()
            elif choice == '2':
                self.log_in()
            elif choice == '3':
                self.show_leaderboard()
            elif choice == '4':
                self.settings_menu()
            elif choice == '5':
                print("Exiting the game. Goodbye!")
                self.profile_manager.close()
                break
            else:
                print("Invalid choice. Please try again.")
    
    def settings_menu(self):
        print("\n--- Settings ---")
        print("1. Change Game Mode (Current: {})".format("short" if self.game_mode == "short" else "long"))
        print("2. Log Out")
        print("3. Back to Main Menu")
        choice = input("Select an option: ").strip()
        if choice == "1":
            self.change_game_mode()
        elif choice == "2":
            self.logout_current_accounts()
        elif choice == "3":
            return
        else:
            print("Invalid choice. Please try again.")

    def change_game_mode(self):
        """Toggle between short and long game modes."""
        if self.debug:
            print(f"Debug: Changing game mode from: {self.game_mode}")
        
        self.game_mode = "short" if self.game_mode == "long" else "long"
        print(f"Game mode changed to {'short' if self.game_mode == 'short' else 'long'}.")

    def log_in(self):
        print("\n--- Log in / Create Profile ---")
        name = input("Enter your name: ").strip()
        if name in ["Easy Bot", "Medium Bot", "Expert Bot"]:
            print(f"Cannot log in as {name}.")
            return None
        profile_id = hashlib.sha256(name.encode()).hexdigest()[:10]
        profile = self.profile_manager.get_profile(profile_id)
        
        if profile:
            print(f"Welcome back, {name}!")
            print(f"Games Played: {profile[2]}, Wins: {profile[3]}, Losses: {profile[4]}, Win Percentage: {profile[5]:.2f}%")
            self.player1_profile = profile
            return profile
        else:
            print(f"No profile found for {name}. Would you like to create one?")
            choice = input("Enter Y to create a new profile or N to cancel: ").strip().lower()
            if choice == "y":
                self.profile_manager.create_profile(name)
                self.player1_profile = self.profile_manager.get_profile(profile_id)
                return self.player1_profile
            else:
                print("Log in canceled.")
                return None

    def logout_current_accounts(self):
        """Logs out the currently logged-in Player 1 and Player 2."""
        self.player1_profile = None
        self.player2_profile = None
        print("Both Player 1 and Player 2 have been logged out.")

    def show_leaderboard(self):
        print("\n---- Leaderboard ---")
        leaderboard = self.profile_manager.get_leaderboard()
        print(leaderboard)
        print("\nStatistics Visualization:")
        self.visualize_leaderboard(leaderboard)

    def visualize_leaderboard(self, leaderboard):
        import matplotlib.pyplot as plt
        import seaborn as sns

        sns.barplot(data=leaderboard, x='name', y='win_percentage', order=leaderboard['name'])
        plt.title("Win Percentage by Player")
        plt.ylabel("Win Percentage (%)")
        plt.xlabel("Player Name")
        plt.xticks(rotation=45)
        plt.show()

    def choose_opponent(self):
        # This is to choose to play against another human locally or against the computer
        print("Choose your opponent:")
        print("1. Human")
        print("2. CPU")
        while True:
            choice = input("Enter 1 for Human or 2 for CPU: ").strip()
            if choice == '1':
                self.playing_against_bot = False
                print("You chose to play against a human!")
                return
            elif choice == '2':
                self.playing_against_bot = True
                self.choose_bot_difficulty()
                print("You the difficulty:")
                print(f"{self.bot_difficulty}")
                return
            else:
                print("Invalid choice. Please Try again.")

    def choose_bot_difficulty(self):
        # Chooses difficulty
        print("Choose bot difficulty:")
        print("1. Easy")
        print("2. Medium")
        print("3. Expert")
        bot_profiles = {
            "1": "Easy Bot",
            "2": "Medium Bot",
            "3": "Expert Bot"
        }
        while True:
            difficulty = input("Enter 1 for Easy, 2 for Medium, 3 for Expert: ").strip()
            if difficulty in bot_profiles:
                self.bot_difficulty = bot_profiles[difficulty]
                print(f"Bot difficulty set to {self.bot_difficulty}.")
                bot_profile_id = hashlib.sha256(self.bot_difficulty.encode()).hexdigest()[:10]
                
                # Fetch or create bot profile without login restrictions
                self.player2_profile = self.profile_manager.force_fetch_bot_profile(bot_profile_id, self.bot_difficulty)
                if not self.player2_profile:
                    print(f"Error: Could not initialize profile for {self.bot_difficulty}.")
                    return
                self.playing_against_bot = True
                return
            else:
                print("Invalid choice. Please try again.")

    def create_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = list(range(2,15)) # 2 to Ace (Ace = 14)
        deck = [(rank, suit) for suit in suits for rank in ranks if rank != 13] # This removes the kings
        random.shuffle(deck)
        
        if self.debug:
            print("\nDebug: Generated Deck (shuffled):")
            print(deck)
        
        return deck
    
    def log_event(self, round_num, player1_card, player2_card, winner):
        #Logs the details of the round to then be saved to a .csv file
        self.game_log.append({
            'Game': self.game_number,
            'Round': round_num,
            'Player 1 Hand': self.player1_hand.copy(),
            'Player 2 Hand': self.player2_hand.copy(),
            'Player 1 Card': player1_card,
            'Player 2 Card': player2_card,
            'Winner': f"Player {winner}",
            'Player 1 Score': self.player1_score,
            'Player 2 Score': self.player2_score
        })

    def save_log_to_csv(self, filename="game_log.csv"):
        with open(filename, 'a', newline='') as csvfile:  # Open in append mode
            fieldnames = [
                'Game', 
                'Round', 
                'Player 1 Hand', 
                'Player 2 Hand', 
                'Player 1 Card', 
                'Player 2 Card', 
                'Winner', 
                'Player 1 Score', 
                'Player 2 Score'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write header only if the file is empty
            if csvfile.tell() == 0:
                writer.writeheader()

            # Add the game number to each log entry and write to the CSV
            for log in self.game_log:
                for field in fieldnames:
                    log.setdefault(field, '')
                log['Game'] = self.game_number  # Include game number
                writer.writerow(log)

            # Add a blank row to separate games
            writer.writerow({})

        self.game_number += 1

    def log_final_scores(self):
    # Logs the final scores and game summary.
        self.game_log.append({
            'Game': self.game_number,
            'Round': 'Final',
            'Player 1 Hand': self.player1_hand.copy(),
            'Player 2 Hand': self.player2_hand.copy(),
            'Player 1 Card': '',
            'Player 2 Card': '',
            'Winner': 'Game Over',
            'Player 1 Score': self.player1_score,
            'Player 2 Score': self.player2_score
    })

    def deal_cards(self):
        if self.deck or len(self.deck) < 16:  # Reinitialize the deck if insufficient cards are left
            self.deck = self.create_deck()  # Recreate the full deck
            if self.debug:
                print("Debug: Deck reinitialized.")
        
        
        self.player1_hand = [self.deck.pop() for _ in range(8)]
        self.player2_hand = [self.deck.pop() for _ in range(8)]
        
        if self.debug:
            print("Player 1 Hand:")
            print(self.render_cards(self.player1_hand))
            print("Player 2 Hand:")
            print(self.render_cards(self.player2_hand))
            print("Debug: Remaining Deck:")
            print(self.deck)
        
        self.game_log.append({
            'Round': 'Deal',
            'Player 1 Hand': self.player1_hand,
            'Player 2 Hand': self.player2_hand,
            'Winner': 'N/A'
        })

    def render_cards(self, cards):
        # This is going to change the cards from (#, *Suit*) to display a text based image of a card to look nicer when playing

        if isinstance(cards, tuple):
            cards = [cards]  # Converts single card tuple to a list

        suit_symbols = {'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣', 'Spades': '♠'}
        rank_map = {11: 'J', 12: 'Q', 14: 'A'} # Maps the special cards so it doesnt appear as a number
        card_lines = [''] * 4 # For storing the actual face of the cards

        for rank, suit in cards:
            rank_str = rank_map.get(rank, str(rank)) # This changes number to a string
            suit_symbol = suit_symbols[suit]

            # Add card lines
            card_lines[0] += "┌─────┐  "
            card_lines[1] += f"|  {rank_str:<2} |  "  # Rank left-aligned
            card_lines[2] += f"|  {suit_symbol}  |  "
            card_lines[3] += f"|  {rank_str:<2} |  "
        
        card_lines.append("└─────┘  " * len(cards))

        return "\n".join(card_lines)
    
    def lead_round(self, leader, follower):
        
        if self.debug:
            print(f"Debug: Leader: Player {leader}, Follower: Player {follower}")
            print(f"Debug: Player 1's hand: {self.player1_hand}")
            print(f"Debug: Player 2's hand: {self.player2_hand}")
        
        if leader == 1:
            player1_card = self.choose_card(self.player1_hand, 1)
            player2_card = self.choose_card(self.player2_hand, 2)
        else:
            player2_card = self.choose_card(self.player2_hand, 2)
            player1_card = self.choose_card(self.player1_hand, 1)

        if player1_card is None or player2_card is None:
            if self.debug:    
                print("Error: A player failed to play a valid card. Ending round.")
            return None, None, None

        # Determines the lead suit
        self.lead_suit = player1_card[1] if leader == 1 else player2_card[1]
        if self.debug:
            print(f"Debug: Lead suit determined as {self.lead_suit}")
        
        print("Player 1 plays:")
        print(self.render_cards(player1_card))
        print("Player 2 plays:")
        print(self.render_cards(player2_card))
        print(f"Lead suit: {self.lead_suit}")
        
        # Initilization of the winner variable
        winner = None

        # Follow Suit Rule Check: Checks to see if anyone did not follow the suit
        if follower == 2 and player2_card[1] != self.lead_suit and any(card[1] == self.lead_suit for card in self.player2_hand):
            print("Player 2 broke the rules by not following suit!")
            winner = 1 # Player 1 automatically wins
        elif follower == 1 and player1_card[1] != self.lead_suit and any(card[1] == self.lead_suit for card in self.player1_hand):
            print("Player 1 broke the rules by not following suit!")
            winner = 2 # Player 2 automatically wins
            
        if winner is None:   
            # Determines the winner normally if no rules have been broken
            if (player2_card[1] == self.lead_suit and leader == 1) or (player1_card[1] == self.lead_suit and leader == 2):
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
        revealed_card = self.deck.pop()
        self.revealed_cards.append(revealed_card)
        print("Revealed Card:")
        print(self.render_cards(revealed_card))
        
        return player1_card, player2_card, winner
    
    def get_lead_suit(self):
        """Returns the lead suit for the current round"""
        return self.lead_suit

    def choose_card(self, player_hand, player_num):
        # Single-player mode: Show player's hand without privacy controls
        if self.playing_against_bot and player_num == 1:
            print("Your hand:")
            print(self.render_cards(player_hand))
            while True:
                choice = input(f"Choose a card by index (0-{len(player_hand) - 1}): ").strip()
                if choice.isdigit():
                    card_idx = int(choice)
                    if 0 <= card_idx < len(player_hand):
                        return player_hand.pop(card_idx)
                    else:
                        print("Invalid card index. Try again.")
                else:
                    print("Invalid input. Enter a number.")
        elif self.playing_against_bot and player_num == 2:
            return self.bot_choose_card(player_hand)
        else:
            print(f"Game Mode: {'Singleplayer' if self.playing_against_bot else 'Multiplayer'}")
            # Multiplayer mode: Allow privacy controls for human players
            hidden = True  # Cards start hidden in multiplayer
            while True:
                if hidden:
                    print(f"Player {player_num}'s hand is hidden. Type 'show' (s) to display it.")
                else:
                    print(f"Player {player_num}'s turn. Your hand:")
                    print(self.render_cards(player_hand))
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

    def bot_choose_card(self, bot_hand):
        """Logic for the bot to choose a card based on the difficulty."""
        if not bot_hand:
            if self.debug:
                print("Error: Bot has no cards to play!")
            return None  # Return early if the bot has no cards
        
        if self.debug:
            print(f"Debug: Bot's hand before choosing: {bot_hand}")

        print("Bot is choosing a card...")
        if self.bot_difficulty == "easy":
            return self.bot_easy_choice(bot_hand)
        elif self.bot_difficulty == "medium":
            return self.bot_medium_choice(bot_hand)
        elif self.bot_difficulty == "expert":
            return self.bot_expert_choice(bot_hand)
        else:
            chosen_card = bot_hand.pop()
            if self.debug:
                print(f"Debug: Bot (fallback) chose card: {chosen_card}")
            return chosen_card

    def bot_easy_choice(self, bot_hand):
        if not bot_hand:
            if self.debug:
                print("Debug: Bot (easy) has no cards in its hand!")
            return None
        if self.debug:
            print(f"Debug: Bot (easy) hand: {bot_hand}")
        random.shuffle(bot_hand) # This will shuffle the bots hand to add randomness to the pick
        chosen_card = bot_hand.pop() # Picks a random card from the hand
        if self.debug:
            print(f"Debug: Bot (easy) chose card: {chosen_card}")
        return chosen_card    
    
    def bot_medium_choice(self, bot_hand):
        if not bot_hand:
            if self.debug:
                print("Debug: Bot (medium) has no cards in its hand!")
            return None
        
        if self.debug:
            print(f"Debug: Bot (medium) hand: {bot_hand}")
        
        if self.lead_suit is None:
            # If there is no lead suit, play the lowest card
            chosen_card = bot_hand.pop(bot_hand.index(min(bot_hand, key=lambda x: x[0])))
        else:
            # Filters cards in hand for the lead suit
            valid_cards = [card for card in bot_hand if card[1] == self.lead_suit]
            if valid_cards:
                chosen_card = bot_hand.pop(bot_hand.index(max(valid_cards, key=lambda x: x[0]))) # Plays then highest card in suit
            else:
                chosen_card = bot_hand.pop(bot_hand.index(min(bot_hand, key=lambda x: x[0]))) # Dumps lowest card
        if self.debug:
            print(f"Debug: Bot (medium) chose card: {chosen_card}")
        return chosen_card
    
    def bot_expert_choice(self, bot_hand):
        if not bot_hand:
            if self.debug:
                print("Debug: Bot (expert) has no cards in its hand!")
            return None
        if self.debug:
            print(f"Debug: Bot (expert) hand: {bot_hand}")
            print("Debug: Expert Bot is analyzing the game...")

        # Filter known cards (revealed or played)
        known_cards = self.card_memory.copy()

        # Add revealed cards to memory
        for card in self.revealed_cards:
            if not ((known_cards['rank'] == card[0]) & (known_cards['suit'] == card[1])).any():
                known_cards = pd.concat([known_cards, pd.DataFrame([{"rank": card[0], "suit": card[1], "player": "revealed"}])], ignore_index=True)

        # Expert Bot logic: play a winning card if possible
        if self.lead_suit:
            valid_cards = [card for card in bot_hand if card[1] == self.lead_suit]
            if valid_cards:
                # Try to win the round
                chosen_card = max(valid_cards, key=lambda x: x[0], default=None)
            else:
                # Play the lowest card
                chosen_card = min(bot_hand, key=lambda x: x[0])
        else:
            # No lead suit, play the lowest card
            chosen_card = min(bot_hand, key=lambda x: x[0])

        # Remove chosen card from hand and log it
        bot_hand.remove(chosen_card)
        
        if self.debug:
            print(f"Debug: Bot (expert) chose card: {chosen_card}")
        return chosen_card

    def visualize_bot_memory(self):
        import seaborn as sns
        import matplotlib.pyplot as plt

        if not self.card_memory.empty:
            sns.countplot(data=self.card_memory, x="suit", hue="player")
            plt.title("Expert Bot Memory of Played Cards")
            plt.xlabel("Suit")
            plt.ylabel("Count")
            plt.legend(title="Player")
            plt.show()
        else:
            print("No cards played yet.")
    
    def end_game_summary(self):
        print("\n--- Game Summary ---")
        print("Expert Bot Memory:")
        print(self.card_memory)
        self.visualize_bot_memory()

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

    def is_long_game(self):
        return self.game_mode == 'long'
    
    def is_short_game(self):
        return self.game_mode == 'short'

    def play_game(self):
        print("Welcome to Decktionary Battle!")
        self.print_instructions()
        self.reset_game_state()
        if self.debug:
            print(f"Debug: Starting game in mode: {self.game_mode}")
        
        print("\n--- Choose Game Mode ---")
        print("1. Multiplayer")
        print("2. Singleplayer")

        while True:
            mode = input("Enter 1 for Multiplayer, 2 for Singleplayer: ").strip()
            if mode == '1':
                self.setup_multiplayer_game()
                return
            elif mode == "2":
                self.setup_singleplayer_game()
                return
            else:
                print("Invalid choice. Please try again.")

    def setup_multiplayer_game(self):
        print("\n--- Multiplayer Setup ---")
        if self.player1_profile:
                print("\nPlayer 1 is already logged in.")
                print("1. Add Player 2")
                print("2. Back to Main Menu")
                choice = input("Enter your choice: ").strip()
                if choice == "1":
                    print("Choose Player 2:")
                    self.player2_profile = self.log_in()
                    if not self.player2_profile:
                        print("Failed to log in Player 2. Returning to menu.")
                        return
                elif choice == "2":
                    return
                else:
                    print("Invalid choice. Returning to menu.")
                    return    
        else:
            # Logs in both players if player 1 was not logged in from main menu
            print("Choose Player 1:")
            self.player1_profile = self.log_in()
            if not self.player1_profile:
                print("Failed to log in to player 1. Returning to menu.")
                return
            
            print("Choose Player 2:")
            self.player2_profile = self.log_in()
            if not self.player2_profile:
                print("Failed to log in Player 2. Returning to menu.")
                return
        if self.debug:
            print(f"Debug: Starting game in mode: {self.game_mode}")
        self.play_multiplayer_game()

    def setup_singleplayer_game(self):
        print("\n--- Singleplayer Setup ---")
        if not self.player1_profile:
            print("Choose Player 1:")
            self.player1_profile = self.log_in()
            if not self.player1_profile:
                print("Playing as guest. Stats will not be recorded")
                self.player1_profile - {"name": "Guest"}
        else:
            print(f"Continuing as {self.player1_profile[1]}")
        self.choose_bot_difficulty()

        if self.debug:
            print(f"Debug: Starting game in mode: {self.game_mode}")
        
        if self.is_long_game():
            self.play_long_game()
        elif self.is_short_game():
            self.play_short_game()
    
    def play_multiplayer_game(self):
        print("\n--- Multiplayer Game ---")
        self.deal_cards()
        self.start_game_loop()
        self.update_profiles()

    
    def play_long_game(self):
        print("\n--- Starting Long Game ---")
        self.deal_cards()
        self.start_game_loop()
        self.print_final_scores()
        self.log_final_scores()
        self.save_log_to_csv()
        self.update_profiles()

    def play_short_game(self):
        print("\n--- Starting Short Game ---")
        self.deal_cards()
        self.start_game_loop()
        print("--- Game Over ---")
        self.print_final_scores()
        self.log_final_scores()
        self.save_log_to_csv()
        self.update_profiles()

    def update_profiles(self):
        if self.player1_profile:
            self.profile_manager.update_profile_stats(
                self.player1_profile[0],
                wins=1 if self.player1_score > self.player2_score else 0,
                losses=1 if self.player1_score < self.player2_score else 0
            )
        
        if self.player2_profile:
            self.profile_manager.update_profile_stats(
                self.player2_profile[0],
                wins=1 if self.player2_score > self.player1_score else 0,
                losses=1 if self.player2_score < self.player1_score else 0
            )

    def start_game_loop(self):
        
        self.lead_suit = None # Resets the lead suit
        leader = 1 # Player 1 leads the first round

        while True: # Loops until the game ends
            if self.debug:
                print("\nDebug: Current Deck State:")
                print(self.deck)
            
            for round_num in range(1,9): # Play 8 rounds
                print(f"\n--- Round {round_num} ---")
                print(f"Player {leader} is leading this round.")
                player1_card, player2_card, winner = self.lead_round(leader, 2 if leader == 1 else 1)

                leader = winner

                # Logs the round        
                self.log_event(round_num, player1_card, player2_card, winner)
                
                # Checks the game-ending criteria after each round
                if self.check_game_end():
                    return

            # After 8 rounds checks if hands are empty in long games
            if self.is_long_game():
                if not self.player1_hand and not self.player2_hand:
                    if len(self.deck) >= 16:
                        print("\n--- Dealing New Cards ---")
                        self.deal_cards()
                    else:
                        print("\nNot enough cards to deal. Game over.")
                        return
            elif self.is_short_game():
                if not self.player1_hand and not self.player2_hand:
                    print("\n--- Hands are empty. Game over. ---")
                    return

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
         
    def reset_game_state(self):
        """Resets the game state for a new game."""
        self.deck = self.create_deck()
        self.revealed_cards = []
        self.player1_score = 0
        self.player2_score = 0
        self.lead_suit = None
        self.game_log = []
        self.game_number += 1  # Increment game number for logging
        if self.debug:
            print("Debug: Game state reset.")    
    
    def print_final_scores(self, message=None):   
        if message:
            print(f"\n{message}")
        print("\n--- Final Scores ---")
        print("Player 1:", self.player1_score)
        print("Player 2:", self.player2_score)

        if self.player1_score > self.player2_score:
            print("Player 1 wins the game!")
        elif self.player2_score > self.player1_score:
            print("Player 2 wins the game!")
        else:
            print("The game is a tie!")

if __name__ == "__main__":
    game = DecktionaryBattle()
    game.main_menu()