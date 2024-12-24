import sqlite3
import os

# Connect to SQLite database
conn = sqlite3.connect('todo_list.db')
# Check if the database file exists, if not create it
if not os.path.exists('todo_list.db'):
    open('todo_list.db', 'w').close()
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS todos
             (id INTEGER PRIMARY KEY, task TEXT, status TEXT)''')

# Function to add a new task
def add_task(task):
    c.execute("INSERT INTO todos (task, status) VALUES (?, ?)", (task, 'pending'))
    conn.commit()

# Function to list all tasks
def list_tasks():
    c.execute("SELECT * FROM todos")
    tasks = c.fetchall()
    for task in tasks:
        print(task)

# Function to update task status
def update_task(task_id, status):
    c.execute("UPDATE todos SET status = ? WHERE id = ?", (status, task_id))
    conn.commit()

# Function to delete a task
def delete_task(task_id):
    c.execute("DELETE FROM todos WHERE id = ?", (task_id,))
    conn.commit()

# Close the connection
def close_connection():
    conn.close()

# Main function to handle user input
def main():
    while True:
        print("\nOptions:")
        print("1. Add task")
        print("2. List tasks")
        print("3. Update task")
        print("4. Delete task")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            task = input("Enter the task: ")
            add_task(task)
        elif choice == '2':
            list_tasks()
        elif choice == '3':
            task_id = int(input("Enter the task ID to update: "))
            status = input("Enter the new status: ")
            update_task(task_id, status)
        elif choice == '4':
            task_id = int(input("Enter the task ID to delete: "))
            delete_task(task_id)
        elif choice == '5':
            close_connection()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()