from flask import Flask, request, jsonify
import database

app = Flask(__name__)
DATABASE = 'tasks.db'

@app.before_first_request
def initialize_database():
    conn = database.create_connection(DATABASE)
    database.create_table(conn)
    conn.close()

@app.route('/tasks', methods=['POST'])
def add_task():
    task_data = request.json
    task = (task_data['name'], task_data['completed'])
    conn = database.create_connection(DATABASE)
    task_id = database.insert_task(conn, task)
    conn.close()
    return jsonify({"id": task_id}), 201

@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    conn = database.create_connection(DATABASE)
    tasks = database.get_tasks(conn)
    conn.close()
    return jsonify(tasks)

if __name__ == '__main__':
    app.run(debug=True)
  
