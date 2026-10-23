from flask import Flask, request, render_template_string

app = Flask(__name__)

employees = []

PAGE = """

<!DOCTYPE html>

<html>
<head>
    <title>Payroll System - V1</title>
</head>
<body>
    <h1>Payroll System - V1</h1>
    <h2>Add Employee Salary</h2>

```
<form method="POST" action="/add">
    <label>Employee ID:</label>
    <input type="text" name="employee_id" required>
    <br><br>

    <label>Employee Name:</label>
    <input type="text" name="name" required>
    <br><br>

    <label>Basic Salary (₹):</label>
    <input type="number" name="basic_salary"
           min="0" step="0.01" required>
    <br><br>

    <button type="submit">Add Employee</button>
</form>

<h2>Employees</h2>

{% if employees %}
    <table border="1" cellpadding="8">
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Basic Salary</th>
        </tr>

        {% for e in employees %}
        <tr>
            <td>{{ e["employee_id"] }}</td>
            <td>{{ e["name"] }}</td>
            <td>₹{{ "%.2f"|format(e["basic_salary"]) }}</td>
        </tr>
        {% endfor %}
    </table>
{% else %}
    <p>No employees added yet.</p>
{% endif %}
```

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(PAGE, employees=employees)

@app.route("/add", methods=["POST"])
def add_employee():
    employee_id = request.form["employee_id"].strip()
    name = request.form["name"].strip()
    salary_text = request.form["basic_salary"]

    try:
        basic_salary = float(salary_text)
    except ValueError:
        return "Please enter a valid salary.", 400

    if basic_salary < 0:
        return "Salary cannot be negative.", 400

    for e in employees:
        if e["employee_id"] == employee_id:
            return "Employee ID already exists.", 400

    employees.append({
        "employee_id": employee_id,
        "name": name,
        "basic_salary": basic_salary
    })

    return render_template_string(PAGE, employees=employees)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
