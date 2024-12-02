from flask import Flask, render_template, request
import psycopg2
import os
import logging

app = Flask(__name__)

# PostgreSQL connection setup
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "postgres")

# Query folder path
QUERY_FOLDER = "queries"

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def get_db_connection():
    """Establish and return a database connection."""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME
    )

def load_queries(folder):
    queries = {}
    for filename in sorted(os.listdir(folder)):
        if filename.endswith('.sql'):
            query_name = os.path.splitext(filename)[0]
            # Ensure proper handling of filenames with or without underscores.
            title = ' '.join(word.capitalize() for word in query_name.split('_'))
            with open(os.path.join(folder, filename), 'r') as file:
                queries[query_name] = {'title': title, 'sql': file.read()}
    return queries

def execute_query(query, params=None):
    """Execute a query with optional parameters and return its result."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            return columns, rows
    finally:
        conn.close()

    
@app.route('/', methods=['GET', 'POST'])
def index():
    """Render the main page with performance metrics."""
    logging.info("Rendering the index page...")

    # Load available snapshots
    snapshots_query = """
        SELECT snap_id, snap_timestamp 
        FROM statspack.hist_snapshots 
        ORDER BY snap_id;
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(snapshots_query)
            snapshots = cursor.fetchall()
        logging.info(f"Snapshots loaded: {snapshots}")
    except Exception as e:
        logging.error(f"Error fetching snapshots: {e}")
        snapshots = []
    finally:
        conn.close()

    # Handle snapshot selection
    begin_snap = request.form.get('begin_snap')
    end_snap = request.form.get('end_snap')
    logging.info(f"Selected snapshots - Begin: {begin_snap}, End: {end_snap}")

    # Load queries and execute them with snapshot parameters
    queries = load_queries(QUERY_FOLDER)  # Adjusted loader to return dict with title & sql
    query_results = {}

    if request.method == 'POST' and begin_snap and end_snap:
        try:
            for query_name, query_data in queries.items():
                query_title = query_data['title']
                query_sql = query_data['sql']
                logging.info(f"Executing query: {query_name}")
                columns, rows = execute_query(query_sql, params={'begin_snap': begin_snap, 'end_snap': end_snap})
                query_results[query_name] = {"title": query_title, "columns": columns, "rows": rows}
                logging.info(f"Query result for {query_name}: {len(rows)} rows")
        except Exception as e:
            logging.error(f"Error executing queries: {e}")
    # Pass selected snapshots to the template for display.
    return render_template(
            'report.html',
            selected_snapshots={
                'begin_snap': begin_snap,
                'end_snap': end_snap,
            },

            snapshots=snapshots,
            queries=query_results,
            begin_snap=begin_snap,
            end_snap=end_snap
        )

if __name__ == '__main__':
    app.run(debug=True)
