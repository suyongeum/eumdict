from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, word_tokenize
from nltk.corpus import wordnet as wn


class Lemmatiser:

    def __init__(self):
        self.wnl = WordNetLemmatizer()
        wn.ensure_loaded()
        self.contractions = {
            'isn\'t': ['is', 'not'],
            'aren\'t': ['are', 'not'],
            'wasn\'t': ['was', 'not'],
            'weren\'t': ['were', 'not'],
            'don\'t': ['do', 'not'],
            'doestn\'t': ['does', 'not'],
            'didn\'t': ['did', 'not'],
            'can\'t': ['cannot'],
            'we\'re': ['we', 'are'],
            'i\'m': ['I', 'am'],
            'it\'s': ['it', 'is'],
            'haven\'t': ['have', 'not'],
            'hasn\'t': ['has', 'not'],
            'hadn\'t': ['had', 'not'],
            'couldn\'t': ['could', 'not'],
            'mightn\'t': ['might', 'not'],
            'mustn\'t': ['must', 'not'],
            'shan\'t': ['shall', 'not'],
            'mayn\'t': ['may', 'not'],
            'shouldn\'t': ['should', 'not'],
            'won\'t': ['will', 'not'],
            'wouldn\'t': ['would', 'not'],
            'daren\'t': ['dare', 'not'],
            'needn\'t': ['need', 'not'],
            'usedn\'t': ['use', 'not'],
            'let\'s': ['let', 'us'],
            'you\'ve': ['you', 'have'],
            'i\'ve': ['I', 'have'],
        }

    def penn_to_wn(self, tag):
        if tag.startswith('J'):
            return wn.ADJ
        elif tag.startswith('N'):
            return wn.NOUN
        elif tag.startswith('R'):
            return wn.ADV
        elif tag.startswith('V'):
            return wn.VERB
        elif tag == 'IN':
            return wn.VERB
        elif tag == 'PRP':
            return wn.ADJ
        return wn.NOUN

    def contractions_filter(self, sentence: str):
        words = sentence.split()
        filtered_words = []
        for word in words:
            if word.lower() in self.contractions:
                filtered_words.extend(self.contractions[word.lower()])
                continue
            filtered_words.append(word)

        return ' '.join(filtered_words)


    def lemmatise_sentence(self, sentence: str):
        filtered_sentence = self.contractions_filter(sentence)
        tagged = pos_tag(word_tokenize(filtered_sentence))
        lemmas = []
        for token in tagged:
            wn_tag = self.penn_to_wn(token[1])
            lemma = self.wnl.lemmatize(token[0], pos=wn_tag)
            lemmas.append(lemma)
        return lemmas
