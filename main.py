import sys
import os
import json
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from zai import ZaiClient
import playsound as p
import re


name = os.getlogin()
api = 'bdbe9f9db7234a8f98f5067e7cd94ab1.pggwr93ttTJqgffI'
client = ZaiClient(api_key=api, base_url="https://api.z.ai/api/paas/v4/")
bold_toggle = False


class HistoryWindow(QDialog):
    def __init__(self, parent=None, conversations=None):
        super().__init__(parent)
        self.conversations = conversations # Посилання на список розмов
        self.setWindowTitle("Conversation history")
        self.resize(300, 400)
        
        layout = QVBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by title...")
        self.search_input.textChanged.connect(self.filter_history)
        
        self.list_widget = QListWidget()
        self.update_list()
        # Подвійний клік відкриває розмову
        self.list_widget.itemDoubleClicked.connect(self.open_conversation)
        
        btn_layout = QHBoxLayout()
        self.new_btn = QPushButton("New chat")
        self.del_btn = QPushButton("Delete chat")
        
        self.new_btn.clicked.connect(self.create_new_chat)
        self.del_btn.clicked.connect(self.delete_item)
        
        btn_layout.addWidget(self.new_btn)
        btn_layout.addWidget(self.del_btn)
        
        layout.addWidget(self.search_input)
        layout.addWidget(self.list_widget)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def update_list(self):
        self.list_widget.clear()
        for conv in self.conversations:
            self.list_widget.addItem(conv['title'])

    def filter_history(self, text):
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            item.setHidden(text.lower() not in item.text().lower())

    def open_conversation(self, item):
        idx = self.list_widget.row(item)
        if idx >= 0:
            self.parent().load_conversation(idx)
            self.accept()

    def create_new_chat(self):
        self.parent().create_new_chat()
        self.update_list()
        self.accept()

    def delete_item(self):
        idx = self.list_widget.currentRow()
        if idx >= 0:
            self.parent().delete_conversation(idx)
            self.update_list()


class AIApp(QWidget):
    def __init__(self):
        super().__init__()
        # Завантажуємо історію розмов з файлу
        self.load_conversations()
        self.current_index = len(self.conversations) - 1
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Z.AI Chatbot")
        self.resize(450, 600)
        main_layout = QVBoxLayout()

        self.history_button = QPushButton("View history")
        self.history_button.clicked.connect(self.show_history)
        
        self.info_area = QTextEdit()
        self.info_area.setReadOnly(True)
        if 0 <= self.current_index < len(self.conversations):
            self.info_area.setPlainText(self.conversations[self.current_index]['content'])
        
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Ask Z.AI...")
        self.search_button = QPushButton("Send")
        self.search_button.clicked.connect(self.search_country)
        
        main_layout.addWidget(self.history_button)
        main_layout.addWidget(self.info_area)
        main_layout.addLayout(search_layout)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        self.setLayout(main_layout)

    def create_new_chat(self):
        new_chat = {'title': f'Conversation {len(self.conversations) + 1}', 'content': ''}
        self.conversations.append(new_chat)
        self.current_index = len(self.conversations) - 1
        self.info_area.clear()
        self.save_conversations()

    def load_conversation(self, index):
        if 0 <= index < len(self.conversations):
            self.current_index = index
            
            raw_text = self.conversations[index]['content']
            global bold_toggle
            bold_toggle = False
            
            def replace_bold(match):
                global bold_toggle
                bold_toggle = not bold_toggle
                return '<b>' if bold_toggle else '</b>'
            
            result = re.sub(r'\*\*|__', replace_bold, raw_text)
            result = re.sub(r'~', '<s>', result)
            
            result = result.replace('\n', '<br>')
            self.info_area.setHtml(result)

    def delete_conversation(self, index):
        if 0 <= index < len(self.conversations):
            active_conv = self.conversations[self.current_index]
            del self.conversations[index]
            if not self.conversations:
                self.conversations.append({'title': 'First conversation', 'content': ''})
                self.current_index = 0
            else:
                if active_conv in self.conversations:
                    self.current_index = self.conversations.index(active_conv)
                else:
                    self.current_index = min(index, len(self.conversations) - 1)
            self.load_conversation(self.current_index)
            self.save_conversations()

    def load_conversations(self):
        if os.path.exists("conversations.json"):
            try:
                with open("conversations.json", "r", encoding="utf-8") as f:
                    self.conversations = json.load(f)
                if not self.conversations:
                    self.conversations = [{'title': 'First conversation', 'content': ''}]
            except Exception as e:
                print(f"Error loading conversations: {e}")
                self.conversations = [{'title': 'First conversation', 'content': ''}]
        else:
            self.conversations = [{'title': 'First conversation', 'content': ''}]

    def save_conversations(self):
        try:
            with open("conversations.json", "w", encoding="utf-8") as f:
                json.dump(self.conversations, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving conversations: {e}")

    def show_history(self):
        dialog = HistoryWindow(self, self.conversations)
        dialog.exec()

    def search_country(self):
        query = self.search_input.text().strip()
        if not query: return

        # Якщо це перше повідомлення в цій розмові, встановлюємо заголовок
        if not self.conversations[self.current_index]['content']:
            self.conversations[self.current_index]['title'] = query

        # Оновлюємо поточну розмову в пам'яті
        self.conversations[self.current_index]['content'] += f"{name}: {query}\n"
        self.info_area.append(f"{name}: {query}")
        self.search_input.clear()
        self.save_conversations()
        
        try:
            response = client.chat.completions.create(
                model="glm-4.7-flash",
                messages=[{"role": "user", "content": query}]
            )
            ai_text = response.choices[0].message.content
            # конвертор в markdown
            def replace_bold(match):
                global bold_toggle
                bold_toggle = not bold_toggle
                return '<b>' if bold_toggle else '</b>'

            result = re.sub(r'\*\*|__', replace_bold, ai_text)
            result = re.sub(r'~', '<s>', result)
            self.conversations[self.current_index]['content'] += f"Z.AI: {ai_text}\n"
            self.info_area.append(f"Z.AI: {result}\n")
            self.save_conversations()
            p.playsound("done.mp3")
        except Exception as e:
            self.info_area.append(f"Error: {str(e)}")
            self.save_conversations()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AIApp()
    ex.show()
    sys.exit(app.exec())
