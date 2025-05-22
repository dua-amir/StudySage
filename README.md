# 📚 StudySage – AI Study Helper with Voice Support

StudySage is a smart voice-based AI assistant designed to help students understand academic topics with ease. Whether you're stuck on a concept or just looking for a simple study plan, StudySage has your back. It combines voice input, AI-generated explanations, trusted resources, and a clean GUI to support everyday learning.

## 🧠 Project Overview

Team Members:
  - Dua Amir (47849)
  - Samreen Bibi (46484)
  - Zainab Bibi (46462)
  - Maryam Shakeel (48406)

---

## 🚀 Features

✅ Voice and text input for user-friendly interaction  
✅ AI-generated explanations (OpenAI support optional)  
✅ Scrapes relevant YouTube videos & articles  
✅ Speaks answers aloud using TTS  
✅ Suggests a simple study plan  
✅ Stores notes for revision  
✅ Clean GUI interface using `tkinter`

---

## 🔍 Problem Statement

Students often struggle to find simple, trustworthy resources for difficult topics and lose motivation. StudySage solves this by offering:
- Clear explanations
- Reliable content
- Minimal distractions
- Personalized interaction

---

## 🎯 Objectives

- Accept input via voice/text  
- Explain academic topics using AI  
- Recommend YouTube & article links  
- Speak answers via voice  
- Display helpful study tips & save notes  

---

## 🧩 PEAS Description

| Element             | Description                                                             |
|---------------------|-------------------------------------------------------------------------|
| Performance Measure | Clarity of explanation, accuracy of resources, student feedback         |
| Environment         | Desktop/Laptop with Python & internet                                   |
| Actuators           | Voice (TTS), GUI, clickable links                                       |
| Sensors             | Voice input, text box input, article/video scraping                     |

---

## 🧰 Tools & Libraries

- `speech_recognition` – For capturing voice input  
- `pyttsx3` – For text-to-speech output  
- `openai` – For AI-generated explanations (optional)  
- `youtube-search-python` – For finding relevant YouTube videos  
- `requests + BeautifulSoup` – For scraping articles  
- `tkinter` or `customtkinter` – For GUI layout  

---

## 🗂️ Folder Structure

studysage/
│
├── topic_parser.py # Understands input topic
├── explanation_generator.py # AI-based explanation logic
├── resource_finder.py # Scrapes article & video links
├── gui.py # Main GUI interface
├── README.md # Project documentation
└── requirements.txt # Python dependencies
---

## ⚙️ Setup Instructions

1. Clone the Repository
git clone https://github.com/dua-amir/StudySage.git
cd StudySage

Install Dependencies
pip install -r requirements.txt
(Optional) Add OpenAI API Key
If using OpenAI for explanations, set your API key in explanation_generator.py

Run the App
python gui.py


🧪 Sample Demo Flow
User: "Explain Newton's First Law"
✔️ Explanation appears on screen
✔️ Voice reads it aloud
✔️ YouTube links + article links appear
✔️ Study plan and follow-up tips suggested

⚠️ Known Limitations
Requires internet access for scraping & YouTube links
Scraping results may vary by topic
Not optimized for all academic subjects
No mobile version yet

🌟 Future Enhancements
Daily revision notifications
Quiz generation from topics
Voice-based interactive quizzes
GPT-4 API integration
Dark mode and mobile version (React Native)

📬 Contact
Feel free to reach out for suggestions, collaborations, or feedback:

Dua Amir – duaamir4211@gmail.com

📌 License
This project is for educational use only. Commercial redistribution is not permitted.
