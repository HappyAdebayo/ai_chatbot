
from database import database


def create_task(task):
    connection = database.get_connection()

    with connection:
        # Check whether a task with this title already exists
        existing_task = connection.execute("""
            SELECT id FROM tasks
            WHERE LOWER(TRIM(title)) = LOWER(TRIM(?))
        """, (task.title,)).fetchone()

        if existing_task:
            return {
                "success": False,
                "message": f"A task with the title '{task.title}' already exists."
            }

        cursor = connection.execute("""
            INSERT INTO tasks (
                title, description, date, time,
                priority, category, status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            task.title,
            task.description,
            task.date,
            task.time,
            task.priority,
            task.category,
            task.status
        ))

        task_id = cursor.lastrowid

    return {
        "success": True,
        "message": "Task created successfully.",
        "task_id": task_id
    }

def get_all_tasks(
    title=None,
    description=None,
    date=None,
    time=None,
    priority=None,
    category=None,
    status=None,
    created_at=None
):
    connection = database.get_connection()

    query = "SELECT * FROM tasks WHERE 1=1"
    values = []

    filters = {
        "title": title,
        "description": description,
        "date": date,
        "time": time,
        "priority": priority,
        "category": category,
        "status": status,
        "created_at": created_at
    }

    for column, value in filters.items():
        if value is not None:
            if column in ("title", "description"):
                query += f" AND {column} LIKE ?"
                values.append(f"%{value}%")
            else:
                query += f" AND {column} = ?"
                values.append(value)

    query += " ORDER BY created_at DESC, id DESC"

    rows = connection.execute(query, values).fetchall()

    return [dict(row) for row in rows]
    
def find_task(title):
    connection = database.get_connection()

    rows = connection.execute("""
        SELECT * FROM tasks
        WHERE title = ?
    """, (title,)).fetchall()

    if not rows:
        return None

    if len(rows) > 1:
        return {
            "ambiguous": True,
            "matches": [dict(row) for row in rows]
        }

    return dict(rows[0])

def update_task(task_update):
    task_data = task_update.model_dump(
        exclude={"title"},
        exclude_unset=True,
        exclude_none=True
    )

    if not task_data:
        return {
            "success": False,
            "message": "No fields provided for updating."
        }
    
    if "new_title" in task_data:
        task_data["title"] = task_data.pop("new_title")

    existing_task = find_task(task_update.title)

    if existing_task is None:
        return {
            "success": False,
            "message": "Task not found."
        }

    if existing_task.get("ambiguous"):
        return {
            "success": False,
            "message": "Multiple tasks found. Please identify the correct task."
        }

    fields = list(task_data.keys())
    assignments = ", ".join(
        f"{field} = ?" for field in fields
    )

    values = list(task_data.values())

    connection = database.get_connection()

    with connection:
        connection.execute(
            f"UPDATE tasks SET {assignments} WHERE id = ?",
            (*values, existing_task["id"])
        )

    return {
        "success": True,
        "message": "Task updated successfully.",
        "task_id": existing_task["id"]
    }

def delete_task(title):
    existing_task = find_task(title)

    if existing_task is None:
        return {
            "success": False,
            "message": "Task not found."
        }

    if existing_task.get("ambiguous"):
        return {
            "success": False,
            "message": "Multiple tasks found. Please identify the correct task."
        }

    connection = database.get_connection()

    with connection:
        connection.execute(
            "DELETE FROM tasks WHERE id = ?",
            (existing_task["id"],)
        )

    return {
        "success": True,
        "message": "Task deleted successfully."
    }

def delete_all_tasks(confirmed=False):
    connection = database.get_connection()

    with connection:
        task_count = connection.execute("""
            SELECT COUNT(*) FROM tasks
        """).fetchone()[0]

        if task_count == 0:
            return {
                "success": False,
                "message": "There are no tasks to delete."
            }

        if not confirmed:
            return {
                "success": False,
                "requires_confirmation": True,
                "task_count": task_count,
                "message": f"You have {task_count} tasks. Are you sure you want to delete all of them?"
            }

        connection.execute("DELETE FROM tasks")

    return {
        "success": True,
        "deleted_count": task_count,
        "message": f"Successfully deleted all {task_count} tasks."
    }

def complete_task(title):
    existing_task = find_task(title)

    if existing_task is None:
        return {
            "success": False,
            "message": "Task not found."
        }

    if existing_task.get("ambiguous"):
        return {
            "success": False,
            "message": "Multiple tasks found. Please identify the correct task."
        }

    connection = database.get_connection()

    with connection:
        connection.execute("""
            UPDATE tasks
            SET status = 'completed'
            WHERE id = ?
        """, (existing_task["id"],))

    return {
        "success": True,
        "message": "Task completed successfully."
    }

def complete_all_tasks():
    connection = database.get_connection()

    with connection:
        # Get the number of pending tasks
        task_count = connection.execute("""
            SELECT COUNT(*)
            FROM tasks
            WHERE status != 'completed'
        """).fetchone()[0]

        if task_count == 0:
            return {
                "success": False,
                "message": "There are no pending tasks to complete."
            }

        # Mark all pending tasks as completed
        connection.execute("""
            UPDATE tasks
            SET status = 'completed'
            WHERE status != 'completed'
        """)

    return {
        "success": True,
        "completed_count": task_count,
        "message": f"Successfully completed all {task_count} tasks."
    }