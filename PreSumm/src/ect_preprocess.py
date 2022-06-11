import stanza
import os, json
from tqdm import tqdm
from stanza.pipeline.processor import Processor, register_processor, register_processor_variant

@register_processor("lowercase")
class LowercaseProcessor(Processor):
    ''' Processor that lowercases all text '''
    _requires = set(['tokenize'])
    _provides = set(['lowercase'])

    def __init__(self, config, pipeline, use_gpu):
        pass

    def _set_up_model(self, *args):
        pass

    def process(self, doc):
        doc.text = doc.text.lower()
        for sent in doc.sentences:
            for tok in sent.tokens:
                tok.text = tok.text.lower()

            for word in sent.words:
                word.text = word.text.lower()

        return doc


def preproces(s_):
    s = []
    for line in s_:
        if line.startswith("Speaker ::") or line=="\n":
            continue
        else:
            line = line.replace('\n',"").replace("  "," ")
            tokens=[]
            doc = nlp(line)
            for i, sentence in enumerate(doc.sentences):
                tokens.extend([token.text for token in sentence.tokens])
            s.append(tokens)
    return s



if __name__ == "__main__":
    nlp = stanza.Pipeline(lang='en', processors='tokenize,lowercase')
    splits = ["train", "test", "val"] 
    data = []

    for split in splits:
        path_articles = f"/content/Long-Text-Summarization/data/reuters/exp2/{split}/ects"
        path_summaries = f"/content/Long-Text-Summarization/data/reuters/exp2/{split}/gt_summaries"
        if split=="val":
            split="valid"
        outfile = f"/content/Long-Text-Summarization/PreSumm/json_data/ect.{split}.json"
        articles = os.listdir(path_articles)[:10]
        summaries = os.listdir(path_summaries)[:10]
        print(split, len(articles), len(summaries))
        for article in tqdm(articles):
            data_point = {}
            a_ = open(os.path.join(path_articles, article), 'r').readlines()
            a = preproces(a_)
            s_ = open(os.path.join(path_summaries, article), 'r').readlines()
            s = preproces(s_)
            data_point["src"] = a
            data_point["tgt"] = s
            data.append(data_point)

        with open(outfile, "w") as myfile:
            json.dump(data, myfile)
            print(f"{split} done")
        myfile.close()