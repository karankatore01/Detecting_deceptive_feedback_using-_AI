document.getElementById('reviewForm').addEventListener('submit', function(event) {
    event.preventDefault();

    let reviewText = document.getElementById('review').value;

    fetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ review: reviewText })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        return response.json();
    })
    .then(data => {
        console.log("Response data:", data);  // Debugging
        let resultDiv = document.getElementById('result');
        
        if (data.prediction) {
            resultDiv.innerHTML = `Prediction: ${data.prediction}`;
            resultDiv.style.color = data.prediction === "Fake" ? "#dc3545" : "#28a745";
        } else {
            resultDiv.innerHTML = "Error: " + (data.error || "Unexpected response format.");
            resultDiv.style.color = "#dc3545";
        }
    })
    .catch(error => {
        console.error("Error:", error);
        let resultDiv = document.getElementById('result');
        resultDiv.innerHTML = "An error occurred. Please try again.";
        resultDiv.style.color = "#dc3545";
    });
});
