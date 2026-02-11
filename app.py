from flask import Flask, render_template, jsonify, request
import sqlite3
import os
import json
from pathlib import Path

app = Flask(__name__)
BASE_DIR = Path(__file__).parent
EXERCISES_DIR = BASE_DIR / "exercises"


def get_db_connection(db_path):
    """Create a connection to the SQLite database."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def get_table_structure(db_path):
    """Get the structure of all tables in the database."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    
    structure = []
    for table in tables:
        table_name = table['name']
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        structure.append({
            'name': table_name,
            'columns': [{'name': col['name'], 'type': col['type'], 'pk': col['pk']} for col in columns]
        })
    
    conn.close()
    return structure


def load_exercises():
    """Load all exercise folders and their tasks."""
    exercises = []
    
    if not EXERCISES_DIR.exists():
        return exercises
    
    for folder in sorted(EXERCISES_DIR.iterdir()):
        if folder.is_dir():
            config_path = folder / "config.json"
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                tasks = []
                tasks_dir = folder / "tasks"
                if tasks_dir.exists():
                    for task_file in sorted(tasks_dir.glob("*.json")):
                        with open(task_file, 'r', encoding='utf-8') as f:
                            task_data = json.load(f)
                            task_data['id'] = task_file.stem
                            tasks.append(task_data)
                
                exercises.append({
                    'id': folder.name,
                    'name': config.get('name', folder.name),
                    'difficulty': config.get('difficulty', 'unknown'),
                    'tasks': tasks
                })
    
    return exercises


@app.route('/')
def index():
    """Render the main application page."""
    return render_template('index.html')


@app.route('/api/exercises')
def get_exercises():
    """Get all exercise folders with their tasks."""
    exercises = load_exercises()
    return jsonify(exercises)


@app.route('/api/task/<folder_id>/<task_id>')
def get_task(folder_id, task_id):
    """Get details of a specific task."""
    folder_path = EXERCISES_DIR / folder_id
    task_path = folder_path / "tasks" / f"{task_id}.json"
    
    if not task_path.exists():
        return jsonify({'error': 'Task not found'}), 404
    
    with open(task_path, 'r', encoding='utf-8') as f:
        task_data = json.load(f)
    
    # Get database structure
    db_path = folder_path / "database.db"
    structure = get_table_structure(db_path) if db_path.exists() else []
    
    return jsonify({
        'task': task_data,
        'db_structure': structure
    })


@app.route('/api/execute', methods=['POST'])
def execute_query():
    """Execute a SQL query and return results."""
    data = request.json
    folder_id = data.get('folder_id')
    query = data.get('query', '').strip()
    
    if not folder_id or not query:
        return jsonify({'error': 'Missing folder_id or query'}), 400
    
    db_path = EXERCISES_DIR / folder_id / "database.db"
    
    if not db_path.exists():
        return jsonify({'error': 'Database not found'}), 404
    
    try:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        cursor.execute(query)
        
        # Get column names
        columns = [description[0] for description in cursor.description] if cursor.description else []
        
        # Get rows
        rows = cursor.fetchall()
        results = [dict(row) for row in rows]
        
        conn.close()
        
        return jsonify({
            'success': True,
            'columns': columns,
            'rows': results,
            'row_count': len(results)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route('/api/verify', methods=['POST'])
def verify_solution():
    """Verify if the user's solution matches the expected result."""
    data = request.json
    folder_id = data.get('folder_id')
    task_id = data.get('task_id')
    user_query = data.get('query', '').strip()
    
    if not all([folder_id, task_id, user_query]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Load task to get expected solution
    task_path = EXERCISES_DIR / folder_id / "tasks" / f"{task_id}.json"
    if not task_path.exists():
        return jsonify({'error': 'Task not found'}), 404
    
    with open(task_path, 'r', encoding='utf-8') as f:
        task_data = json.load(f)
    
    expected_query = task_data.get('solution', '')
    
    db_path = EXERCISES_DIR / folder_id / "database.db"
    if not db_path.exists():
        return jsonify({'error': 'Database not found'}), 404
    
    try:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        
        # Execute user query
        cursor.execute(user_query)
        user_results = [dict(row) for row in cursor.fetchall()]
        
        # Execute expected query
        cursor.execute(expected_query)
        expected_results = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        # Compare results (order matters)
        is_correct = user_results == expected_results
        
        return jsonify({
            'success': True,
            'correct': is_correct,
            'message': 'Correct! Great job! ✓' if is_correct else 'Incorrect. Try again!'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'correct': False,
            'error': str(e),
            'message': f'Error: {str(e)}'
        })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
