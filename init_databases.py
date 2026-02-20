"""
Script to initialize SQLite databases for the SQL Practice Lab.
Run this script once to create the databases with sample data.
"""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent
EXERCISES_DIR = BASE_DIR / "exercises"


def create_easy_level_db():
    """Create the employees database for Easy Level."""
    db_path = EXERCISES_DIR / "01_easy_level" / "database.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create employees table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            employee_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            salary REAL NOT NULL,
            hire_date TEXT NOT NULL
        )
    ''')
    
    # Insert sample data
    employees = [
        (1, 'John Smith', 'IT', 75000, '2020-03-15'),
        (2, 'Sarah Johnson', 'HR', 65000, '2019-07-22'),
        (3, 'Michael Brown', 'IT', 82000, '2018-01-10'),
        (4, 'Emily Davis', 'Marketing', 58000, '2021-05-03'),
        (5, 'David Wilson', 'IT', 71000, '2020-09-28'),
        (6, 'Jessica Taylor', 'HR', 62000, '2022-02-14'),
        (7, 'Robert Anderson', 'Finance', 88000, '2017-11-30'),
        (8, 'Amanda Martinez', 'Marketing', 55000, '2021-08-17'),
        (9, 'Christopher Lee', 'Finance', 92000, '2016-04-05'),
        (10, 'Jennifer Garcia', 'IT', 78000, '2019-12-01'),
    ]
    
    cursor.execute('DELETE FROM employees')
    cursor.executemany('INSERT INTO employees VALUES (?, ?, ?, ?, ?)', employees)
    
    conn.commit()
    conn.close()
    print(f"[OK] Created Easy Level database: {db_path}")


def create_medium_level_db():
    """Create the store database for Medium Level."""
    db_path = EXERCISES_DIR / "02_medium_level" / "database.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create customers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            city TEXT NOT NULL
        )
    ''')
    
    # Create products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL
        )
    ''')
    
    # Create orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    ''')
    
    # Create order_items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            item_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    ''')
    
    # Insert sample data
    customers = [
        (1, 'Alice Cooper', 'alice@email.com', 'New York'),
        (2, 'Bob Dylan', 'bob@email.com', 'Los Angeles'),
        (3, 'Charlie Parker', 'charlie@email.com', 'Chicago'),
        (4, 'Diana Ross', 'diana@email.com', 'Houston'),
        (5, 'Edward Norton', 'edward@email.com', 'Phoenix'),
    ]
    
    products = [
        (1, 'Laptop Pro', 'Electronics', 1299.99),
        (2, 'Wireless Mouse', 'Electronics', 29.99),
        (3, 'Office Chair', 'Furniture', 249.99),
        (4, 'Standing Desk', 'Furniture', 499.99),
        (5, 'Monitor 27"', 'Electronics', 349.99),
        (6, 'Keyboard', 'Electronics', 89.99),
        (7, 'Desk Lamp', 'Furniture', 45.99),
        (8, 'Webcam HD', 'Electronics', 79.99),
    ]
    
    orders = [
        (1, 1, '2024-01-15'),
        (2, 2, '2024-01-18'),
        (3, 1, '2024-01-20'),
        (4, 3, '2024-01-22'),
        (5, 4, '2024-01-25'),
        (6, 5, '2024-01-28'),
    ]
    
    order_items = [
        (1, 1, 1, 1),   # Order 1: 1 Laptop Pro
        (2, 1, 2, 2),   # Order 1: 2 Wireless Mouse
        (3, 2, 3, 1),   # Order 2: 1 Office Chair
        (4, 2, 7, 2),   # Order 2: 2 Desk Lamp
        (5, 3, 5, 1),   # Order 3: 1 Monitor
        (6, 4, 4, 1),   # Order 4: 1 Standing Desk
        (7, 4, 6, 1),   # Order 4: 1 Keyboard
        (8, 5, 1, 1),   # Order 5: 1 Laptop Pro
        (9, 5, 8, 1),   # Order 5: 1 Webcam
        (10, 6, 2, 3),  # Order 6: 3 Wireless Mouse
    ]
    
    # Clear existing data and insert new
    cursor.execute('DELETE FROM order_items')
    cursor.execute('DELETE FROM orders')
    cursor.execute('DELETE FROM products')
    cursor.execute('DELETE FROM customers')
    
    cursor.executemany('INSERT INTO customers VALUES (?, ?, ?, ?)', customers)
    cursor.executemany('INSERT INTO products VALUES (?, ?, ?, ?)', products)
    cursor.executemany('INSERT INTO orders VALUES (?, ?, ?)', orders)
    cursor.executemany('INSERT INTO order_items VALUES (?, ?, ?, ?)', order_items)
    
    conn.commit()
    conn.close()
    print(f"[OK] Created Medium Level database: {db_path}")


