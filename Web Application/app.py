import streamlit as st
import openai
import json
from google.oauth2 import service_account
import googleapiclient.discovery
import re

# Set the title of the Streamlit app and other configurations
st.set_page_config(page_title="Personalized Calendar Chatbot", page_icon=":calendar:")

# Load and set our OpenAI API key
openai.api_key = open("key.txt", "r").read().strip("\n")

# Load and set Google Calendar API credentials
credentials = service_account.Credentials.from_service_account_file('cedar-bot-391819-76c731233383.json')
calendar_service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)

def about_page():
    st.title("About")
    st.markdown("""
    This is a personalized calendar chatbot powered by OpenAI's GPT-3.5 language model. It can assist you with various tasks related to your Google Calendar.

    Some of the things it can do for you:
    
    - Get the events on a specific date from your Google Calendar.
    - Create a new event in your Google Calendar.
    - Delete an event from your Google Calendar.
    - Get free/busy information from your Google Calendar.
    - Update an existing event in your Google Calendar.
    - Reschedule an event in your Google Calendar.

    Feel free to interact with the chatbot using the input field on the left. Type your messages, and click the "Send" button to chat with the chatbot.

    Please note that the functionality of the chatbot is limited to the Google Calendar operations mentioned above.

    For any questions or feedback, you can contact the developer at onenishitrathod@gmail.com.
    """)

def developers_page():
    st.title("Developers")
    st.markdown("""
    Meet the team behind the Personalized Calendar Chatbot:
    
    **Developer 1**
    - Name: Nishit Rathod
    - Nishit Rathod is an aspiring Data Scientist with a strong foundation in statistical modeling, deep learning and programming languages like SQL, Python, and R. With over 1 year of work experience in data science and machine learning, Nishit has demonstrated expertise in data wrangling, exploratory data analysis, predictive modeling, neural networks, natural language processing and large language models. Nishit is passionate about using data to uncover insights and make informed decisions with dynamic solutions, and has a proven track record of delivering actionable insights. With a background in Artificial Intelligence and Machine Learning from Humber College and a Bachelor's degree in Data Science from Christ (Deemed to be University), Nishit is equipped to tackle real-world data challenges. Additionally, Nishit has contributed to various internships and virtual experiences with reputed organizations like SAP, Boston Consulting Group (BCG), and KPMG, gaining exposure to data science applications in different domains. Nishit's strong interpersonal skills, including communication, organization, business acumen and leadership, complement their technical prowess, making them a valuable asset in any data-driven organization.
    - Email: onenishitrathod@gmail.com
    - LinkedIn: [Nishit Rathod LinkedIn Profile](https://www.linkedin.com/in/onenishit/)
    - GitHub: [Nishit Rathod GitHub Profile](https://github.com/OneNishitRathod)
    
    **Developer 2**
    - Name: Jane Smith
    - Email: jane.smith@example.com
    - GitHub: [jane_smith](https://github.com/jane_smith)
    
    **Developer 3**
    - Name: Tom Johnson
    - Email: tom.johnson@example.com
    - GitHub: [tom_johnson](https://github.com/tom_johnson)
    
    **Developer 4**
    - Name: Emily Lee
    - Email: emily.lee@example.com
    - GitHub: [emily_lee](https://github.com/emily_lee)
    """)

def get_user_message():
    # Function to get user input
    return st.text_input("You: ")

def display_chat_history(conversation_context):
    for message in conversation_context:
        if message['role'] == 'user':
            st.text_area("You:", value=message['content'], height=50, max_chars=None, key=f"user_message_{message['timestamp']}")
        elif message['role'] == 'assistant':
            st.text_area("Bot:", value=message['content'], height=50, max_chars=None, key=f"bot_response_{message['timestamp']}")

