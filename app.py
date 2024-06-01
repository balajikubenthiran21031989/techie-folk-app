import os
from flask import Flask, request, render_template
import pymysql

app = Flask(__name__)

# Database connection details from environment variables
DB_ENDPOINT = os.getenv('techie-folks-db.cnkdkk5u04j4.us-east-1.rds.amazonaws.com')  # Update with your actual DB endpoint from DATABASE_URL
DB_USERNAME = os.getenv('techie_folks')  # Update with your actual DB username from DATABASE_URL
DB_PASSWORD = os.getenv('techie119147#')  # Update with your actual DB password from DATABASE_URL
DB_NAME = os.getenv('techie_db')  # Update with your actual DB name from DATABASE_URL
DB_PORT = os.getenv('3306')  # Update with your actual DB port number from DATABASE_URL

def get_db_connection():
    connection = pymysql.connect(host=DB_ENDPOINT,
                                 port=DB_PORT,
                                 user=DB_USERNAME,
                                 password=DB_PASSWORD,
                                 db=DB_NAME,
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    phone = request.form['phone']
    address = request.form['address']
    description = request.form['description']

    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = """
        INSERT INTO users (first_name, last_name, email, phone, address, description) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (first_name, last_name, email, phone, address, description))
    connection.commit()
    connection.close()

    return 'Form Submitted Successfully!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
