import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class NLTKManager:
    def __init__(self):
        self.sid = SentimentIntensityAnalyzer()

    def evaluate_sentence(self, sentence):
        scores = self.sid.polarity_scores(sentence)
        scores['text'] = sentence
        return scores

    def evaluate_sentences(self, sentences):
        return list(map(self.evaluate_sentence, sentences))

    def evaluate_messages(self, messages):
        sentences = list(map(lambda m: m['text'], messages))
        return self.evaluate_sentences(sentences)