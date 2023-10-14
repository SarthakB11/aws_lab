from flask import Flask, request, render_template
import os
import json

application = Flask(__name__)

# Display the feedback form
@application.route('/')
def feedback_form():
    return render_template('feedback.html')

# Handle form submission and store feedback in the database
@application.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    feedback_data = request.form.get('feedbackData')
    # Parse the JSON data
    feedback_data = json.loads(feedback_data)
    
    # Extract the values
    stars = feedback_data['stars']
    category = feedback_data['category']
    feedback_text = feedback_data['feedbackText']

    print(stars, category, feedback_text)
    try:   
        return f'Stars: {stars}, Category: {category}, Comment:{feedback_text}.Feedback submitted successfully!'
    except Exception as e:
        return f'Error: {str(e)}'
    finally:
        pass

if __name__ == '__main__':
    #create_feedback_table()  # Create the 'feedback' table on application start
    application.run(debug=True,port=int(os.environ.get('PORT',5000)),host='0.0.0.0')
