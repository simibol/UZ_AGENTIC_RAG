import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="conversations.db"):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.initialize_tables()

    def initialize_tables(self):
        # Create tables if they don't already exist
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER NOT NULL,
            sender TEXT NOT NULL,  -- 'user' or 'assistant'
            message_text TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (conversation_id) REFERENCES conversations(id)
        )
        """)
        self.connection.commit()

    def create_conversation(self, user_id):
        # Start a new conversation
        self.cursor.execute("INSERT INTO conversations (user_id) VALUES (?)", (user_id,))
        self.connection.commit()
        return self.cursor.lastrowid

    def add_message(self, conversation_id, sender, message_text):
        # Add a message to an existing conversation
        self.cursor.execute("""
        INSERT INTO messages (conversation_id, sender, message_text) 
        VALUES (?, ?, ?)
        """, (conversation_id, sender, message_text))
        self.connection.commit()

    def get_conversation_history(self, conversation_id):
        # Fetch all messages in a conversation
        self.cursor.execute("""
        SELECT sender, message_text, timestamp FROM messages
        WHERE conversation_id = ?
        ORDER BY timestamp ASC
        """, (conversation_id,))
        return self.cursor.fetchall()

    def add_message(self, conversation_id, sender, message_text):
        # Ensure `message_text` is a string before inserting
        if not isinstance(message_text, str):
            message_text = str(message_text)

        self.cursor.execute("""
        INSERT INTO messages (conversation_id, sender, message_text) 
        VALUES (?, ?, ?)
        """, (conversation_id, sender, message_text))
        self.connection.commit()

    def close(self):
        self.connection.close()