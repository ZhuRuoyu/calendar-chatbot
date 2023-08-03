# Personalized Calendar Chatbot

This is a personalized calendar chatbot powered by OpenAI's GPT-3.5 language model. The chatbot is designed to assist you with various tasks related to your Google Calendar.

## Features

The chatbot can perform the following functions:

- **Get Events on a Specific Date**: You can ask the chatbot to retrieve the events on a specific date from your Google Calendar.

- **Create New Event**: The chatbot allows you to create a new event in your Google Calendar. You need to provide the event summary, start time, and end time.

- **Delete Event**: If you want to remove an event from your Google Calendar, you can ask the chatbot to delete it. You will need to provide the event ID for deletion.

- **Get Free/Busy Information**: The chatbot can provide free/busy information from your Google Calendar for a specified time range.

- **Update Existing Event**: You can ask the chatbot to update an existing event in your Google Calendar. You can modify the event summary, start time, end time, or location.

- **Reschedule Event**: If you need to reschedule an event, you can instruct the chatbot to update the event's start and end times.

## How to Interact with the Chatbot

To interact with the chatbot, use the input field on the left side of the application. Type your messages and click the "Send" button to chat with the chatbot. The chat history will appear on the right side, showing your messages and the chatbot's responses.

Please note that the chatbot's functionality is limited to the Google Calendar operations mentioned above.

## How the Code Works

The code uses the Streamlit library to create a web-based interface for the chatbot. It also utilizes the OpenAI GPT-3.5 language model to generate responses for the chatbot. The chatbot communicates with the Google Calendar API to perform the requested calendar operations.

When you interact with the chatbot, your messages and the chatbot's responses are stored in a conversation context. The context is used to maintain the conversation history and make follow-up queries to the Google Calendar API.

The chatbot is capable of processing your messages and interpreting function calls to perform specific operations on your Google Calendar. You can ask the chatbot to retrieve, create, delete, update, and reschedule events by providing the necessary information in your messages.

Please ensure you have the appropriate API keys and credentials set up to run the code with the Google Calendar API and OpenAI GPT-3.5 language model.

Enjoy using the Personalized Calendar Chatbot!
