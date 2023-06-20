# Personalized-Calendar-Chatbot

-------------------------
Questions: 
- 

--------------------------


## Fundamental Model 
use GPT-3.5 API to detect intentions and extract the args/entities, and make a function call (call Google Calendar API)



## Customized Model

### Step 0: pre-build sentences 

Prepared 10 pre-build sentences which leads to different tasks in google calendar. e.g.
       
        "Creating an event", 
        "retrieving event of today", 
        "retrieving event of tomorrow", 
        "retrieving event of next month", 
        "add one new event",   
        "check event attendees", 
        "delete a event",
        "retrieving event of next week", 
    
    ...


### Step 1: intent recognition
For each user's input, find the most similar pre-build sentence. 

How: use Transformer (pre-trained BERT `sentence_transformers` library or a fined-tuned version) to create sentence embedding, and use consine similarity to find the closed sentence.

Structure: Build a 10-class classification model to classify the intent of users' input


### Step 2: entities recognition
    
Use name entities recognition (NER) method to extract key information for the selected pre-build sentence

#### Challenge 
1. Q: What if the user's input (request) is beyond the scope?
   
   A: First, try to match the best sentences. Second, make a follow up question (let the user providing more details or asking in a different way)
  
2. Q: The model can not remember context from the past.

  A: Give the whole conversation (or 2 most recent sentence) to the model and find the best match again.
        

### Step 3: call Google Calendar API accordingly
call corresponding google calendar API based on the information extracted. 




### Step 4: combine the retrived information into a complete sentence

... TBC
