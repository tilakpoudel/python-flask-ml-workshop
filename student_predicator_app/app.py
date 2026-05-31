"""
Student Performance Predictor - Flask Web Application
This app takes student study hours and predicts their final score
"""

from flask import Flask, render_template, request
import pickle
import numpy as np
import os

# Create Flask app
app = Flask(__name__)

# Load our trained model
print("📚 Loading student performance model...")

# Check if model exists
if os.path.exists('simple_student_model.pkl'):
    with open('simple_student_model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("✅ Model loaded successfully!")
else:
    print("⚠️ Model not found! Creating a simple model...")
    # Create a simple model if not available
    from sklearn.linear_model import LinearRegression
    X_demo = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]).reshape(-1, 1)
    y_demo = np.array([45, 52, 58, 65, 70, 76, 82, 87, 92, 96])
    model = LinearRegression()
    model.fit(X_demo, y_demo)
    print("✅ Demo model created!")

# Get model coefficients for display
coefficient = model.coef_[0]
intercept = model.intercept_

print(f"📐 Model Formula: Score = {coefficient:.2f} × Hours + {intercept:.2f}")


def get_grade(score):
    """
    Determine grade and feedback based on predicted score
    
    Parameters:
    score: predicted score (0-100)
    
    Returns:
    grade, message, color, emoji
    """
    if score >= 90:
        return ("A", "Excellent! Keep up the great work!", "#27ae60", "🌟")
    elif score >= 80:
        return ("B", "Good job! You're doing well!", "#3498db", "👍")
    elif score >= 70:
        return ("C", "Good! With a little more effort, you can do even better!", "#f39c12", "📚")
    elif score >= 60:
        return ("D", "You're passing, but try to study more!", "#e67e22", "⚠️")
    else:
        return ("F", "Don't give up! Try increasing your study hours!", "#e74c3c", "💪")


def get_study_tip(hours, score):
    """
    Provide personalized study tips
    
    Parameters:
    hours: current study hours
    score: predicted score
    
    Returns:
    tip message
    """
    if score < 60:
        recommended = max(5, hours + 2)
        return f"💡 Tip: Try studying {recommended:.1f} hours per day to improve your score!"
    elif score < 75:
        return "💡 Tip: You're on the right track! Stay consistent with your studies."
    elif score < 90:
        return "💡 Tip: Great work! Consider helping other students who are struggling."
    else:
        return "🎯 Tip: Excellent! Keep challenging yourself with advanced topics."


@app.route('/')
def home():
    """
    Home page - shows the prediction form
    """
    return render_template('index.html', 
                          result_html='',
                          accuracy=round(abs(coefficient * 2), 1))


@app.route('/predict', methods=['POST'])
def predict():
    """
    Handle form submission and make prediction
    """
    try:
        # Get study hours from form
        hours = float(request.form['hours'])
        
        # Validate input
        if hours < 0:
            hours = 0
        if hours > 15:
            hours = 15
        
        # Make prediction using our model
        predicted_score = model.predict([[hours]])[0]
        predicted_score = round(predicted_score, 1)
        
        # Ensure score is within 0-100 range
        predicted_score = max(0, min(100, predicted_score))
        
        # Get grade and feedback
        grade, message, color, emoji = get_grade(predicted_score)
        tip = get_study_tip(hours, predicted_score)
        
        # Create HTML for results
        result_html = f"""
        <div class="result" style="border-left: 4px solid {color};">
            <h2>{emoji} Your Predicted Score:</h2>
            <div class="score" style="color: {color};">{predicted_score}</div>
            <div class="grade">Grade: {grade}</div>
            <p>{message}</p>
            <div class="tip">
                {tip}
            </div>
            <div class="formula-info">
                <small>📐 Based on formula: Score = {coefficient:.2f} × {hours} + {intercept:.2f} = {predicted_score}</small>
            </div>
        </div>
        """
        
        return render_template('index.html', 
                              result_html=result_html,
                              accuracy=round(abs(coefficient * 2), 1))
    
    except Exception as e:
        error_html = f"""
        <div class="result" style="border-left: 4px solid #e74c3c;">
            <h2>❌ Error</h2>
            <p>Something went wrong. Please check your input.</p>
            <p style="font-size: 12px;">Error: {str(e)}</p>
        </div>
        """
        return render_template('index.html', 
                              result_html=error_html,
                              accuracy=round(abs(coefficient * 2), 1))


@app.route('/about')
def about():
    """
    About page with information about the model
    """
    about_html = f"""
    <div class="result">
        <h2>📊 About This Predictor</h2>
        <p>This tool uses Linear Regression to predict student performance based on study hours.</p>
        <h3>Model Information:</h3>
        <ul style="text-align: left;">
            <li><strong>Formula:</strong> Score = {coefficient:.2f} × Hours + {intercept:.2f}</li>
            <li><strong>Interpretation:</strong> Each study hour adds {coefficient:.2f} points to the base score</li>
            <li><strong>Base score:</strong> {intercept:.1f} points (with 0 study hours)</li>
            <li><strong>Model Type:</strong> Linear Regression</li>
        </ul>
        <h3>How to Use:</h3>
        <ol style="text-align: left;">
            <li>Enter your daily study hours (1-12 hours)</li>
            <li>Click "Predict My Score"</li>
            <li>See your predicted score and grade</li>
            <li>Get personalized study tips</li>
        </ol>
        <p style="margin-top: 20px;">
            <a href="/" style="color: #3498db;">← Back to Predictor</a>
        </p>
    </div>
    """
    return render_template('index.html', 
                          result_html=about_html,
                          accuracy=round(abs(coefficient * 2), 1))


# Run the app
if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 STUDENT PERFORMANCE PREDICTOR")
    print("="*50)
    print(f"📐 Model: Score = {coefficient:.2f} × Hours + {intercept:.2f}")
    print(f"🌐 Server starting at: http://127.0.0.1:5000")
    print(f"📱 Press Ctrl+C to stop the server")
    print("="*50 + "\n")
    app.run(debug=True, host='127.0.0.1', port=5000)