def get_calendar_events(date):
    """Get the events on a given date from Google Calendar"""
    events_result = calendar_service.events().list(
        calendarId='iamnishitrathod@gmail.com',
        timeMin=f'{date}T00:00:00Z',
        timeMax=f'{date}T23:59:59Z',
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    formatted_events = []
    for event in events:
        formatted_event = {
            "summary": event['summary'],
            "start_time": event['start'].get('dateTime', event['start'].get('date')),
            "location": event.get('location', 'N/A'),
        }
        formatted_events.append(formatted_event)

    return json.dumps({"date": date, "events": formatted_events})

def create_event(summary, start_time, end_time, location=None):
    """Create a new event in Google Calendar"""
    event = {
        'summary': summary,
        'start': {
            'dateTime': start_time,
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'UTC',
        },
    }

    if location:
        event['location'] = location

    created_event = calendar_service.events().insert(calendarId='iamnishitrathod@gmail.com', body=event).execute()
    return json.dumps({"event_id": created_event['id'], "summary": created_event['summary'], "status": "created"})

def delete_event(event_id):
    """Delete an event from Google Calendar"""
    calendar_service.events().delete(calendarId='iamnishitrathod@gmail.com', eventId=event_id).execute()
    return json.dumps({"event_id": event_id, "status": "deleted"})

def get_free_busy_info(start_time, end_time):
    """Get free/busy information from Google Calendar"""
    free_busy_query = {
        "timeMin": start_time,
        "timeMax": end_time,
        "items": [{"id": "iamnishitrathod@gmail.com"}],
    }

    free_busy_info = calendar_service.freebusy().query(body=free_busy_query).execute()
    return json.dumps(free_busy_info)

def update_event(event_id, summary=None, start_time=None, end_time=None, location=None):
    """Update an event in Google Calendar"""
    event = calendar_service.events().get(calendarId='iamnishitrathod@gmail.com', eventId=event_id).execute()

    if summary:
        event['summary'] = summary
    if start_time:
        event['start']['dateTime'] = start_time
    if end_time:
        event['end']['dateTime'] = end_time
    if location:
        event['location'] = location

    updated_event = calendar_service.events().update(calendarId='iamnishitrathod@gmail.com', eventId=event_id, body=event).execute()
    return json.dumps({"event_id": updated_event['id'], "summary": updated_event['summary'], "status": "updated"})

def reschedule_event(event_id, start_time, end_time):
    """Reschedule an event in Google Calendar"""
    return update_event(event_id, start_time=start_time, end_time=end_time)

# Function definitions for calendar-related queries
functions = [
    {
        "name": "get_calendar_events",
        "description": "Get the events on a given date from Google Calendar",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "The date for which to retrieve events (in 'YYYY-MM-DD' format)",
                },
            },
            "required": ["date"],
        },
    },
    {
        "name": "create_event",
        "description": "Create a new event in Google Calendar",
        "parameters": {
            "type": "object",
            "properties": {
                "summary": {
                    "type": "string",
                    "description": "The summary or title of the event",
                },
                "start_time": {
                    "type": "string",
                    "description": "The start time of the event (in RFC3339 format)",
                },
                "end_time": {
                    "type": "string",
                    "description": "The end time of the event (in RFC3339 format)",
                },
                "location": {
                    "type": "string",
                    "description": "The location of the event (optional)",
                },
            },
            "required": ["summary", "start_time", "end_time"],
        },
    },
    {
        "name": "delete_event",
        "description": "Delete an event from Google Calendar",
        "parameters": {
            "type": "object",
            "properties": {
                "event_id": {
                    "type": "string",
                    "description": "The ID of the event to be deleted",
                },
            },
            "required": ["event_id"],
        },
    },
    {
        "name": "get_free_busy_info",
        "description": "Get free/busy information from Google Calendar",
        "parameters": {
            "type": "object",
            "properties": {
                "start_time": {
                    "type": "string",
                    "description": "The start time for querying free/busy information (in RFC3339 format)",
                },
                "end_time": {
                    "type": "string",
                    "description": "The end time for querying free/busy information (in RFC3339 format)",
                },
            },
            "required": ["start_time", "end_time"],
        },
    },
    {
        "name": "update_event",
        "description": "Update an event in Google Calendar",
        "parameters": {
            "type": "object",
            "properties": {
                "event_id": {
                    "type": "string",
                    "description": "The ID of the event to be updated",
                },
                "summary": {
                    "type": "string",
                    "description": "The new summary or title of the event (optional)",
                },
                "start_time": {
                    "type": "string",
                    "description": "The new start time of the event (in RFC3339 format) (optional)",
                },
                "end_time": {
                    "type": "string",
                    "description": "The new end time of the event (in RFC3339 format) (optional)",
                },
                "location": {
                    "type": "string",
                    "description": "The new location of the event (optional)",
                },
            },
            "required": ["event_id"],
        },
    },
    {
        "name": "reschedule_event",
        "description": "Reschedule an event in Google Calendar",
        "parameters": {
            "type": "object",
            "properties": {
                "event_id": {
                    "type": "string",
                    "description": "The ID of the event to be rescheduled",
                },
                "start_time": {
                    "type": "string",
                    "description": "The new start time of the event (in RFC3339 format)",
                },
                "end_time": {
                    "type": "string",
                    "description": "The new end time of the event (in RFC3339 format)",
                },
            },
            "required": ["event_id", "start_time", "end_time"],
        },
    },
]

# Chat with the personalized calendar chatbot
context = [
    {"role": "user", "content": "What events do I have?"},
    {"role": "assistant", "content": 'I will check your calendar for events.'},
    {"role": "assistant", "content": 'Assistant to=functions.get_calendar_events'},
    {"role": "user", "content": "Tell me about my events."},
    {"role": "assistant", "content": "You don't have any events scheduled."},
    {"role": "user", "content": "Create a new event"},
    {"role": "assistant", "content": 'Assistant to=functions.create_event'},
    {"role": "user", "content": "Delete the event with ID XYZ"},
    {"role": "assistant", "content": 'Assistant to=functions.delete_event'},
    {"role": "user", "content": "Get free/busy information"},
    {"role": "assistant", "content": 'Assistant to=functions.get_free_busy_info'},
    {"role": "user", "content": "Update the event with ID XYZ"},
    {"role": "assistant", "content": 'Assistant to=functions.update_event'},
    {"role": "user", "content": "Reschedule the event with ID XYZ"},
    {"role": "assistant", "content": 'Assistant to=functions.reschedule_event'},
]

