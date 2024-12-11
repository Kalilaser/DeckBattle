import sqlite3
import hashlib
import pandas as pd

class ProfileManager:
    def __init__(self, db_name="profiles.db"):
        # Initializes the database and creates the tables
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Creates the profiles table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS profiles (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                games_played INTEGER DEFAULT 0,
                wins INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0,
                win_percentage REAL DEFAULT 0.0,
                match_history TEXT DEFAULT ''
            )
        """)
        self.conn.commit()
        self.add_bot_profiles()

    def create_profile(self, name):
        # Generates a unique ID using a hash of the player's name
        profile_id = hashlib.sha256(name.encode()).hexdigest()[:10]
        try:
            self.cursor.execute("""
                INSERT INTO profiles (id, name) 
                VALUES (?, ?)
            """, (profile_id, name))
            self.conn.commit()
            print(f"Profile created for {name} with ID: {profile_id}")
        except sqlite3.IntegrityError:
            print("A profile with this name already exists.")

    def add_bot_profiles(self):
        # Adds bot profiles to the database
        bot_profiles = ["Easy Bot", "Medium Bot", "Expert Bot"]
        for bot in bot_profiles:
            profile_id = hashlib.sha256(bot.encode()).hexdigest()[:10]
            try:
                self.cursor.execute("""
                    INSERT INTO profiles (id, name)
                    VALUES (?, ?)
                """, (profile_id, bot))
                self.conn.commit()
            except sqlite3.IntegrityError:
                # If bot profiles already exist
                continue
    
    def force_fetch_bot_profile(self, profile_id, bot_name):
        """Fetches a bot profile or creates it if missing."""
        try:
            self.cursor.execute("SELECT * FROM profiles WHERE id = ? AND name = ?", (profile_id, bot_name))
            profile = self.cursor.fetchone()
            if not profile:
                print(f"Bot profile for {bot_name} not found. Creating it...")
                self.create_profile(bot_name)  # Create bot profile
                self.cursor.execute("SELECT * FROM profiles WHERE id = ? AND name = ?", (profile_id, bot_name))
                profile = self.cursor.fetchone()
            return profile
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

    def update_profile_stats(self, profile_id, wins=0, losses = 0):
        # Updates games played, wins, losses, and w/l percentage for a profile
        self.cursor.execute("""
            SELECT games_played, wins, losses FROM profiles WHERE id = ?
        """, (profile_id,))
        data = self.cursor.fetchone()
        if data:
            games_played, current_wins, current_losses = data
            games_played += wins + losses
            current_wins += wins
            current_losses += losses
            win_percentage = (current_wins / games_played) * 100 if games_played > 0 else 0.0

            self.cursor.execute("""
                UPDATE profiles 
                SET games_played = ?, wins = ?, losses = ?, win_percentage = ?
                WHERE id = ?
            """, (games_played, current_wins, current_losses, win_percentage, profile_id))
            self.conn.commit()
            print(f"Updated stats for profile ID: {profile_id}")
        else:
            print(f"No profile found with ID: {profile_id}")

    def get_leaderboard(self):
        # Retrieves leaderboard data (sorted by wins and w/l percentage)
        df = pd.read_sql_query("""
            SELECT name, games_played, wins, losses, win_percentage
            FROM profiles
            ORDER BY wins DESC, win_percentage DESC
        """, self.conn)
        return df
    
    def get_profile(self, profile_id):
        """Fetches a profile based on the profile ID."""
        try:
            self.cursor.execute("SELECT * FROM profiles WHERE id = ?", (profile_id,))
            profile = self.cursor.fetchone()
            return profile
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
    
    def delete_profile(self, profile_id):
        # Deletes a profile using ID
        self.cursor.execute("""
            DELETE FROM profiles WHERE id = ?
        """, (profile_id))
        self.conn.commit()
        print(f"Profile with ID {profile_id} has been deleted.")

    def close(self):
        # Closes the database connection
        self.conn.close()