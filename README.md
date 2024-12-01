# aurora-statspack-ui
Web interface for Aurora Statspack report


Local testing

Clone the repository into your machine and execute:

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export DB_HOST="your_hostname" 
export DB_PORT="your_port" 
export DB_USER="your_user" 
export DB_PASSWORD="your_pass" 
export DB_NAME="your_dbname"
python3 statspack_app.py

You can access Statspack Report now in: http://localhost:5000


Docker deployment

Clone the repository into your machine and execute:

docker build -t statspack_app .

docker run --rm -it \
  -e DB_HOST="your_hostname" \
  -e DB_PORT="your_port" \
  -e DB_USER="your_user" \
  -e DB_PASSWORD="your_pass" \
  -e DB_NAME="your_dbname" \
  -v $(pwd)/logs:/app/logs \
  -p 5000:5000 \
  statspack_app python3 /app/statspack_app.py

You can access Statspack Report now in: http://localhost:5000




# aurora-statspack-ui
A web interface for Aurora Statspack reports.

---

## 🚀 Local Testing

To test the application locally, follow these steps:

### 1. Clone the repository:
```bash
git clone https://github.com/yourusername/aurora-statspack-ui.git
cd aurora-statspack-ui
```
2. Set up a Python virtual environment:
bash
Copy code
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
3. Install the required dependencies:
bash
Copy code
pip install -r requirements.txt
4. Configure your database connection:
Set the following environment variables with your database connection details:

export DB_HOST="your_hostname"
export DB_PORT="your_port"
export DB_USER="your_user"
export DB_PASSWORD="your_pass"
export DB_NAME="your_dbname"
5. Start the application:
bash
Copy code
python3 statspack_app.py
You can now access the Statspack Report at:

http://localhost:5000

🐳 Docker Deployment
To deploy the application using Docker, follow these steps:

1. Clone the repository:

git clone https://github.com/yourusername/aurora-statspack-ui.git
cd aurora-statspack-ui

2. Build the Docker image:

docker build -t statspack_app .

3. Run the Docker container:

Ensure to replace the environment variables with your actual database connection details.

docker run --rm -it \
  -e DB_HOST="your_hostname" \
  -e DB_PORT="your_port" \
  -e DB_USER="your_user" \
  -e DB_PASSWORD="your_pass" \
  -e DB_NAME="your_dbname" \
  -v $(pwd)/logs:/app/logs \
  -p 5000:5000 \
  statspack_app python3 /app/statspack_app.py
You can now access the Statspack Report at:

http://localhost:5000

📝 Notes
The application is accessible at http://localhost:5000 by default.
The database connection details can be set via environment variables or by modifying the statspack_app.py file.
Logs will be saved in the logs directory of the repository. Ensure you mount the volume (-v $(pwd)/logs:/app/logs) when running in Docker to persist logs.
📜 License
This project is licensed under the MIT License - see the LICENSE file for details.

