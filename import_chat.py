import os
import sqlite3
import re
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, 'chat_log.db')
RAW_CHAT_DIR = os.path.join(BASE_DIR, 'RAW_Chat')

def import_logs():
    if not os.path.exists(RAW_CHAT_DIR):
        print(f"RAW_Chat directory not found: {RAW_CHAT_DIR}")
        return

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Create table just in case
    c.execute('''
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            source_id TEXT,
            user_id TEXT,
            message TEXT
        )
    ''')

    txt_files = [f for f in os.listdir(RAW_CHAT_DIR) if f.endswith('.txt')]
    
    for file_name in txt_files:
        file_path = os.path.join(RAW_CHAT_DIR, file_name)
        source_id = file_name.replace('.txt', '').replace('[LINE]', '').strip()
        print(f"Processing file: {file_name} -> Source ID: {source_id}")
        
        current_date = None
        last_row_id = None
        
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            lines = f.readlines()
            
        for line in lines:
            line_str = line.strip('\r\n')
            if not line_str:
                continue
                
            # 1. Check if date header (e.g. 2026.02.25 Wednesday)
            date_match = re.match(r'^(\d{4})\.(\d{2})\.(\d{2})\s+\w+', line_str)
            if date_match:
                current_date = f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}"
                continue
                
            # 2. Check if message line (e.g. 09:41 Torre Message)
            msg_match = re.match(r'^(\d{2}):(\d{2})\s+([^\s]+)\s+(.*)$', line_str)
            if msg_match and current_date:
                time_str = f"{msg_match.group(1)}:{msg_match.group(2)}"
                user_id = msg_match.group(3)
                message = msg_match.group(4)
                timestamp = f"{current_date} {time_str}:00"
                
                c.execute(
                    'INSERT INTO chat_messages (timestamp, source_id, user_id, message) VALUES (?, ?, ?, ?)',
                    (timestamp, source_id, user_id, message)
                )
                last_row_id = c.lastrowid
                
            # 3. It's a continuation line or message without text?
            elif current_date and last_row_id:
                c.execute('SELECT message FROM chat_messages WHERE id = ?', (last_row_id,))
                old_msg = c.fetchone()[0]
                new_msg = old_msg + "\n" + line_str
                c.execute('UPDATE chat_messages SET message = ? WHERE id = ?', (new_msg, last_row_id))
        
        conn.commit()
        print(f"Finished processing {file_name}")

    conn.close()
    print("All chat logs imported successfully!")

if __name__ == '__main__':
    import_logs()
