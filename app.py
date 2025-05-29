from flask import Flask, request, jsonify
import database

app = Flask(__name__)
DATABASE = 'tasks.db'

@app.before_first_request
def initialize_database():
    conn = database.create_connection(DATABASE)
    database.create_table(conn)
    conn.close()

def simple_ai_response(question):
    # Prosta logika do generowania odpowiedzi
    responses = {
        "Jakie są zalety uczenia maszynowego?": "Zalety to automatyzacja, dokładność, i możliwość analizy dużych zbiorów danych.",
        "Co to jest Python?": "Python to wszechstronny język programowania, który jest łatwy do nauki i używania.",
        "Jakie są zastosowania sztucznej inteligencji?": "Zastosowania obejmują rozpoznawanie obrazów, przetwarzanie języka naturalnego, i autonomiczne pojazdy."
    }
    return responses.get(question, "Przepraszam, nie znam odpowiedzi na to pytanie.")

@app.route('/ask', methods=['POST'])
def ask_question():
    question = request.json.get('question')
    
    # Uzyskanie odpowiedzi z lokalnej logiki
    answer = simple_ai_response(question)
    
    # Zapisanie pytania i odpowiedzi do bazy danych
    conn = database.create_connection(DATABASE)
    database.insert_task(conn, (question, answer))
    conn.close()
    
    return jsonify({"question": question, "answer": answer}), 200

@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    conn = database.create_connection(DATABASE)
    tasks = database.get_tasks(conn)
    conn.close()
    return jsonify(tasks)

if __name__ == '__main__':
    app.run(debug=True)
    
