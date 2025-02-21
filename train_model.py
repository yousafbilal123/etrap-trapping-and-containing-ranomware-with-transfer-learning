from django.shortcuts import render
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import os

def result_view(request):
    # Create a dummy dataset
    data = {
        'feature1': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'feature2': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'label': [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]  # 0 = benign, 1 = ransomware
    }
    df = pd.DataFrame(data)

    # Split the data into features (X) and labels (y)
    X = df[['feature1', 'feature2']]
    y = df['label']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a Random Forest Classifier
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    # Save the trained model
    models_dir = 'models'
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)

    model_path = os.path.join(models_dir, 'ransomware_model.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)

    # Prepare context to pass to the template
    context = {
    'accuracy': accuracy * 100,
    'model_path': model_path,
}


    # Render the result.html template with the context
    return render(request, 'detector/result.html', context)