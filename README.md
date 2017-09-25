# symtopspot
Symptomspot is a simple symptom string extractor based on the [Symptom 
Ontology](symptomontologywiki.igs.umaryland.edu) developed at the Institute 
for Genome Sciences (IGS) at the University of Maryland. The symptom strings
are extracted using [SpaCy's custom entity matching](https://spacy.io/docs/usage/rule-based-matching).

### Installation
Install requirements, download spacy model and download git repository. 
The lightest model should suffice for this purpose.
```
pip install -r requirements.txt
python -m spacy download en
pip install git+https://github.com/mlehl88/symptomspot.git
```

### Usage

#### As a Python library
Use the `SymptomExtractor` to extract unique symtom strings from a text or URL:
```
>>> from symptomspot.extractor import SymptomExtractor
>>> extractor = SymptomExtractor()
>>> extractor.extract(text='I have a back pain')
['back pain', 'pain']
>>> extractor.extract(url='www.nhs.uk/Conditions/Sleep-paralysis/Pages/Symptoms.aspx')
['inability to move', 'hallucinations', 'anxiety']
```

#### As a web service

Usage with input text:

```
python symptomspot/app.py
curl -X POST 'localhost:5000/symptomspot/text' -d "text=The Trump anxiety."
```

Usage with input URL:

```
curl -X POST 'localhost:5000/symptomspot/url' -d "url=www.nhs.uk/Conditions/Sleep-paralysis/Pages/Symptoms.aspx"
```

### Evaluation

Run the evaluation script for a lightweight evaluation of 8 labelled documents:
```
python eval/eval.py
```
