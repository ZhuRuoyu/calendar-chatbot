from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final = "5916030920:AAFQtcekS3RJEvIDsD5Suw8oTkSBXF1vtP0"
BOT_USERNAME: Final = '@google_calendarbot'


#Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am a Calendar Bot! How may I help you?")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello there! I\'m a bot. What\'s up?')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Try typing anything and I will do my best to respond!')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command, you can add whatever text you want here.')


#Responses
#Here We can use our model!
def handle_response(text: str) -> str:

    processed: str = text.lower()

    if 'hello' in processed or 'hi' in processed:
        return "Hello! I can help you with getting event details, checking available time, and creating/updating/rescheduling/deleting events."

    if 'create event' in processed:
        return "Sure! Please provide the start time, end time, and location of the event."

    if 'get event detail' in processed:
        return "Sure! Fetching the event details."

    if 'update event' in processed:
        return "Sure! What changes do you want to make in your event?"


    if 'reschedule event' in processed:
        return "when do you want to reschedule the event?"

    if 'start time' in processed and 'end time' in processed and 'location' in processed:
        # Extract the start time, end time, and location from the user's input
        start_time = extract_start_time(processed)  # Implement a function to extract the start time
        end_time = extract_end_time(processed)  # Implement a function to extract the end time
        location = extract_location(processed)  # Implement a function to extract the location

        response = f"Great! You entered the following details:\n" \
                   f"Start time: {start_time}\n" \
                   f"End time: {end_time}\n" \
                   f"Location: {location}\n" \
                   f"Is that correct?"

        return response

    # Handle other intents and scenarios
    # ...



    if 'missing information' in processed:
        return "I need more information to create/update/reschedule/delete the event. Could you please provide the start time, end time, or location?"

    if 'not sure' in processed:
        return "Do you want to create an event, update an event, or delete an event?"

    if 'no intents found' in processed:
        return "Sorry, I don't understand. Can you please rephrase your request? I can help with tasks like getting event details, checking available time, and more."

    if 'exit' in processed or 'bye' in processed:
        return "Thank you for using the Calendar Bot. Have a great day!"

    return 'I don\'t understand'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get basic info of the incoming message
    message_type: str = update.message.chat.type
    text: str = update.message.text

    # Print a log for debugging
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    # React to group messages only if users mention the bot directly
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return  # We don't want the bot respond if it's not mentioned in the group
    else:
        response: str = handle_response(text)

    # Reply normal if the message is in private
    print('Bot:', response)
    await update.message.reply_text(response)


# Log errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Log all errors
    app.add_error_handler(error)

    print('Polling...')
    # Run the bot
    app.run_polling(poll_interval=5)
#This is not the final file. 
