# 🎮 Discord Quiz Bot - Your Ultimate Quizmaster 🧠
Welcome to the **Discord Quiz Bot**  project! This bot can host exciting quizzes directly in your Discord server, track your progress, and crown the top quizzers on the leaderboard! Whether you're a trivia enthusiast or just looking for some friendly competition, this bot has got you covered. 🎉

## 🚀 Features
- **Custom Quizzes**: Create quizzes with as many questions as you want.
- **Time Challenge**: Users have **30 seconds** to answer each question.
- **Leaderboard**: Automatically tracks correct answers and displays the top scorers on demand.

## 🛠️ Admin Portal
The admin portal is built with **ReactJS** and offers a clean, intuitive interface:
- **Add, View, and Delete Questions** effortlessly.
- Includes an **About Page** with details about the project’s inspiration and goals.
- **Pushes all data** to a **Django**-powered database.
## 🎯 Quick Setup Guide

### 1️⃣ Start the Admin Page
```bash
cd quiz-frontend
npm install
npm start
# This will install all dependencies, including:
#    ReactRouterDom
#   React-Bootstrap
```

### 2️⃣ Start the Discord Bot
Before running the bot, don’t forget to replace the necessary API keys in config.ini under discord_sdk!

```bash
python3 Botmanager.py
```
### 3️⃣ Start the Django Database
```bash
Copy code
python3 manage.py runserver
```

With everything running, you’re ready to go! 🎉

⚙️ Dependencies
Make sure to install these Python modules as well:
- **Django**
- **DjangoRestFramework**
- And others as needed!

## 🎉 Final Words
This is my first project ever, and I'm thrilled to share it with you all. I'll be back with even more awesome projects soon. Until then, Hasta La Vista! 👋