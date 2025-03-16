import sqlite3

# Свързваме се с базата
conn = sqlite3.connect("questions.db")
cursor = conn.cursor()

# Добавяне на въпроси (ниво, въпрос, отговори, правилен отговор)
new_questions = [
    ("A1", "What is the capital of France?", "Paris", "London", "Berlin", "Madrid", "Paris"),
    ("A2", "Which is a mammal?", "Shark", "Frog", "Dog", "Snake", "Dog"),
    ("B1", "What is the synonym of 'happy'?", "Sad", "Angry", "Joyful", "Tired", "Joyful"),
    ("B2", "Who wrote '1984'?", "Orwell", "Huxley", "Tolkien", "Shakespeare", "Orwell"),
    ("C1", "What does 'meticulous' mean?", "Careful", "Lazy", "Boring", "Fast", "Careful"),
]

# Добавяне в таблицата
cursor.executemany(
    "INSERT INTO questions (level, question, option1, option2, option3, option4, correct_answer) VALUES (?, ?, ?, ?, ?, ?, ?)",
    new_questions
)

# Запазваме промените
conn.commit()
conn.close()

print("✅ Въпросите са добавени успешно!")
