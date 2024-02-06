from asyncio import tasks

from flask import Flask, jsonify, request
from flask_cors import CORS
import json;

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)

test = 'pong'
JSON_FILE_PATH = 'tasks.json'

def load_tasks_from_file():
    try:
        with open(JSON_FILE_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:  # Если файл не существует, вернуть пустой список
        return []
#test
def save_tasks_to_file(tasks):
    with open(JSON_FILE_PATH, 'w') as file:
        json.dump(tasks, file, indent=4)

def delete_tasks_from_file(task_index):
    new_data = []
    with open(JSON_FILE_PATH, 'r') as file:
        temp = json.load(file)
    i=0
    for entry in temp:   # Проходимся по json, перезаписываем файл без удаленного элемента.
        if i == int(task_index):
            pass
            i=i+1
        else:
            new_data.append(entry)
            i=i+1
    with open(JSON_FILE_PATH, 'w') as file:
        json.dump(new_data, file, indent=4)

@app.route('/tasks', methods=['GET', 'POST'])
def all_tasks():
    global TASKS
    response_object = {'status': 'success'}

    if request.method == 'POST': # Создаем новый элемент массива
        post_data = request.get_json()
        TASKS.append({
            'title': post_data.get('title'),
            'description': post_data.get('description'),
            'dateFrom': post_data.get('dateFrom'),
            'dateTo': post_data.get('dateTo')
        })
        save_tasks_to_file(TASKS)  # Сохранить данные при добавлении новой задачи
        response_object['message'] = 'Task added'
    else:
        TASKS = load_tasks_from_file()  # Загрузить данные из файла при запросе списка задач
        response_object['tasks'] = TASKS

    return jsonify(response_object)

@app.route('/tasks/<int:task_index>', methods=['PATCH'])
def update_task(task_index): # Редактирование таска
    if 0 <= task_index < len(TASKS):
        new_task = request.get_json()
        TASKS[task_index] = new_task
        save_tasks_to_file(TASKS)
        return jsonify({'status': 'success', 'message': 'Task updated'})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid task index'})

@app.route('/tasks/<int:task_index>', methods=['DELETE'])
def delete_task(task_index): # удаление
    if 0 <= task_index < len(TASKS):
        delete_tasks_from_file(task_index)
        return jsonify({'status': 'success', 'message': 'Task deleted'})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid task index'})

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify(test)

TASKS = load_tasks_from_file()

if __name__ == '__main__':
    app.run()