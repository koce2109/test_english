import sqlite3

# Свързване с (или създаване на) базата данни
conn = sqlite3.connect('questions.db')
cursor = conn.cursor()

# Създаване на таблица за въпросите, ако не съществува
cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        level TEXT NOT NULL,        -- Ниво на теста (A1, A2, B1 и т.н.)
        question TEXT NOT NULL,     -- Текст на въпроса
        option_a TEXT NOT NULL,     -- Опция A
        option_b TEXT NOT NULL,     -- Опция B
        option_c TEXT NOT NULL,     -- Опция C
        option_d TEXT NOT NULL,     -- Опция D
        correct_answer TEXT NOT NULL -- Верният отговор (A, B, C или D)
    )
''')

# Запазване на промените и затваряне на връзката
conn.commit()
conn.close()

print("Database created successfully and table initialized.")