def create_hard_level_db():
    """Create the university database for Hard Level."""
    db_path = EXERCISES_DIR / "03_hard_level" / "database.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            enrollment_year INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS professors (
            professor_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            course_id INTEGER PRIMARY KEY,
            course_name TEXT NOT NULL,
            department TEXT NOT NULL,
            credits INTEGER NOT NULL,
            professor_id INTEGER,
            FOREIGN KEY (professor_id) REFERENCES professors(professor_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS enrollments (
            enrollment_id INTEGER PRIMARY KEY,
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            grade REAL,
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (course_id) REFERENCES courses(course_id)
        )
    ''')

    students = [
        (1, 'Anna White', 'anna@uni.edu', 2021),
        (2, 'Brian Green', 'brian@uni.edu', 2020),
        (3, 'Clara Hill', 'clara@uni.edu', 2022),
        (4, 'Derek Stone', 'derek@uni.edu', 2021),
        (5, 'Eva Moon', 'eva@uni.edu', 2023),
        (6, 'Frank Reed', 'frank@uni.edu', 2020),
        (7, 'Grace Lin', 'grace@uni.edu', 2022),
        (8, 'Henry Woods', 'henry@uni.edu', 2023),
    ]

    professors = [
        (1, 'Dr. Smith', 'Computer Science'),
        (2, 'Dr. Adams', 'Mathematics'),
        (3, 'Dr. Clark', 'Physics'),
        (4, 'Dr. Baker', 'Computer Science'),
    ]

    courses = [
        (1, 'Intro to Programming', 'Computer Science', 4, 1),
        (2, 'Data Structures', 'Computer Science', 4, 1),
        (3, 'Calculus I', 'Mathematics', 3, 2),
        (4, 'Linear Algebra', 'Mathematics', 3, 2),
        (5, 'Physics I', 'Physics', 4, 3),
        (6, 'Database Systems', 'Computer Science', 3, 4),
    ]

    enrollments = [
        (1, 1, 1, 92),
        (2, 1, 3, 88),
        (3, 1, 5, 79),
        (4, 2, 1, 75),
        (5, 2, 2, 81),
        (6, 2, 4, 70),
        (7, 3, 1, 95),
        (8, 3, 3, 91),
        (9, 4, 2, 68),
        (10, 4, 5, 72),
        (11, 4, 6, 85),
        (12, 6, 2, 88),
        (13, 6, 3, 90),
        (14, 6, 6, 93),
        (15, 7, 1, 87),
        (16, 7, 4, 82),
    ]
    # Note: students 5 (Eva) and 8 (Henry) have no enrollments

    cursor.execute('DELETE FROM enrollments')
    cursor.execute('DELETE FROM courses')
    cursor.execute('DELETE FROM professors')
    cursor.execute('DELETE FROM students')

    cursor.executemany('INSERT INTO students VALUES (?, ?, ?, ?)', students)
    cursor.executemany('INSERT INTO professors VALUES (?, ?, ?)', professors)
    cursor.executemany('INSERT INTO courses VALUES (?, ?, ?, ?, ?)', courses)
    cursor.executemany('INSERT INTO enrollments VALUES (?, ?, ?, ?)', enrollments)

    conn.commit()
    conn.close()
    print(f"[OK] Created Hard Level database: {db_path}")


if __name__ == '__main__':
    print("Initializing SQL Practice Lab databases...")
    print("")
    create_easy_level_db()
    create_medium_level_db()
    create_hard_level_db()
    print("")
    print("[OK] All databases created successfully!")
