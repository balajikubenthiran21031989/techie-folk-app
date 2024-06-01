import os
from flask import Flask, request, render_template
import pymysql

app = Flask(__name__)

# Database connection details from environment variables
DB_ENDPOINT = os.getenv('DB_ENDPOINT')
DB_PORT = os.getenv('DB_PORT')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

def get_db_connection():
    connection = pymysql.connect(host=DB_ENDPOINT,
                                 port=int(DB_PORT),
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