def parse_event_details(event_details):
    # Extract the event details from the user input
    event_args = re.findall(r'(?:"[^"]*"|\S)+', event_details)
    if len(event_args) >= 3:
        summary = event_args[0].strip('"')
        start_time = event_args[1].strip('"')
        end_time = event_args[2].strip('"')
        location = None
        if len(event_args) >= 4:
            location = event_args[3].strip('"')
        return {
            "summary": summary,
            "start_time": start_time,
            "end_time": end_time,
            "location": location,
        }
    else:
        return {}

def process_user_message(user_message, context, credentials):
    if user_message:
        # Append the user message to the conversation context
        context.append({"role": "user", "content": user_message})

        # Generate a response from the chatbot
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=context,
            functions=functions,
            max_tokens=500,
        )

        # Check if there's a function call in the response
        if response.choices[0].message.get("function_call"):
            fn_name = response.choices[0].message["function_call"]["name"]
            arguments = response.choices[0].message["function_call"]["arguments"]

            # Convert string to dictionary if necessary
            if isinstance(arguments, str):
                arguments = json.loads(arguments)

            # Call the appropriate function
            if fn_name == "get_calendar_events":
                response = get_calendar_events(**arguments)
            elif fn_name == "create_event":
                # If 'arguments' is a string, parse the event details from it
                if isinstance(arguments, str):
                    arguments = parse_event_details(arguments)
                response = create_event(**arguments)  
            elif fn_name == "delete_event":
                response = delete_event(**arguments)  
            elif fn_name == "get_free_busy_info":
                response = get_free_busy_info(**arguments)
            elif fn_name == "update_event":
                response = update_event(**arguments)
            elif fn_name == "reschedule_event":
                response = reschedule_event(**arguments)
           
            # Append the function call and response to the conversation context
            context.append(
                {
                    "role": "assistant",
                    "content": None,
                    "function_call": {"name": fn_name, "arguments": json.dumps(arguments)},
                }
            )
            context.append(
                {
                    "role": "function",
                    "name": fn_name,
                    "content": f"response: {str(response)}",
                }
            )
            
            # Generate a response from the chatbot
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=context,
                functions=functions,
                max_tokens=500,
            )

        # Retrieve the assistant's reply from the response
        assistant_reply = response['choices'][0]['message']['content']
        context.append({"role": "assistant", "content": assistant_reply})

        return assistant_reply, context
    else:
        return "", context

def main():
    # Set your OpenAI API key here (replace 'YOUR_API_KEY' with your actual API key)
    openai.api_key = "YOUR API KEY"

    # Initialize the conversation context as an empty list
    conversation_context = st.session_state.get("conversation_context", [])

    st.title("Personalized Calendar Chatbot")

    tabs = ["About","Chatbot", "Developers"]
    current_tab = st.sidebar.radio("Personalized Calendar Chatbot", tabs)

    if current_tab == "Chatbot":
        st.markdown("Hi! I'm your chatbot assistant. How can I help you today?")

        user_input = get_user_message()

        if st.button("Send", key="send_button"):
            if user_input.lower() in ["exit", "quit", "bye"]:
                st.write("Bot: Goodbye!")
            else:
                # Process the user message and get the assistant's reply
                assistant_reply, conversation_context = process_user_message(
                    user_input, conversation_context, credentials
                )

                # Display the assistant's reply in a chat-like interface
                st.text_area("Bot:", value=f"Bot: {assistant_reply}", height=100, max_chars=None, key="bot_response")

        # Format and display the full conversation history
        chat_history = "\n".join(
            [f"You: {message['content']}" if message['role'] == 'user' else f"Bot: {message['content']}" for message in conversation_context]
        )
        st.text_area("Chat History:", value=chat_history, height=400, max_chars=None, key="chat_history")

        # Store the conversation context in session state
        st.session_state["conversation_context"] = conversation_context

                
    elif current_tab == "About":
        about_page()

    elif current_tab == "Developers":
        developers_page()

# Custom CSS styling to make the chat-like interface more attractive
st.markdown(
    """
    <style>
    .stTextInput>div>div>input {
        background-color: #C10941 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }

    .stButton>button {
        background-color: #FFFFFF !important;
        color: #4741BB !important;
        font-size: 16px !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        cursor: pointer !important;
    }

    .stTextArea>div>textarea {
        background-color: #f2f2f2 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if __name__ == "__main__":
    main()
