from flask import Flask, request, render_template
import pymysql
import json

app = Flask(__name__)

# Replace these with your Amazon RDS instance credentials and connection details
db_host = 'xxxxxxxx.ap-south-1.rds.amazonaws.com'
db_user = 'root'
db_password = 'pwdxxxxx'
db_name = 'lab5_db'

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
            CREATE TABLE IF NOT EXISTS feedfront (
                id INT AUTO_INCREMENT PRIMARY KEY,
                stars VARCHAR(255) NOT NULL,
                category VARCHAR(255) NOT NULL,
                feedback_text VARCHAR(255) NOT NULL
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
    return render_template('feedback.html')

# Handle form submission and store feedback in the database
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    feedback_data = request.form.get('feedbackData')
    # Parse the JSON data
    feedback_data = json.loads(feedback_data)
    
    # Extract the values
    stars = feedback_data['stars']
    category = feedback_data['category']
    feedback_text = feedback_data['feedbackText']

    try:
        connection = connect_to_db()
        with connection.cursor() as cursor:
            # Insert the feedback into the database
            sql = "INSERT INTO feedfront (stars, category, feedback_text) VALUES (%s, %s, %s)"
            cursor.execute(sql, (stars, category, feedback_text))
            connection.commit()
            return 'Feedback submitted successfully!'
    except Exception as e:
        return f'Error: {str(e)}'
    finally:
        connection.close()

if __name__ == '__main__':
    create_feedback_table()  # Create the 'feedback' table on application start
    app.run(debug=True,port=80,host='0.0.0.0')
