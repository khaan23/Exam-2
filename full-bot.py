import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters
import os


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Define a few command handlers. These usually take the two arguments update and context.
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Salom qaysi davlat bayramini bilmoqchisiz?'
                                    "Kiritmoqchi bo'lgan davlatni kodini yozing")

async def holiday(update: Update, context: CallbackContext) -> None:
    country_code = update.message.text
    url = f'https://calendarific.com/api/v2/holidays?&api_key=nP5EjQWi9KDHNzVOySuULjOKLdgn6oWW&country={country_code}&year=2024'

    response = requests.get(url)
    response.raise_for_status()  # Raises an HTTPError if the status is 4xx or 5xx
    data = response.json()
    # print(data)
    holidays = data.get('response', {}).get('holidays', [])

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        holidays = data.get('response', {}).get('holidays', [])

        if holidays:
            message = f"Upcoming public holidays in {country_code}:\n"
            for holiday in holidays:
                name = holiday.get('name')
                date = holiday.get('date', {}).get('iso')
                message += f"{name} on {date}\n"
            await update.message.reply_text(message)
        else:
            await update.message.reply_text('No public holidays found.')
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        await update.message.reply_text('Failed to retrieve data. Please try again later.')
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        await update.message.reply_text('An unexpected error occurred. Please try again later.')

def main() -> None:
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6025142350:AAFRs7ikv-EJEsT1WTqE0-MPgH6QBLcPXXc").build()
    # Add a handler for the /start command
    application.add_handler(CommandHandler('start', start))

    application.add_handler(MessageHandler(
        filters=filters.TEXT, callback=holiday))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
