# 📋 Professional To-Do Dashboard

A robust, dark-themed desktop application for managing daily tasks. Built with **Python** and **Tkinter**, this dashboard offers persistent data storage, task prioritization, and productivity statistics in a clean, professional user interface.

![Project Screenshot]
<img width="2864" height="1601" alt="Screenshot 2026-01-06 122418" src="https://github.com/user-attachments/assets/062f2b8d-d336-483a-b668-0c8683f7bb80" />

## ✨ Key Features

* **🎨 Professional UI:** A custom dark-themed interface (`#1a1a2e`) designed for long-term usage without eye strain.
* **📊 Live Statistics:** Real-time tracking of Total, Completed, and Pending tasks.
* **🔥 Priority Management:** Visual indicators for **Low** (Blue), **Medium** (Orange), and **High** (Red) priority tasks.
* **💾 Auto-Save:** Tasks are automatically saved to a local `tasks.json` file, ensuring you never lose data.
* **✅ Task Actions:**
    * **Add:** Create tasks with titles and detailed descriptions.
    * **Edit:** Update task details and change priorities seamlessly.
    * **Complete:** Mark tasks as done with a strikethrough visual.
    * **Delete:** Remove tasks with a confirmation safety prompt.


## 🛠️ Technology Stack

* **Language:** Python 3.x
* **GUI Library:** Tkinter (Standard Library)
* **Data Storage:** JSON (Local File System)

## 🚀 How to Run

Since this application uses Python's standard libraries, there are **no external dependencies** to install.

1.  **Clone the repository** (or download the files):
    ```bash
    git clone [https://github.com/sufia0/To-do-list.git](https://github.com/sufia0/To-do-list.git)
    cd To-do-list
    ```

2.  **Run the application:**
    ```bash
    python To-do list.py
    ```
    *(Note: If your script is named something else, replace `To-do list.py` with your filename)*

## 📂 Project Structure

```text
├── To-do list.py          # The main application source code
├── tasks.json       # Created automatically to store your tasks
└── README.md        # Documentation
