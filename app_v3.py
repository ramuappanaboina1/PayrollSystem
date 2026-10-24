from flask import Flask, request
from datetime import datetime
from html import escape

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def payslip():

    if request.method == "POST":
        emp_id = escape(request.form["emp_id"].strip())
        name = escape(request.form["name"].strip())
        department = escape(request.form["department"].strip())
        month = escape(request.form["month"])

        try:
            basic = float(request.form["basic"])
            allowance = float(request.form["allowance"])
            bonus = float(request.form["bonus"])
            deductions = float(request.form["deductions"])

            if min(basic, allowance, bonus, deductions) < 0:
                return "Salary amounts cannot be negative.", 400

        except ValueError:
            return "Please enter valid salary amounts.", 400

        gross = basic + allowance + bonus
        net = gross - deductions
        payslip_no = "PAY-" + datetime.now().strftime("%Y%m%d%H%M%S")

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>V3 Employee Payslip</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background: #eef2f7;
                    padding: 25px;
                }}

                .container {{
                    max-width: 750px;
                    margin: auto;
                    background: white;
                    padding: 30px;
                    border-radius: 12px;
                    box-shadow: 0 3px 12px #ccc;
                }}

                .header {{
                    text-align: center;
                    border-bottom: 3px solid #243b55;
                    padding-bottom: 15px;
                }}

                .header h1 {{
                    color: #243b55;
                }}

                .details {{
                    margin: 20px 0;
                }}

                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 15px;
                }}

                th, td {{
                    border: 1px solid #ddd;
                    padding: 12px;
                    text-align: left;
                }}

                th {{
                    background: #243b55;
                    color: white;
                }}

                .total {{
                    font-weight: bold;
                    background: #e5f7e9;
                }}

                .net {{
                    background: #243b55;
                    color: white;
                    font-size: 20px;
                    font-weight: bold;
                }}

                button {{
                    padding: 12px 22px;
                    margin: 8px;
                    border: none;
                    border-radius: 5px;
                    background: #243b55;
                    color: white;
                    cursor: pointer;
                }}

                .actions {{
                    text-align: center;
                    margin-top: 25px;
                }}

                @media print {{
                    body {{
                        background: white;
                        padding: 0;
                    }}

                    .container {{
                        box-shadow: none;
                    }}

                    .actions {{
                        display: none;
                    }}
                }}
            </style>
        </head>

        <body>
            <div class="container">
                <div class="header">
                    <h1>ABC TECHNOLOGIES</h1>
                    <p>Employee Payroll Department</p>
                    <h2>EMPLOYEE PAYSLIP</h2>
                </div>

                <div class="details">
                    <p><strong>Payslip Number:</strong> {payslip_no}</p>
                    <p><strong>Employee ID:</strong> {emp_id}</p>
                    <p><strong>Employee Name:</strong> {name}</p>
                    <p><strong>Department:</strong> {department}</p>
                    <p><strong>Salary Month:</strong> {month}</p>
                    <p><strong>Generated Date:</strong>
                    {datetime.now().strftime("%d-%m-%Y")}</p>
                </div>

                <table>
                    <tr>
                        <th>Earnings</th>
                        <th>Amount (₹)</th>
                    </tr>
                    <tr>
                        <td>Basic Salary</td>
                        <td>₹{basic:,.2f}</td>
                    </tr>
                    <tr>
                        <td>Allowances</td>
                        <td>₹{allowance:,.2f}</td>
                    </tr>
                    <tr>
                        <td>Bonus</td>
                        <td>₹{bonus:,.2f}</td>
                    </tr>
                    <tr class="total">
                        <td>Total Earnings</td>
                        <td>₹{gross:,.2f}</td>
                    </tr>
                </table>

                <table>
                    <tr>
                        <th>Deductions</th>
                        <th>Amount (₹)</th>
                    </tr>
                    <tr>
                        <td>Total Deductions</td>
                        <td>₹{deductions:,.2f}</td>
                    </tr>
                </table>

                <table>
                    <tr class="net">
                        <td>NET SALARY</td>
                        <td>₹{net:,.2f}</td>
                    </tr>
                </table>

                <div class="actions">
                    <button onclick="window.print()">
                        Print / Save as PDF
                    </button>

                    <button onclick="window.location.href='/'">
                        Generate Another Payslip
                    </button>
                </div>

                <p style="text-align:center; margin-top:25px;">
                    Generated by Payroll System V3
                </p>
            </div>
        </body>
        </html>
        """

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>V3 Payslip Generator</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #eef2f7;
                padding: 25px;
            }

            form {
                max-width: 450px;
                margin: auto;
                padding: 25px;
                background: white;
                border-radius: 12px;
                box-shadow: 0 3px 12px #ccc;
            }

            h1, h2 {
                text-align: center;
                color: #243b55;
            }

            label {
                display: block;
                margin-top: 12px;
                font-weight: bold;
            }

            input {
                width: 100%;
                padding: 10px;
                margin-top: 5px;
                box-sizing: border-box;
            }

            button {
                width: 100%;
                padding: 12px;
                margin-top: 20px;
                background: #243b55;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
        </style>
    </head>

    <body>
        <form method="POST">
            <h1>ABC TECHNOLOGIES</h1>
            <h2>Generate Employee Payslip</h2>

            <label>Employee ID</label>
            <input type="text" name="emp_id" required>

            <label>Employee Name</label>
            <input type="text" name="name" required>

            <label>Department</label>
            <input type="text" name="department" required>

            <label>Salary Month</label>
            <input type="month" name="month" required>

            <label>Basic Salary (₹)</label>
            <input type="number" name="basic"
                   min="0" step="0.01" required>

            <label>Allowances (₹)</label>
            <input type="number" name="allowance"
                   min="0" step="0.01" required>

            <label>Bonus (₹)</label>
            <input type="number" name="bonus"
                   min="0" step="0.01" value="0" required>

            <label>Deductions (₹)</label>
            <input type="number" name="deductions"
                   min="0" step="0.01" required>

            <button type="submit">Generate Payslip</button>
        </form>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=False)