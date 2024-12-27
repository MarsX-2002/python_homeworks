
import json

class Task:
    def __init__(self, task_id, title, description, due_date=None, status="Pending"):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.status = status

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "status": self.status
        }

    @staticmethod
    def from_dict(data):
        return Task(
            data["task_id"],
            data["title"],
            data["description"],
            data.get("due_date"),
            data.get("status", "Pending")
        )

class StorageHandler:
    def __init__(self, file_name="tasks.json"):
        self.file_name = file_name

    def save(self, tasks):
        with open(self.file_name, "w") as file:
            json.dump([task.to_dict() for task in tasks], file)

    def load(self):
        try:
            with open(self.file_name, "r") as file:
                return [Task.from_dict(data) for data in json.load(file)]
        except FileNotFoundError:
            return []

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.storage = StorageHandler()
        self.tasks = self.storage.load()

    def add_task(self, task):
        self.tasks.append(task)

    def view_tasks(self):
        for task in self.tasks:
            print(f"{task.task_id}, {task.title}, {task.description}, {task.due_date}, {task.status}")

    def update_task(self, task_id, **kwargs):
        for task in self.tasks:
            if task.task_id == task_id:
                for key, value in kwargs.items():
                    if hasattr(task, key):
                        setattr(task, key, value)
                return True
        return False

    def delete_task(self, task_id):
        self.tasks = [task for task in self.tasks if task.task_id != task_id]

    def filter_tasks(self, status):
        for task in self.tasks:
            if task.status.lower() == status.lower():
                print(f"{task.task_id}, {task.title}, {task.description}, {task.due_date}, {task.status}")

    def save_tasks(self):
        self.storage.save(self.tasks)

def main():
    manager = TaskManager()
    while True:
        print("\n1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Filter Tasks")
        print("6. Save and Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            task_id = input("Task ID: ")
            title = input("Title: ")
            description = input("Description: ")
            due_date = input("Due Date (YYYY-MM-DD): ")
            status = input("Status (Pending/In Progress/Completed): ")
            manager.add_task(Task(task_id, title, description, due_date, status))
        elif choice == "2":
            manager.view_tasks()
        elif choice == "3":
            task_id = input("Task ID to update: ")
            title = input("New Title (leave blank to keep): ")
            description = input("New Description (leave blank to keep): ")
            due_date = input("New Due Date (leave blank to keep): ")
            status = input("New Status (leave blank to keep): ")
            updates = {k: v for k, v in [("title", title), ("description", description), ("due_date", due_date), ("status", status)] if v}
            if not manager.update_task(task_id, **updates):
                print("Task not found.")
        elif choice == "4":
            task_id = input("Task ID to delete: ")
            manager.delete_task(task_id)
        elif choice == "5":
            status = input("Filter by Status (Pending/In Progress/Completed): ")
            manager.filter_tasks(status)
        elif choice == "6":
            manager.save_tasks()
            print("Tasks saved. Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
