# Personalized-Calendar-Chatbot

-------------------------
Questions: 
- 

--------------------------


## Fundamental Model 
use GPT-3.5 API to detect intentions and extract the args/entities, and make a function call (call Google Calendar API)



## Customized Model

### Step 0: pre-build sentences 

Prepared 6 pre-build sentences which leads to different tasks in google calendar. e.g.
       

    "create a new event", #0
    "delete a certain event",#1
    "retrieve event detail of a certain date", #2 -> TAG: retrieving event (intent) today (entity arguments)
    "get free time information during certain time period", #3
    "change the location or summary of an event",#4
    "reschedule the time of an event" #5
    
    ...


### Step 1: intent recognition
For each user's input, find the most similar pre-build sentence and understand user's intention. e.g. 'create new event','delete event' or 'reshedule event' ...

How: use Transformer (pre-trained BERT `sentence_transformers` library or a fined-tuned version) to create sentence embedding, and use consine similarity to find the closed sentence.

Fine-tune: TBC

Structure: Build a 6-class classification model to classify the intent of users' input

if match -> go to Step 2
if can't decide between 2 intents -> ask detail. Get more information and go to Step 2
if no -> ask again


### Step 2: entities recognition (customized NER)
    
Use name entities recognition (NER) method to extract key information for the selected pre-build sentence

How (custom NER): use Spacy to tag and train customized NER model, key words: date, event_id, summary, start_time, end_time, location


        
### Step 3: combine intent recognition + customized NER

for each intent, find if all required keywords are found. 
if yes, -> go to Step 4
if no, -> ask more information

#### Challenge 
1. Q: What if the user's input (request) is beyond the scope?
   
   A: First, try to match the best sentences. Second, make a follow up question (let the user providing more details or asking in a different way)
  
2. Q: The model can not remember context from the past.

  A: Give the whole conversation (or 2 most recent sentence) to the model and find the best match again.

### Step 4: call Google Calendar API accordingly
call corresponding google calendar API based on the information extracted. 




### Step 5: combine the retrived information into a complete sentence

... TBC
