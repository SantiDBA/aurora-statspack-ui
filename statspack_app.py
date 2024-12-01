from flask import Flask, render_template, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# PostgreSQL connection setup
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "postgres")

# SQL script path
SQL_SCRIPT_PATH = "statspack_report_2_0.sql"

# HTML Table styling
HTML_STYLE = """
    <style>
        table {
            width: 80%;
            margin: 20px auto;
            border-collapse: collapse;
        }
        th, td {
            padding: 12px;
            text-align: center;
            border: 1px solid #ddd;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        tr:nth-child(odd) {
            background-color: #e9f7df;
        }
        tr:hover {
            background-color: #ddd;
        }
    </style>
"""

# Function to execute SQL query
def execute_sql_query():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME
        )
        cursor = conn.cursor()

        # Read and preprocess the SQL script
        with open(SQL_SCRIPT_PATH, "r") as sql_file:
            sql_lines = sql_file.readlines()

        # Filter out lines that start with a backslash or are comments
        filtered_sql = "\n".join(line for line in sql_lines if not line.strip().startswith("\\") and not line.strip().startswith("--"))
        print(f"Executing SQL:\n{filtered_sql}")  # Debugging output

        # Execute the preprocessed SQL
        cursor.execute(filtered_sql)
        columns = [desc[0] for desc in cursor.description]
        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return columns, results
    except Exception as e:
        print(f"Error executing SQL query: {e}")
        return None, None


# Route to display the report
@app.route("/report")
def report():
    try:
        columns, results = execute_sql_query()
        if not results:
            return render_template("error.html", message="No data available to display.")
        return render_template("report.html", columns=columns, rows=results)
    except Exception as e:
        print(f"Error: {e}")
        return "An unexpected error occurred. Check the logs for details.", 500


@app.route("/test_db")
def test_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME
        )
        conn.close()
        return "Database connection successful!"
    except Exception as e:
        return f"Database connection failed: {e}"

@app.route('/')
def index():
    return '<h1>Welcome to the Statspack App!</h1><p>Go to <a href="/report">/report</a> to view the report.</p>'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
