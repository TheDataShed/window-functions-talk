import csv
import os


SESSION_TIMEOUT_SECS = 1800

CSV_FILE = "employees.csv"

base_dir = os.path.dirname(os.path.dirname(__file__))
file_path = os.path.join(base_dir, "data", CSV_FILE)


def read_employees() -> list[dict]:
    with open(file_path) as f:
        csv_reader = csv.DictReader(f)
        employees = list(csv_reader)
    # Convert int fields from strings
    return [{
        "first_name": employee["first_name"],
        "last_name": employee["last_name"],
        "email": employee["email"],
        "phone": employee["phone"],
        "department": employee["department"],
        "job_title": employee["job_title"],
        "experience_years": int(employee["experience_years"]),
        "salary": int(employee["salary"]),
    } for employee in employees]

def rank_employees(employees):
    ranked = sorted(employees, key=lambda employee: employee['salary'])
    for e in ranked:
        print(e["salary"])

if __name__ == "__main__":
    employees = read_employees()
    rank_employees(employees)
