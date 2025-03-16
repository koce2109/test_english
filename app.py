from flask import Flask, render_template, request
import sqlite3
import random

app = Flask(__name__, template_folder='templates')

def get_questions(level):
    # Свързване с базата данни и извличане на въпроси за съответното ниво
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions WHERE level=?", (level,))
    questions = cursor.fetchall()
    conn.close()
    return questions


@app.route('/', methods=['GET', 'POST'])
def index():
    level = None
    questions = []

    if request.method == 'POST':
        level = request.form['level']  # Избираме ниво
        questions = get_questions(level)  # Вземаме въпросите за това ниво
        selected_questions = random.sample(questions, 10)  # Вземаме 10 въпроса случайно

        # Записваме ID-та на избраните въпроси за да ги изпратим в резултатната страница
        selected_question_ids = [str(question[0]) for question in selected_questions]

        return render_template('index.html', questions=selected_questions, level=level, selected_question_ids=','.join(selected_question_ids))

    return render_template('index.html', level=level, questions=questions)


@app.route('/result', methods=['POST'])
def result():
    # Вземаме отговорите от формата
    answers = request.form.getlist('answers')
    level = request.form.get('level')  # Вземаме нивото от формата

    # Вземаме избраните въпроси от сесията
    selected_questions_ids = request.form.get('selected_questions_ids')  # Добавяме идентификаторите на избраните въпроси
    selected_questions_ids = selected_questions_ids.split(",")  # Разделяме идентфикаторите на въпросите

    selected_questions = []

    # Свързваме се с базата и вземаме само въпросите с тези идентификатори
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions WHERE id IN ({})".format(','.join('?' for _ in selected_questions_ids)), selected_questions_ids)
    selected_questions = cursor.fetchall()
    conn.close()

    # Резултати от теста
    score = 0
    result_data = []

    for question in selected_questions:
        question_id = question[0]
        correct_answer = question[7]  # правилен отговор
        user_answer = request.form.get(f'answers[{question_id}]')  # Получаваме отговора на потребителя

        result_data.append({
            'question': question[2],
            'options': [question[3], question[4], question[5], question[6]],
            'user_answer': user_answer,
            'correct_answer': correct_answer,
            'is_correct': (user_answer == correct_answer)  # Проверка дали отговорът е верен
        })

        if user_answer == correct_answer:
            score += 1

    return render_template('result.html', score=score, result_data=result_data, level=level)

if __name__ == '__main__':
    app.run(debug=True)
