# pip install flask

# 1. Import Flask
from flask import Flask, render_template

# 2. Create the app
app = Flask(__name__)

# 3. Homepage route
@app.route('/')
def home():
    return '''
    <h1>📘 Python Notes</h1>
    <p>Welcome to your study notebook server.</p>

    <h2>Available Routes:</h2>
    <ul>
        <li><a href="/test">/test</a> - A test page to check if the server is working.</li>
        <li><a href="/about">/about</a> - Learn more about this Flask app.</li>
        <li><a href="/topics">/topics</a> - View a list of Python topics.</li>
    </ul>
    '''

# add test route
@app.route('/test')
def test():
    return '''
    <h1>Test Page</h1>
    <p>This is a test route to check if the server is working.</p>
    '''

@app.route('/about')
def about():
    return '''
    <h1>About This Flask App</h1>
    <p>This app is part of your Python notebook.</p>
    <p>Flask helps you turn Python code into web pages.</p>
    <a href="/">← Back to Home</a>
    '''

# 5. Dynamic user page
@app.route('/user/<username>')
def user_profile(username):
    # Show different content based on the URL
    return f'''
    <h1>👤 User Profile: {username}</h1>
    <p>This page is personalized for {username}.</p>
    <p>In a real app, you would load data from a database here.</p>
    <a href="/">← Back to Home</a>
    '''

topics = [
    {"id": 1, "name": "Python Basics", "description": "Learn about variables, data types, and control flow.", "hours": 5},
    {"id": 2, "name": "Functions and Modules", "description": "Understand how to create reusable code with functions and modules.", "hours": 4},
    {"id": 3, "name": "Object-Oriented Programming", "description": "Learn about classes, objects, and OOP principles.", "hours": 6},
    {"id": 4, "name": "Data Structures", "description": "Explore lists, dictionaries, sets, and tuples.", "hours": 5},
    {"id": 5, "name": "File Handling", "description": "Learn how to read and write files in Python.", "hours": 3},
]

@app.route('/topics')
def topics_list():
    """Show all Python topics"""
    # Pass the entire topics list to the template
    return render_template('topics.html', title="Topics - Python Syllabus", topics=topics)

# 6. Run the server
if __name__ == '__main__':
    # debug=True means: 
    # - Server restarts when you save code
    # - Shows error messages in browser (helpful for learning)
    app.run(debug=True)
