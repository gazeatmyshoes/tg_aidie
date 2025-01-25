# TGAidie

This is a Telegram bot for diary and mood tracking. It uses Yandex Natural Language API for sentiment analysis and supports 5 languages: russian, english, german, french, and spanish.

## Setup

To set up the bot, you need to create a Zadex API key and configure the following environment variables:

1. Create a Zadex API key at https://cloud.yandex.com/.

2. Add the following environment variables to your `.env` file:

   ```bash
   YANDEX_API_KEY=your_yandex_api_key
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   GOOGLE_APPLICATION_CREDENTIALS=your_google_application_credentials
   FIREBASE_DATABASE_URL=your_firebase_database_url
   ```

3. Run the bot using the following command:

   ```bash
   python3.8 run_bot.py
   ```

## Language Support

The bot supports the following languages:

- Russian (`ru`)
- English (`en`)
- German (`de`)
- French (`ru`)
- Spanish (`es`)

## Contributing

Please fork the repository and create a pull request for any changes you would like to make. Make sure to update the changelog and test your changes.

## License

This project is open-source and licensed under the MIT License. See the `LICENSE` file for more information.
