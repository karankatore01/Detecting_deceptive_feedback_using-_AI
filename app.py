from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import joblib

# Initialize the app and enable CORS
app = Flask(__name__)
CORS(app)

# Load the model and vectorizer
model = joblib.load(r'C:\Users\karan\Desktop\fake review\project\models\fake_review_detector_model.pkl')
vectorizer = joblib.load(r'C:\Users\karan\Desktop\fake review\project\models\tfidf_vectorizer.pkl')

# Home route with form
@app.route('/')
def home():
    return render_template('index.html')

# Predict route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get review text from request
        data = request.get_json(force=True)
        review_text = data.get('review')
        
        # Ensure review_text is provided
        if not review_text:
            return jsonify({"error": "No review text provided"}), 400

        # Process text and predict
        vectorized_text = vectorizer.transform([review_text])
        prediction = model.predict(vectorized_text)[0]
        result = "Fake" if prediction == 0 else "Real"
        
        # Return the prediction as JSON
        return jsonify({"review": review_text, "prediction": result})
    
    except Exception as e:
        # Log the error for server-side debugging
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred during prediction"}), 500

if __name__ == '__main__':
    app.run(debug=True)
