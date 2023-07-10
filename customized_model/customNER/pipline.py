  
!pip install sentence_transformers

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
# import pandas as pd
# import spacy
# from spacy import displacy
# from spacy.tokens import DocBin
# import json
# from datetime import datetime
# from tqdm import tqdm
# import re

# GLOBAL
model_pretrained = 'bert-base-nli-mean-tokens'
model = SentenceTransformer(model_pretrained)

ner_model_path = 'drive/MyDrive/capstone_ner_output'
ner_output = spacy.load(ner_model_path + "/model-best")

intents = [
    "create a new event", #0
    "delete a certain event",#1
    "retrieve event detail of a certain date", #2 -> TAG: retrieving event (intent) today (entity arguments)
    "get free time information during certain time period", #3
    "change the location or summary of an event",#4
    "reschedule the time of an event" #5
    ]

intents_embed_given = model.encode(intents)




