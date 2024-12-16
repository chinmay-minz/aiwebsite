// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', () => {
    const inputForm = document.getElementById('inputForm');
    const inputData = document.getElementById('inputData');
    const resultText = document.getElementById('resultText');
    const loadingDiv = document.getElementById('loading');
    const form = document.getElementById("uploadForm");
    const resultDiv = document.getElementById("result");


    // Handle form submission
    form.addEventListener("submit", async (event) => {
        event.preventDefault(); // Prevent form submission
    
        // Get the uploaded file
        const fileInput = document.getElementById("imageInput");
        if (!fileInput.files.length) {
            resultDiv.textContent = "Please upload a .jpg image!";
            return;
        }
    
        const file = fileInput.files[0];
    
        // Ensure the uploaded file is a .jpg
        if (!file.type.includes("jpeg")) {
            resultDiv.textContent = "Only .jpg files are allowed!";
            return;
        }
    
        // Create FormData to send the file
        const formData = new FormData();
        formData.append("image", file);
    
        try {
            // Send the file to the Flask backend
            const response = await fetch("/predict", {
                method: "POST",
                body: formData,
            });
    
            // Handle the response
            if (response.ok) {
                const data = await response.json();
                resultDiv.textContent = `Prediction: ${data.result ? "True" : "False"}`;
            } else {
                const errorData = await response.json();
                resultDiv.textContent = `Error: ${errorData.error}`;
            }
        } catch (error) {
            resultDiv.textContent = "An error occurred. Please try again!";
            console.error(error);
        }
    });