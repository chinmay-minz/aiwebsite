// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', () => {
    const inputForm = document.getElementById('inputForm');
    const inputData = document.getElementById('inputData');
    const resultText = document.getElementById('resultText');
    const loadingDiv = document.getElementById('loading');

    // Handle form submission
    inputForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Show loading text
        loadingDiv.style.display = 'block';

        // Simulate an AI model request
        const input = inputData.value;
        
        // Call an AI API (for example, using fetch to call an API)
        try {
            // Example: Sending input data to a machine learning API
            const response = await fetch('https://api.example.com/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ inputData: input })
            });
            
            const data = await response.json();
            
            // Display the result
            resultText.textContent = `Prediction: ${data.prediction}`;
        } catch (error) {
            resultText.textContent = 'Error fetching prediction. Please try again.';
        } finally {
            // Hide loading text
            loadingDiv.style.display = 'none';
        }
    });
});