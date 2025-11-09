from flask import Flask, request, jsonify, render_template
import joblib
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences

app = Flask(__name__)

# Load Trained Model & Tokenizer
model = tf.keras.models.load_model('models/feedback_model_large.h5')
tokenizer = joblib.load('models/tokenizer.pkl')

MAX_LEN = 200

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    feedback_text = request.form.get("feedback")
    if not feedback_text:
        return jsonify({"error": "No feedback provided"}), 400

    # Convert text into sequences
    seq = pad_sequences(tokenizer.texts_to_sequences([feedback_text]), maxlen=MAX_LEN)
    prediction = model.predict(seq)[0][0]
    result = "Fake" if prediction < 0.5 else "Real"

    return jsonify({"feedback": feedback_text, "prediction": result})

if __name__ == '_main_':
    app.run(debug=True)
