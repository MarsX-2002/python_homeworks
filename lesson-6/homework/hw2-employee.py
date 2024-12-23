FILE_NAME = "employees.txt"

# task 1
def add_employee_record():
    """Add new employee record."""
    with open(FILE_NAME, "a") as file:
        emp_id = input("Enter Employee ID (unique): ")
        name = input("Enter Name: ")
        position = input("Enter Position: ")
        salary = input("Enter Salary: ")

        # input format
        record = f"{emp_id}, {name}, {position}, {salary}\n"
        file.write(record)
        print("Employee record added successfully!\n")


# task 2
def view_all_records():
    """View all employee records."""
    try:
        with open(FILE_NAME, "r") as file:
            records = file.readlines()  # Read all lines 

        if not records or all(record.strip() == "" for record in records):
            print("No employee records found.\n")
        else:
            print("\nEmployee Records:")
            for record in records:
                record = record.strip()  # Remove extra whitespace.
                if record:  # Only print non-empty lines.
                    print(record)
            print()
    except FileNotFoundError:
        print("No employee records found. File does not exist.\n")



def search_employee():
    """Search for an employee by ID."""
    emp_id = input("Enter Employee ID to search: ")
    found = False

    try:
        with open(FILE_NAME, "r") as file:
            for record in file:
                if record.startswith(emp_id + ","):
                    print("Employee Found:", record.strip(), "\n")
                    found = True
                    break

        if not found:
            print(f"No employee found with ID: {emp_id}\n")
    except FileNotFoundError:
        print("No employee records found.\n")

def update_employee_record():
    """Update an employee's information."""
    emp_id = input("Enter Employee ID to update: ")
    updated_records = []
    found = False

    try:
        with open(FILE_NAME, "r") as file:
            for record in file:
                if record.startswith(emp_id + ","):
                    print("Current Record:", record.strip())
                    name = input("Enter new Name (leave blank to keep current): ") or record.split(", ")[1]
                    position = input("Enter new Position (leave blank to keep current): ") or record.split(", ")[2]
                    salary = input("Enter new Salary (leave blank to keep current): ") or record.split(", ")[3].strip()
                    updated_records.append(f"{emp_id}, {name}, {position}, {salary}\n")
                    found = True
                else:
                    updated_records.append(record)

        with open(FILE_NAME, "w") as file:
            file.writelines(updated_records)

        if found:
            print("Employee record updated successfully!\n")
        else:
            print(f"No employee found with ID: {emp_id}\n")
    except FileNotFoundError:
        print("No employee records found.\n")

def delete_employee_record():
    """Delete an employee's record."""
    emp_id = input("Enter Employee ID to delete: ")
    updated_records = []
    found = False

    try:
        with open(FILE_NAME, "r") as file:
            for record in file:
                if record.startswith(emp_id + ","):
                    print("Deleting Record:", record.strip())
                    found = True
                else:
                    updated_records.append(record)

        with open(FILE_NAME, "w") as file:
            file.writelines(updated_records)

        if found:
            print("Employee record deleted successfully!\n")
        else:
            print(f"No employee found with ID: {emp_id}\n")
    except FileNotFoundError:
        print("No employee records found.\n")

# Menu
while True:
    print("Employee Records Manager")
    print("1. Add new employee record")
    print("2. View all employee records")
    print("3. Search for an employee by Employee ID")
    print("4. Update an employee's information")
    print("5. Delete an employee record")
    print("6. Exit")

    print('>>>', sep='')

    choice = input("Enter your choice: ")

    if choice == "1":
        add_employee_record()
    elif choice == "2":
        view_all_records()
    elif choice == "3":
        search_employee()
    elif choice == "4":
        update_employee_record()
    elif choice == "5":
        delete_employee_record()
    elif choice == "6":
        print("Exiting the program. Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.\n")
