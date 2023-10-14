from flask import Flask, request, render_template
import pymysql

app = Flask(__name__)

# RDS Database Configuration
db_host = 'xxxxxxx.ap-south-1.rds.amazonaws.com'
db_user = 'root'
db_password = 'pwdxxxxx'
db_name = 'lab5_db'
#mysql -h lab5cc.curnbwpvlyma.ap-south-1.rds.amazonaws.com -u root -p
#for beanstalk,replace file name with application everywhere.
# and in website.zipadd a file name eb_extensions with all import versions.

# Function to connect to the database
def connect_to_db():
    return pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)

# Create the 'feedback' table if it doesn't exist
def create_feedback_table():
    try:
        connection = connect_to_db()
        with connection.cursor() as cursor:
            # Create the 'feedback' table if it doesn't exist
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS feedback (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                message TEXT NOT NULL
            )
            """
            cursor.execute(create_table_sql)
            connection.commit()
    except Exception as e:
        print(f'Error creating table: {str(e)}')
    finally:
        connection.close()

# Display the feedback form
@app.route('/')
def feedback_form():
    return render_template('index.html')

# Handle form submission and store feedback in the database
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    name = request.form['name']
    message = request.form['message']

    try:
        connection = connect_to_db()
        with connection.cursor() as cursor:
            # Insert the feedback into the database
            sql = "INSERT INTO feedback (name, message) VALUES (%s, %s)"
            cursor.execute(sql, (name, message))
            connection.commit()
            return 'Feedback submitted successfully!'
    except Exception as e:
        return f'Error: {str(e)}'
    finally:
        connection.close()

if __name__ == '__main__':
    create_feedback_table()  # Create the 'feedback' table on application start
    app.run(debug=True,port=80,host='0.0.0.0')
