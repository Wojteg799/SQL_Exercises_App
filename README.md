# SQL Practice Lab

A simple app to practice SQL. Pick an exercise, write your query, and check if it's correct.

Runs locally in the browser using Python + Flask + SQLite. No account, no internet required.

## How to run

```bash
pip install flask
python init_databases.py
python app.py
```

Open http://127.0.0.1:5000

## Exercises

**Easy Level** — single table (`employees`): 8 tasks
- SELECT, WHERE, COUNT, AVG, ORDER BY, GROUP BY, LIMIT

**Medium Level** — multiple tables (`customers`, `products`, `orders`, `order_items`): 12 tasks
- JOIN, LEFT JOIN, GROUP BY + HAVING, subqueries, COALESCE, correlated subqueries

**Hard Level** — university database (`students`, `professors`, `courses`, `enrollments`): 7 tasks
- Multi-table JOINs, correlated subqueries, COUNT DISTINCT, ROUND, complex HAVING

27 tasks total.

## Adding new exercises

1. Create a folder in `exercises/` (e.g. `04_expert_level/`)
2. Add `config.json`:
   ```json
   {
     "name": "Expert Level",
     "difficulty": "hard"
   }
   ```
3. Add a `database.db` (SQLite) with your tables
4. Add JSON task files in `tasks/`:
   ```json
   {
     "title": "Task Name",
     "description": "What to do",
     "hint": "Optional hint",
     "solution": "SELECT correct FROM answer"
   }
   ```

## Stack

Python, Flask, SQLite, vanilla JS. Dark theme, green accents.
