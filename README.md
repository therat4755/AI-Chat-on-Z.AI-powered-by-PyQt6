# Z.AI PyQt6 Desktop Chatbot

A clean, lightweight, and feature-rich desktop AI chatbot application built with **Python**, **PyQt6**, and the **Z.AI API**. This project provides a native desktop interface complete with multi-chat history management, local JSON persistence, real-time search, and markdown-to-HTML rendering.

---

## ✨ Features

* **Native Desktop GUI**: Built using PyQt6 for a responsive and clean user interface.
* **Multi-Chat Management**: Create, delete, and switch between multiple independent chat sessions using a dedicated history window.
* **History Filtering**: Instantly search and filter through past conversation titles on the fly.
* **Z.AI API Integration**: Powered by Z.AI's `glm-4.7-flash` model for fast, intelligent conversational responses.
* **Markdown Support**: Automatically parses basic markdown elements (such as bolding and strikethroughs) into clean HTML for the chat view.
* **Audio Cues**: Plays an audio notification (`done.mp3`) as soon as the AI completes a generation.
* **Local Persistence**: Automatically saves and loads your chat logs to `conversations.json`.

---

## 🛠️ Tech Stack

* **Python**
* **PyQt6** (Graphical User Interface)
* **ZaiClient** (Z.AI API SDK)
* **Playsound** (Audio alerts)

---

## 🚀 Getting Started

### Prerequisites

Make sure you have Python installed along with the required libraries:

```bash
  pip install PyQt6 zai-sdk playsound
```
### Running the App

1. Clone the repository:
```bash
   git clone https://github.com/therat4755/AI-Chat-on-Z.AI-powered-by-PyQt6.git
   cd your-repo-name
```
2. Configure your API key in the script if necessary.
3. Ensure you have a done.mp3 file in your working directory for audio notifications.
4. Run the application: python main.py
