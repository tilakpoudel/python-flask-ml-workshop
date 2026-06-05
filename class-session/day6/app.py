"""
Student Performance Predictor - Flask Web Application
Uses multiple features to predict student scores
"""

from flask import Flask, render_template, request
import pickle
import numpy as np
import os

app = Flask(__name__)

# Load the trained model package
print("📚 Loading student performance model...")

if os.path.exists('student_model_multiple.pkl'):
    with open('student_model_multiple.pkl', 'rb') as f:
        model_package = pickle.load(f)
    
    model = model_package['model']
    scaler = model_package['scaler']
    label_encoder = model_package['label_encoder']
    feature_columns = model_package['feature_columns']
    coefficients = model_package['coefficients']
    intercept = model_package['intercept']
    
    print("✅ Model loaded successfully!")
    print(f"📋 Features used: {feature_columns}")
else:
    print("⚠️ Model not found! Creating a simple model...")
    # Fallback to simple model
    from sklearn.linear_model import LinearRegression
    X_demo = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]).reshape(-1, 1)
    y_demo = np.array([45, 52, 58, 65, 70, 76, 82, 87, 92, 96])
    model = LinearRegression()
    model.fit(X_demo, y_demo)
    scaler = None
    feature_columns = ['hours_studied']
    coefficients = {'hours_studied': model.coef_[0]}
    intercept = model.intercept_
    print("✅ Demo model created!")

print(f"📐 Model intercept: {intercept:.2f}")


def predict_score(hours, previous_score, attendance, sleep_hours, extracurricular):
    """
    Make prediction using all features
    
    Parameters:
    hours: float - hours studied per day
    previous_score: float - previous exam score
    attendance: float - attendance percentage
    sleep_hours: float - hours of sleep per night
    extracurricular: str - 'Yes' or 'No'
    
    Returns:
    float: predicted final score
    """
    # Encode extracurricular
    extra_encoded = 1 if extracurricular == 'Yes' else 0
    
    # Create features array
    features = np.array([[hours, previous_score, attendance, sleep_hours, extra_encoded]])
    
    # Scale features if scaler exists
    if scaler:
        features_scaled = scaler.transform(features)
    else:
        features_scaled = features
    
    # Make prediction
    prediction = model.predict(features_scaled)[0]
    
    # Ensure score is within 0-100 range
    prediction = max(0, min(100, round(prediction, 1)))
    
    return prediction


def get_grade(score):
    """
    Determine grade and feedback based on predicted score
    """
    if score >= 90:
        return ("A", "🌟 Excellent! Outstanding performance!", "#27ae60", "🌟", "Top performer! Keep it up!")
    elif score >= 80:
        return ("B", "👍 Good job! You're doing well!", "#3498db", "👍", "Above average! Aim for 90+ next time!")
    elif score >= 70:
        return ("C", "📚 Good! You're on the right track!", "#f39c12", "📚", "Satisfactory. With more effort, you can reach B!")
    elif score >= 60:
        return ("D", "⚠️ You're passing, but can improve!", "#e67e22", "⚠️", "Need improvement. Try increasing study hours!")
    else:
        return ("F", "💪 Don't give up! Need significant improvement!", "#e74c3c", "💪", "At risk. Please focus on increasing study time!")


def get_recommendations(hours, previous_score, attendance, sleep_hours, extracurricular, score):
    """
    Generate personalized recommendations based on weak areas
    """
    recommendations = []
    
    if hours < 5:
        recommendations.append(f"📚 Increase study hours from {hours} to 7-8 hours/day (+{2.5 * (7 - hours):.0f} points potential)")
    
    if previous_score < 70:
        recommendations.append(f"📊 Review previous course material to strengthen foundation")
    
    if attendance < 85:
        recommendations.append(f"📈 Improve attendance from {attendance}% to 90% (+{(90 - attendance) * 0.3:.0f} points potential)")
    
    if sleep_hours < 7:
        recommendations.append(f"😴 Increase sleep from {sleep_hours} to 7-8 hours for better focus")
    
    if extracurricular == 'No' and score < 75:
        recommendations.append(f"🎭 Consider joining extracurricular activities (+5 points potential)")
    
    if score >= 80:
        recommendations.append(f"🎯 Great work! Consider helping peers to reinforce your learning")
    
    if not recommendations:
        recommendations.append("✨ You're doing great! Maintain your current routine!")
    
    return recommendations


@app.route('/')
def home():
    """Home page - shows the prediction form"""
    return render_template('improved.html', 
                          prediction=None,
                          feature_columns=feature_columns)


@app.route('/predict', methods=['POST'])
def predict():
    """Handle form submission and make prediction"""
    try:
        # Get all form data
        hours = float(request.form.get('hours', 5))
        previous_score = float(request.form.get('previous_score', 70))
        attendance = float(request.form.get('attendance', 80))
        sleep_hours = float(request.form.get('sleep_hours', 7))
        extracurricular = request.form.get('extracurricular', 'No')
        
        # Validate inputs
        hours = max(0, min(15, hours))
        previous_score = max(0, min(100, previous_score))
        attendance = max(0, min(100, attendance))
        sleep_hours = max(0, min(12, sleep_hours))
        
        # Make prediction
        predicted_score = predict_score(hours, previous_score, attendance, sleep_hours, extracurricular)
        
        # Get grade and feedback
        grade, message, color, emoji, short_advice = get_grade(predicted_score)
        
        # Get personalized recommendations
        recommendations = get_recommendations(hours, previous_score, attendance, sleep_hours, extracurricular, predicted_score)
        
        # Calculate contribution breakdown
        contributions = {
            'Study Hours': hours * 2.5,
            'Previous Score': previous_score * 0.5,
            'Attendance': attendance * 0.3,
            'Sleep Hours': sleep_hours * 1.2,
            'Extracurricular': 5 if extracurricular == 'Yes' else 0
        }
        
        return render_template('improved.html',
                              prediction=predicted_score,
                              grade=grade,
                              message=message,
                              emoji=emoji,
                              color=color,
                              short_advice=short_advice,
                              recommendations=recommendations,
                              contributions=contributions,
                              hours=hours,
                              previous_score=previous_score,
                              attendance=attendance,
                              sleep_hours=sleep_hours,
                              extracurricular=extracurricular,
                              feature_columns=feature_columns)
    
    except Exception as e:
        error_message = f"Error: {str(e)}"
        return render_template('improved.html',
                              prediction=None,
                              error=error_message)


@app.route('/about')
def about():
    """About page with model information"""
    return render_template('about.html',
                          feature_columns=feature_columns,
                          coefficients=coefficients,
                          intercept=intercept)


if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 STUDENT PERFORMANCE PREDICTOR")
    print("="*50)
    print(f"📋 Using features: {feature_columns}")
    print(f"🌐 Server starting at: http://127.0.0.1:5000")
    print(f"📱 Press Ctrl+C to stop the server")
    print("="*50 + "\n")
    app.run(debug=True, host='127.0.0.1', port=5000)
    