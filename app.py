from flask import Flask, render_template, request, jsonify
import numpy as np
from sklearn.cluster import KMeans

app = Flask(__name__)

# Define muscle groups and features with more accurate data
muscle_groups = ["Chest", "Back", "Biceps", "Triceps", "Shoulders", "Legs", "Abs", "Cardio"]

# Muscle features array with the following columns:
# [strength_importance, endurance_importance, flexibility_importance, recovery_time_in_days]
muscle_features = np.array([
    [9, 5, 3, 3],  # Chest
    [8, 6, 3, 3],  # Back
    [7, 4, 2, 2],  # Biceps
    [7, 4, 2, 2],  # Triceps
    [6, 5, 3, 2],  # Shoulders
    [9, 6, 4, 4],  # Legs
    [5, 7, 5, 1],  # Abs
    [4, 9, 6, 1],  # Cardio
])

# Enhanced clustering based on user goals
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_plan', methods=['POST'])
def generate_plan():
    days = int(request.form['days'])
    goal = request.form['goal']  # Strength, Endurance, or Flexibility

    # Define goal index based on user input
    if goal == "Strength":
        goal_idx = 0
    elif goal == "Endurance":
        goal_idx = 1
    else:  # Flexibility
        goal_idx = 2

    if 1 <= days <= 7:
        # Extract the column based on the user's goal
        goal_features = muscle_features[:, goal_idx].reshape(-1, 1)

        # Cluster the workouts based on user's goal
        kmeans = KMeans(n_clusters=days, random_state=42, n_init=10)
        kmeans.fit(goal_features)
        labels = kmeans.labels_

        plan = [[] for _ in range(days)]

        for i, label in enumerate(labels):
            plan[label].append(muscle_groups[i])

        # Ensure that no day has fewer than 2 muscle groups
        for i in range(days):
            if len(plan[i]) < 2:
                additional_muscle = np.random.choice(muscle_groups)
                while additional_muscle in plan[i]:
                    additional_muscle = np.random.choice(muscle_groups)
                plan[i].append(additional_muscle)

        # Format the workout plan
        plan_str = [f"Day {i+1}: {', '.join(day)}" for i, day in enumerate(plan)]
        return jsonify({'plan': plan_str})

    else:
        return jsonify({'error': "Please enter a valid number of days between 1 and 7."})

if __name__ == '__main__':
    app.run(debug=True)
