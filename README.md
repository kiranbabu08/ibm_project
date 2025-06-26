# ibm_project
# 🩺 HealthAI Assistant

HealthAI is an intelligent healthcare assistant web app built using Flask. It allows users to chat with a healthcare AI bot, predict diseases based on symptoms, generate treatment plans, analyze health vitals visually, and upload medical reports for AI-based interpretation.

---

## 🚀 Features

- 💬 **AI-Powered Patient Chat**
- 🧬 **Disease Prediction**
- 💊 **Treatment Planning**
- 📊 **Health Analytics (Charts + Insights)**
- 📤 **Report Upload & Analysis via OCR** *(optional)*

---

## 🛠️ Tech Stack

- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Backend**: Python, Flask
- **Data Processing**: NumPy, Pandas, Matplotlib, Seaborn
- **OCR (Optional)**: Tesseract via `pytesseract`

---

## 📁 Project Structure

HealthAI/
│
├── app.py # Flask application entry point
├── utils1.py # AI response and OCR logic
│
├── templates/ # HTML templates
│ ├── index.html # Chat UI
│ ├── disease.html # Disease form
│ ├── treatment.html # Treatment form
│ ├── analytics.html # Analytics input form
│ ├── result.html # Result display page
│ └── upload.html # File upload page (optional)
│
├── static/
│ ├── styles.css # Custom styles
│ └── analytics_chart.png # Auto-generated chart image (if any)
│
└── README.md # Project overview (this file)
