
from flask import Flask, request, render_template_string

app = Flask(__name__)

PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Payroll System V2</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f0f2f5;
            padding: 30px;
            text-align: center;
        }

        .box {
            background: white;
            max-width: 430px;
            margin: auto;
            padding: 25px;
            border-radius: 10px;
        }

        input, button {
            box-sizing: border-box;
            width: 100%;
            padding: 12px;
            margin: 8px 0;
        }

        button {
            background: #1769aa;
            color: white;
            border: none;
            cursor: pointer;
        }

        .result {
            background: #e0f2e9;
            padding: 15px;
            overflow-wrap: anywhere;
        }

        .error {
            color: #b00020;
        }
    </style>
</head>
<body>
<div class="box">
    <h1>Payroll System V2</h1>
    <h3>Calculate Employee Salary</h3>

    <form method="POST">
        <input name="employee_id" placeholder="Employee ID" required>
        <input name="name" placeholder="Employee Name" required>

        <input name="basic" type="number" min="0" step="0.01"
               placeholder="Basic Salary (₹)" required>

        <input name="allowance" type="number" min="0" step="0.01"
               placeholder="Allowances (₹)" value="0" required>

        <input name="deduction" type="number" min="0" step="0.01"
               placeholder="Deductions (₹)" value="0" required>

        <button type="submit">Calculate Salary</button>
    </form>

    {% if result %}
    <div class="result">
        <h3>Salary Details</h3>
        <p>Employee ID: {{ result.employee_id }}</p>
        <p>Name: {{ result.name }}</p>
        <p>Basic Salary: ₹{{ "%.2f"|format(result.basic) }}</p>
        <p>Allowances: ₹{{ "%.2f"|format(result.allowance) }}</p>
        <p>Gross Salary: ₹{{ "%.2f"|format(result.gross) }}</p>
        <p>Deductions: ₹{{ "%.2f"|format(result.deduction) }}</p>
        <h3>Net Salary: ₹{{ "%.2f"|format(result.net) }}</h3>
    </div>
    {% endif %}

    {% if error %}
    <p class="error">{{ error }}</p>
    {% endif %}
</div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def calculate_salary():
    result = None
    error = None

    if request.method == "POST":
        try:
            employee_id = request.form["employee_id"].strip()
            name = request.form["name"].strip()
            basic = float(request.form["basic"])
            allowance = float(request.form["allowance"])
            deduction = float(request.form["deduction"])

            if not employee_id or not name:
                raise ValueError("Employee ID and name are required.")

            if basic < 0 or allowance < 0 or deduction < 0:
                raise ValueError("Salary amounts cannot be negative.")

            gross = basic + allowance

            if deduction > gross:
                raise ValueError(
                    "Deductions cannot exceed gross salary."
                )

            net = gross - deduction

            result = {
                "employee_id": employee_id,
                "name": name,
                "basic": basic,
                "allowance": allowance,
                "gross": gross,
                "deduction": deduction,
                "net": net
            }

        except (ValueError, KeyError) as exc:
            error = str(exc) or "Please enter valid salary values."

    return render_template_string(PAGE, result=result, error=error)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=False)

