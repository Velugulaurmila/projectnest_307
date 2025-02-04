from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import os

app = Flask(__name__)

# Load the trained model and scaler
model_filename = "heart_disease_model.pkl"
scaler_filename = "scaler.pkl"

if os.path.exists(model_filename) and os.path.exists(scaler_filename):
    with open(model_filename, "rb") as model_file:
        model = pickle.load(model_file)
    with open(scaler_filename, "rb") as scaler_file:
        scaler = pickle.load(scaler_file)
    print("✅ Model and scaler loaded successfully!")
else:
    model = None
    scaler = None
    print("❌ Model or scaler file not found! Please train and save the model first.")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None or scaler is None:
        return jsonify({'error': 'Model or scaler not loaded properly. Check server logs.'}), 500

    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No input data provided'}), 400

        # Define expected feature names
        required_features = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 
                             'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']

        input_features = []
        for feature in required_features:
            if feature not in data:
                return jsonify({'error': f'Missing feature: {feature}'}), 400
            try:
                value = float(data[feature]) if feature not in ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal'] else int(data[feature])
                input_features.append(value)
            except ValueError:
                return jsonify({'error': f'Invalid value for feature: {feature}. Expected numeric input.'}), 400

        # Convert to NumPy array and scale
        input_array = np.array([input_features])
        input_array = scaler.transform(input_array)

        # Predict
        prediction = model.predict(input_array)[0]
        probability = model.predict_proba(input_array)[0][1] * 100  # Probability of heart disease

        result = {
            'prediction': int(prediction),
            'probability': f"{probability:.2f}%",
            'message': 'High risk of heart disease' if prediction == 1 else 'Low risk of heart disease'
        }

        return jsonify(result)

    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
