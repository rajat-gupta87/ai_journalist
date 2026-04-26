# 🗞️ AI Journalist Agent

An AI-powered journalism application that generates high-quality, publication-ready articles using a **multi-agent pipeline** (Searcher → Writer → Editor) built with **Python, Streamlit, and Google Gemini API**.

---

## 🚀 Features

* 🔍 **Research Agent (Searcher)**
  Generates search strategies, key sources, and research insights.

* ✍️ **Writer Agent**
  Creates long-form, structured, high-quality articles (1500+ words).

* 📝 **Editor Agent**
  Refines and polishes the article to professional standards.

* 🎨 **Modern UI (Streamlit)**
  Clean newspaper-style interface.

* 📥 **Download Option**
  Export generated article as a Markdown file.

---

## 🧠 Tech Stack

* Python 3.13
* Streamlit
* Google Gemini API (`gemini-2.0-flash`)

---

## 📂 Project Structure

```
ai-journalist/
│
├── ai_journalist.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

```bash
pip install streamlit google-generativeai
```

---

## ▶️ Run the App

```bash
python -m streamlit run ai_journalist.py
```

Then open in browser:

```
http://localhost:8501
```

---

## 🔑 API Key Setup

1. Go to Google AI Studio
2. Generate your Gemini API key
3. Paste it in the app sidebar

---

## 🧪 How It Works

1. Enter a topic
2. Click **Generate Article**
3. AI performs:

   * Research
   * Writing
   * Editing
4. Get a full-length professional article

---

## ⚠️ Notes

* Requires a valid Gemini API key
* Free tier has usage limits
* Do not share your API key publicly

---

## 💼 Project Description

**AI Journalist Agent (Python, Streamlit, Gemini API)**

* Developed a multi-agent AI system for automated article generation
* Implemented structured content pipeline (Research → Writing → Editing)
* Built an interactive UI using Streamlit
* Integrated Gemini API for real-time content generation

---

## 📌 Future Improvements

* 🌐 Real-time web search integration
* 🖼️ Image generation support
* 📄 Export to PDF
* 🧠 Memory-based article refinement

---

## 👨‍💻 Author

Rajat Gupta

---

⭐ If you like this project, consider giving it a star!
