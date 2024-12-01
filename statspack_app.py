from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os
import re

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

# Function to fetch snapshot IDs
def fetch_snapshots():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute("SELECT snap_id, snap_timestamp FROM statspack.hist_snapshots ORDER BY snap_id DESC;")
        snapshots = cursor.fetchall()
        cursor.close()
        conn.close()
        return snapshots
    except Exception as e:
        print(f"Error fetching snapshots: {e}")
        return []

# Function to execute SQL queries and handle multiple results
def execute_sql_query(begin_snap, end_snap):
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
            sql_script = sql_file.read()

        # Remove PostgreSQL meta-commands (lines starting with '\')
        sql_script = "\n".join(
            line for line in sql_script.splitlines() if not line.strip().startswith("\\")
        )

        # Substitute variables with actual values
        sql_script = re.sub(r":BEGIN_SNAP", str(begin_snap), sql_script)
        sql_script = re.sub(r":END_SNAP", str(end_snap), sql_script)

        # Split the SQL script into individual queries
        queries = [q.strip() for q in sql_script.split(";") if q.strip()]

        all_results = []
        for query in queries:
            cursor.execute(query)
            if cursor.description:  # Fetch results only for SELECT queries
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                all_results.append({"columns": columns, "rows": rows})

        cursor.close()
        conn.close()

        return all_results
    except Exception as e:
        print(f"Error executing SQL queries: {e}")
        return None


# Route to display the snapshot selection form
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        begin_snap = request.form.get("begin_snap")
        end_snap = request.form.get("end_snap")
        return redirect(url_for("report", begin_snap=begin_snap, end_snap=end_snap))
    
    snapshots = fetch_snapshots()
    return render_template("index.html", snapshots=snapshots)

# Route to display the report
@app.route("/report", methods=["GET", "POST"])
def report():
    try:
        # Fetching the parameters from the GET or POST request
        begin_snap = request.args.get("begin_snap") or request.form.get("begin_snap")
        end_snap = request.args.get("end_snap") or request.form.get("end_snap")

        # Validate input parameters
        if not begin_snap or not end_snap:
            return render_template("error.html", message="Both BEGIN_SNAP and END_SNAP must be provided.")

        # Convert to integers to ensure valid input
        try:
            begin_snap = int(begin_snap)
            end_snap = int(end_snap)
        except ValueError:
            return render_template("error.html", message="BEGIN_SNAP and END_SNAP must be valid integers.")

        # Call the function with the required arguments
        all_results = execute_sql_query(begin_snap, end_snap)
        if not all_results:
            return render_template("error.html", message="No data available to display.")

        # Pass the results to the HTML template
        return render_template("report.html", all_results=all_results, style=HTML_STYLE)
    except Exception as e:
        print(f"Error: {e}")
        return render_template("error.html", message="An unexpected error occurred. Check the logs for details.")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
