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
        sentences_evaluation = list(map(self.evaluate_sentence, sentences))
        return sentences_evaluation

    def evaluate_messages(self, messages):
        sentences = list(map(lambda m: m['text'], messages))
        messages_evaluations = self.evaluate_sentences(sentences)
        return messages_evaluations