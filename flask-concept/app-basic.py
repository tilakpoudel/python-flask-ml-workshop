# app.py - Complete beginner-friendly Flask app

# 1. Import Flask
from flask import Flask

# 2. Create the app
app = Flask(__name__)

# 3. Homepage route
@app.route('/')
def home():
    # This runs when someone visits /
    return '''
    <h1>📘 BCA UI/UX Notes</h1>
    <p>Welcome to your study notebook server.</p>
    <p>Try these links:</p>
    <ul>
        <li><a href="/about">About this project</a></li>
        <li><a href="/user/student">Dynamic user page</a></li>
    </ul>
    '''

# 4. About page
@app.route('/about')
def about():
    return '''
    <h1>About This Flask App</h1>
    <p>This app is part of your BCA UI/UX notebook.</p>
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

# 6. Run the server
if __name__ == '__main__':
    # debug=True means: 
    # - Server restarts when you save code
    # - Shows error messages in browser (helpful for learning)
    app.run(debug=True)
    