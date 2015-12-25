class Concept:
    def __init__(self, relevance, text):
        self.relevance = relevance
        self.text = text


class Sentiment:
    def __init__(self, mixed, score, typ):
        self.mixed = mixed
        self.score = score
        self.typ = typ


class Entity:
    def __init__(self, count, text, typ):
        self.count = count
        self.text = text
        self.typ = typ


class DataModel:

    def __init__(self):
        self.entities = []
        self.author = ""
        self.sentiment = None
        self.url = ""
        self.title = ""
        self.publication_date = None
        self.concept = []

    def add_entity(self, count, txt, typ):
        en = Entity(count, txt, typ)
        self.entities.append(en)

    def set_sentiment(self, mixed, scope, typ):
        senti = Sentiment(mixed, scope, typ)
        self.sentiment = senti

    def add_concept(self, relevance, txt):
        con = Concept(relevance, txt)
        self.concept.append(con)