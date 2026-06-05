"""
Train a model using multiple features for better predictions
Run this file first to create the model
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
import pickle
import os

print("="*60)
print("TRAINING STUDENT PERFORMANCE MODEL WITH MULTIPLE FEATURES")
print("="*60)

# Create sample dataset with multiple features
np.random.seed(42)
n_students = 500

# Generate features
data = {
    'hours_studied': np.random.randint(1, 15, n_students),
    'previous_score': np.random.randint(40, 100, n_students),
    'attendance': np.random.randint(50, 100, n_students),
    'sleep_hours': np.random.uniform(4, 10, n_students).round(1),
    'extracurricular': np.random.choice(['Yes', 'No'], n_students, p=[0.4, 0.6]),
}

df = pd.DataFrame(data)

# Create target variable (final score) based on realistic formula
df['final_score'] = (
    df['hours_studied'] * 2.5 +           # Each study hour adds 2.5 points
    df['previous_score'] * 0.5 +          # Previous score has 50% weight
    df['attendance'] * 0.3 +              # Attendance adds 0.3 points per %
    df['sleep_hours'] * 1.2 +             # Good sleep adds up to 12 points
    (df['extracurricular'] == 'Yes') * 5 + # Extracurricular bonus: 5 points
    np.random.normal(0, 5, n_students)    # Random noise
).clip(0, 100).round(1)

print("\n📊 Dataset created:")
print(f"   Total students: {len(df)}")
print(f"   Features: {list(df.columns)}")

# Encode categorical variable
le = LabelEncoder()
df['extracurricular_encoded'] = le.fit_transform(df['extracurricular'])
print(f"\n🔢 Encoded extracurricular:")
print(f"   Yes → 1, No → 0")

# Select features for training
feature_columns = ['hours_studied', 'previous_score', 'attendance', 'sleep_hours', 'extracurricular_encoded']
target_column = 'final_score'

X = df[feature_columns]
y = df[target_column]

print(f"\n📋 Features used for prediction:")
for col in feature_columns:
    print(f"   - {col}")

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train the model
model = LinearRegression()
model.fit(X_scaled, y)

print(f"\n🤖 Model training complete!")
print(f"   R² Score: {model.score(X_scaled, y):.3f}")

# Display coefficients
print(f"\n📐 Model Coefficients:")
for col, coef in zip(feature_columns, model.coef_):
    impact = "positive" if coef > 0 else "negative"
    print(f"   {col}: {coef:.2f} ({impact} impact)")

print(f"\n   Intercept: {model.intercept_:.2f}")

# Save everything in one package
model_package = {
    'model': model,
    'scaler': scaler,
    'label_encoder': le,
    'feature_columns': feature_columns,
    'coefficients': dict(zip(feature_columns, model.coef_)),
    'intercept': model.intercept_
}

with open('student_model_multiple.pkl', 'wb') as f:
    pickle.dump(model_package, f)

print("\n✅ Model saved as 'student_model_multiple.pkl'")

# Test predictions
print("\n🎯 Sample Predictions:")
test_students = [
    {'name': 'Hard Worker', 'hours': 8, 'previous': 85, 'attendance': 90, 'sleep': 8, 'extra': 'Yes'},
    {'name': 'Average Student', 'hours': 5, 'previous': 70, 'attendance': 80, 'sleep': 7, 'extra': 'No'},
    {'name': 'Needs Improvement', 'hours': 2, 'previous': 50, 'attendance': 60, 'sleep': 5, 'extra': 'No'},
]

for student in test_students:
    # Prepare features
    extra_encoded = 1 if student['extra'] == 'Yes' else 0
    features = np.array([[student['hours'], student['previous'], 
                         student['attendance'], student['sleep'], extra_encoded]])
    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)[0]
    print(f"   {student['name']}: {prediction:.1f} points")

print("\n" + "="*60)
print("✅ Model training complete! Ready to run app.py")
print("="*60)
