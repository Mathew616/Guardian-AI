import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QInputDialog, QMessageBox
from PyQt5.QtCore import Qt
import requests
import uuid

API_KEY = "###"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key=" + API_KEY

class GeminiAI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Gemini AI - IPC Sections & Complaint Lodge')
        self.setGeometry(200, 200, 1000, 900)
        
        # Layouts
        main_layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        
        # Chat display area
        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)
        main_layout.addWidget(QLabel("Chat:"))
        main_layout.addWidget(self.chat_display)
        
        # Input area for chat
        self.input_box = QLineEdit(self)
        self.input_box.setPlaceholderText("Ask about IPC sections or describe a crime...")
        input_layout.addWidget(self.input_box)
        
        # Send button for chat
        send_button = QPushButton('Send', self)
        send_button.clicked.connect(self.send_message)
        input_layout.addWidget(send_button)

        # Register Complaint button
        complaint_button = QPushButton('Register Complaint', self)
        complaint_button.clicked.connect(self.register_complaint)
        input_layout.addWidget(complaint_button)
        
        main_layout.addLayout(input_layout)
        
        self.setLayout(main_layout)
        
        # Display welcome message
        self.chat_display.append("Bot: Hi, I am Guardian AI. How can I help you?")
    
    def send_message(self):
        user_message = self.input_box.text().strip()
        if not user_message:
            return
        
        self.chat_display.append(f"You: {user_message}")
        self.input_box.clear()
        
        response = self.get_response_from_gemini(user_message)
        self.chat_display.append(f"<b>Bot:</b> {response}")
    
    def get_response_from_gemini(self, message):
        try:
            data = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": message}]
                    }
                ]
            }
            response = requests.post(GEMINI_API_URL, json=data)
            response.raise_for_status()
            response_json = response.json()
            
            if 'candidates' in response_json and len(response_json['candidates']) > 0:
                finish_reason = response_json['candidates'][0].get('finishReason', '')
                if finish_reason == 'SAFETY':
                    return "<b>Your message contains potentially harmful content. Please rephrase or ask a different question.</b>"
                
                if 'content' in response_json['candidates'][0] and 'parts' in response_json['candidates'][0]['content'] and len(response_json['candidates'][0]['content']['parts']) > 0:
                    return "<b>" + response_json['candidates'][0]['content']['parts'][0]['text'] + "</b>"
            
            return "Error: Invalid response format from Gemini API"
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}"
    
    def register_complaint(self):
        name, ok1 = QInputDialog.getText(self, 'Complaint Registration', 'Enter your name:')
        if not ok1 or not name:
            return
        email, ok2 = QInputDialog.getText(self, 'Complaint Registration', 'Enter your email:')
        if not ok2 or not email:
            return
        crime_details, ok3 = QInputDialog.getText(self, 'Complaint Registration', 'Enter crime details:')
        if not ok3 or not crime_details:
            return
        
        complaint_id = str(uuid.uuid4())
        complaint_info = f"Complaint ID: {complaint_id}\nName: {name}\nEmail: {email}\nCrime Details: {crime_details}\n\n"
        
        with open("complaints.txt", "a") as file:
            file.write(complaint_info)
        
        QMessageBox.information(self, 'Complaint Registered', f"Your complaint has been registered.\nComplaint ID: {complaint_id}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gemini_ai = GeminiAI()
    gemini_ai.show()
    sys.exit(app.exec_())
