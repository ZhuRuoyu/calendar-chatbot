# thanks to https://levelup.gitconnected.com/auto-detect-anything-with-custom-named-entity-recognition-ner-c89d6562e8e9

pip install -U pip setuptools wheel
pip install -U spacy
#python -m spacy download en_core_web_sm 
python -m spacy download en_core_web_lg

#A config.cfg file will appear in your working directory.

python -m spacy init fill-config base_config.cfg config.cfg


#brgin training After training is complete, the resulting model will appear in a new folder called output.
#python -m spacy train config.cfg — output ./output
python -m spacy train config.cfg --output ./output


