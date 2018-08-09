from unittest import TestCase
from core.nlp.Lemmatiser import Lemmatiser

class TestLemmatiser(TestCase):
    def test_lemmatise_sentence(self):
        lemmatiser = Lemmatiser()

        lemmas = lemmatiser.lemmatise_sentence('I like cats')
        self.assertEqual(lemmas, ['I', 'like', 'cat'])

        lemmas = lemmatiser.lemmatise_sentence('I don\'t like cats')
        self.assertEqual(lemmas, ['I', 'do', 'not', 'like', 'cat'])

        lemmas = lemmatiser.lemmatise_sentence('Let\'s go dance')
        self.assertEqual(lemmas, ['let', 'us', 'go', 'dance'])


