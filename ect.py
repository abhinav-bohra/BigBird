import csv
import json
import os
import datasets

_CITATION = "None"
_DESCRIPTION = "None"
_HOMEPAGE = "None"
_LICENSE = "None"
_DOCUMENT = "article"
_SUMMARY = "abstract"

# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class Ect(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.1.0")

    def _info(self):
        features = datasets.Features(
                {
                    _DOCUMENT: datasets.Value("string"),
                    _SUMMARY: datasets.Value("string")
                }
            )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,  
            supervised_keys=(_DOCUMENT, _SUMMARY),
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        data_dir = "/content/ECTSumm/data/reuters/Longformer/"
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "train.txt"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "test.txt"),
                    "split": "test"
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "val.txt"),
                    "split": "val",
                },
            ),
        ]

    # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    def _generate_examples(self, filepath, split):
        # TODO: This method handles input defined in _split_generators to yield (key, example) tuples from the dataset.
        # The `key` is for legacy reasons (tfds) and is not important in itself, but must be unique for each example.
        with open(filepath, encoding="utf-8") as f:
            for line in f:
                d = json.loads(line)
                summary = "\n".join(d["abstract_text"])
                yield d["article_id"], {
                    _DOCUMENT: "\n".join(d["article_text"]),
                    _SUMMARY: summary,
                }
