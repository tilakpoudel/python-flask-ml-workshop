"""
Run this file first to create the model if you don't have it
"""

import pickle
import numpy as np
from sklearn.linear_model import LinearRegression

print("Creating student performance model...")

# Create training data
# More study hours = higher scores
hours_studied = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]).reshape(-1, 1)
final_scores = np.array([45, 52, 58, 65, 70, 76, 82, 87, 92, 96, 98, 99])

# Train the model
model = LinearRegression()
model.fit(hours_studied, final_scores)

# Save the model
with open('simple_student_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print(f"✅ Model created and saved!")
print(f"📐 Formula: Score = {model.coef_[0]:.2f} × Hours + {model.intercept_:.2f}")
print(f"\nTest predictions:")
for hours in [3, 5, 7, 9]:
    pred = model.predict([[hours]])[0]
    print(f"  {hours} hours → {pred:.1f} points")
    