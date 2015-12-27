from data_model import *
import json
import urllib2


class Request:

    def __init__(self, api_key, txt):
        self.url = None
        self.txt = txt.lower()
        self.url_template = "https://access.alchemyapi.com/calls/data/GetNews?" \
                            "apikey=" + api_key + "&return=enriched.url.title,enriched.url.url,enriched.url.author," \
                            "enriched.url.publicationDate," \
                            "enriched.url.enrichedTitle.entities," \
                            "enriched.url.enrichedTitle.docSentiment,enriched.url.enrichedTitle.concepts&start=" \
                            "1450396800&end=1451084400&q.enriched.url.enrichedTitle.entities.entity=|" \
                            "text=" + txt + ",type=company|&q.enriched.url.enrichedTitle.docSentiment." \
                            "type=positive&count=25&outputMode=json"

    def parse_alchemi_json(self, data):
        ret = []
        jsraw = json.loads(data)
        result = jsraw["result"]
        news = result["docs"]
        for item in news:
            temp = DataModel()
            target = item["source"]['enriched']['url']
            temp.url = target['url']
            temp.title = target['title']
            for ent in target['enrichedTitle']['entities']:
                en = Entity(ent['count'], ent['text'], ent['type'])
                temp.entities.append(en)
            for concept in target['enrichedTitle']['concepts']:
                conc = Concept(concept['relevance'], concept['text'])
                temp.concept.append(conc)
            senti = target['enrichedTitle']['docSentiment']
            temp.sentiment = Sentiment(senti['mixed'], senti['score'], senti['type'])
            temp.author = target['author']
            ret.append(temp)
        return ret

    def request(self, is_file=True):

        if is_file:
            file_name = self.txt + '.json'
            with open('TCS.json') as file_content:
                ret = file_content.read()
            data = self.parse_alchemi_json(ret)
        else:
            ret = urllib2.urlopen(self.url_template).read()
            data = self.parse_alchemi_json(ret)
        return data




