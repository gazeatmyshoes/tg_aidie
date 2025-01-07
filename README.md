# AI Diary Bot

AI Diary Bot is a Telegram bot designed to help users maintain a personal diary using artificial intelligence. The bot includes features such as voice input, automatic reflection questions, sentiment analysis, goal tracking, and psychology-based recommendations. All user actions are accessible through a visual menu using Inline Keyboard.

## Features

1. **Voice Input (Speech-to-Text)**
   - Converts voice messages to text using Google Cloud Speech-to-Text API.

2. **Automatic Reflection Questions**
   - Sends random reflection questions to the user.

3. **Sentiment Analysis**
   - Analyzes the sentiment of the user's text using Google Cloud Natural Language API.

4. **Goal Setting and Tracking**
   - Helps users set and track personal goals.

5. **Psychology-Based Recommendations**
   - Provides psychological advice and recommendations to improve mood and productivity.

6. **Visual Menu with Inline Keyboard**
   - All main functions are accessible through a visual menu with buttons.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/gazeatmyshoes/tg_aidie.git
   cd tg_aidie
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Google Cloud:
   - Create a project in Google Cloud and enable the Speech-to-Text and Natural Language APIs.
   - Download the service account key file and set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable.

4. Set up Firebase:
   - Create a project in Firebase and set up a database for storing user goals.
   - Download the Firebase service account key file and initialize Firebase Admin SDK.

5. Run the bot:
   ```bash
   python bot.py
   ```

## Requirements

- Python 3.8 or higher
- `python-telegram-bot`
- `google-cloud-speech`
- `google-cloud-language`
- `firebase-admin`

## Usage

- Start the bot by sending the `/start` command.
- Use the visual menu to interact with the bot's features.

## License

This project is licensed under the MIT License.