async function toggleComplaintForm() {
    var complaintForm = document.getElementById('complaint-form');
    complaintForm.style.display = (complaintForm.style.display == 'none' || complaintForm.style.display == '') ? 'block' : 'none';
}

async function sendMessage() {
    var userMessage = document.getElementById('user-message').value.trim();
    if (!userMessage) {
        return;
    }

    var chatDisplay = document.getElementById('chat-display');
    chatDisplay.innerHTML += "<div class='message user-message'>You: " + userMessage + "</div>";

    document.getElementById('user-message').value = '';

    try {
        var response = await getResponseFromGemini(userMessage);
        chatDisplay.innerHTML += "<div class='message bot-message'>Bot: " + response + "</div>";
    } catch (error) {
        console.error('Error:', error);
        chatDisplay.innerHTML += "<div class='message bot-message'>Bot: Error retrieving response from Gemini API</div>";
    }
}

async function registerComplaint() {
    var complaintDetails = {
        name: document.getElementById('name').value.trim(),
        email: document.getElementById('email').value.trim(),
        complaint: document.getElementById('complaint').value.trim()
    };

    if (!complaintDetails.name || !complaintDetails.email || !complaintDetails.complaint) {
        alert('Please fill in all fields');
        return;
    }

    try {
        var response = await sendComplaintDetails(complaintDetails);
        alert('Complaint registered successfully. Your complaint ID is: ' + response.complaintId);
        toggleComplaintForm();
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to register complaint. Please try again later.');
    }
}

async function getResponseFromGemini(message) {
    var apiKey = "AIzaSyDohGeh3e0YPkE_u12eD0BI4dQl4gkTLcQ";
    var geminiApiUrl = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key=" + apiKey;

    var data = {
        "contents": [{
            "role": "user",
            "parts": [{
                "text": message
            }]
        }]
    };

    var response = await fetch(geminiApiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    if (!response.ok) {
        throw new Error('Failed to fetch response from Gemini API');
    }

    var responseData = await response.json();

    if (responseData.candidates && responseData.candidates.length > 0 && responseData.candidates[0].content && responseData.candidates[0].content.parts && responseData.candidates[0].content.parts.length > 0) {
        return responseData.candidates[0].content.parts[0].text;
    } else {
        throw new Error('Invalid response format from Gemini API');
    }
}

async function sendComplaintDetails(complaintDetails) {
    // Assuming you have a backend endpoint to handle this
    var response = await fetch('YOUR_BACKEND_ENDPOINT', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(complaintDetails)
    });

    if (!response.ok) {
        throw new Error('Failed to send complaint details');
    }

    return await response.json();
}
