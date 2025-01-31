import sqlite3

conn = sqlite3.connect('jarvis.db')
cursor = conn.cursor()

cursor.execute('''
INSERT INTO sys_command (name, path) VALUES
    ('brave', '/Applications/Brave Browser.app'),
    ('music', '/Applications/Music.app')
''')
conn.commit()
conn.close()
print("Data inserted successfully.")
