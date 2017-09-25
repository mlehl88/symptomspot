import argparse

import spacy

from newspaper import Article
from owlready2 import get_ontology
from spacy.matcher import Matcher
from spacy.attrs import LOWER

# Symptom ontology created at the Institute for Genome Sciences (IGS) at the University of Maryland
ONTOLOGY_URL = 'http://purl.obolibrary.org/obo/symp.owl'
# label of most general concept in the ontology
SYMPTOM = 'symptom'


class SymptomExtractor(object):
    """Extract symptoms from a text or web page specified by a URL.

    Example Usage
    -------------

    >>> from symptomspot.extractor import SymptomExtractor
    >>> extractor = SymptomExtractor()
    >>> extractor.extract(text='I have a back pain')
    ['back pain', 'pain']
    >>> extractor.extract(url='www.nhs.uk/Conditions/Sleep-paralysis/Pages/Symptoms.aspx')
    ['inability to move', 'hallucinations', 'anxiety']
    """

    def __init__(self):
        self.nlp = spacy.load('en', tagger=None, parser=None, entity=None)
        self.matcher = Matcher(self.nlp.vocab)
        self.add_symptom_classes()

    @staticmethod
    def get_ontology_classes(ontology_url=ONTOLOGY_URL):
        onto = get_ontology(ontology_url)
        onto.load()
        return onto.classes()

    def add_symptom_classes(self):
        """Add symptom entities and patters to self.matcher for custom entity matching.
        Acquire symptom entities from the Symptom Ontology created at the Institute for
        Genome Sciences (IGS) at the University of Maryland."""
        symptom_classes = self.get_ontology_classes(ONTOLOGY_URL)
        all_labels_set = set()  # keep track of all added labels to avoid duplicate patterns

        for cl in symptom_classes:
            # acquire the labels of the class and its synonyms and sort by string length
            all_labels = sorted(cl.label + cl.hasExactSynonym, key=lambda s: len(s))

            # ignore the uppermost concept in the ontology (avoid string 'symptom' being matched)
            if SYMPTOM in all_labels:
                continue

            # use shortest of the synonym labels as entity ID and create entity
            entity_id = all_labels[0].replace(" ", "_")
            self.matcher.add_entity(entity_id,
                                    attrs={"ent_type": "SYMPTOM"},
                                    if_exists='ignore')

            # add the label and its synonyms as entity patterns avoiding duplicates
            for label in all_labels:
                if label not in all_labels_set:
                    self.matcher.add_pattern(
                        entity_id,
                        [{LOWER: token} for token in label.split(" ")]
                    )
                all_labels_set.add(label)

    def extract_from_text(self, text):
        """Extract symptom strings from specified text.

        Returns
        -------
        match_terms : a list of non-repeating symptom match terms
        """
        doc = self.nlp(text)
        matches = self.matcher(doc)
        match_terms = [str(doc[match[2]:match[3]]).lower() for match in matches]
        match_terms = list(set(match_terms))
        return match_terms

    def extract_from_url(self, url):
        """Extract symptom strings from specified web page.

        Returns
        -------
        match_terms : a list of non-repeating symptom match terms
        """
        a = Article(url)
        a.download()
        a.parse()
        return self.extract_from_text(a.text)

    def extract(self, text=None, url=None):
        if text:
            return self.extract_from_text(text)
        else:
            return self.extract_from_url(url)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Symptom Extractor based on the Symptom Ontology '
                                                 'of the Institute for Genome Sciences (IGS) at '
                                                 'the University of Maryland.')
    parser.add_argument('--text', dest='text', default=None,
                        help='Text to extract from')
    parser.add_argument('--url', dest='url', default=None,
                        help='URL of page to extract from')

    args = parser.parse_args()

    if not args.text and not args.url:
        parser.error('Neither text nor URL provided for extraction.')

    extractor = SymptomExtractor()
    print(extractor.extract(text=args.text, url=args.url))
