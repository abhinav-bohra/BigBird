"""VLSP dataset."""
import json
import os

import tensorflow as tf
import tensorflow_datasets.public_api as tfds


_DESCRIPTION = """
Scientific papers datasets contains two sets of long and structured documents.

  - input: the body of the document, pagragraphs seperated by "/n".
  - output: the abstract of the document, pagragraphs seperated by "/n".
  - meta_data: titles of sections, seperated by "/n".

"""

_DOCUMENT = "input"
_SUMMARY = "output"

class Vlsp(tfds.core.GeneratorBasedBuilder):
  """DatasetBuilder for VLSP dataset."""

  VERSION = tfds.core.Version('1.0.0')
  RELEASE_NOTES = {
      '1.0.0': 'Initial release.',
  }

  def _info(self) -> tfds.core.DatasetInfo:
    """Returns the dataset metadata."""
    # TODO(VLSP): Specifies the tfds.core.DatasetInfo object
    return tfds.core.DatasetInfo(
        builder=self,
        description=_DESCRIPTION,
        features=tfds.features.FeaturesDict({
            _DOCUMENT: tfds.features.Text(),
            _SUMMARY: tfds.features.Text(),
            "meta_data": tfds.features.Text(),
        }),
        supervised_keys=(_DOCUMENT, _SUMMARY),
        homepage=None,
        citation=None,
    )

  def _split_generators(self, dl_manager: tfds.download.DownloadManager):
    """Returns SplitGenerators."""
    # TODO(VLSP): Downloads the data and defines the splits
    # dl_manager is a tfds.download.DownloadManager that can be used to
    # download and extract URLs
    # dl_paths = dl_manager.download_and_extract(_URLS)
    path = os.path.join("VLSP")
    print(f"Path: {path}")
    
    return [
        tfds.core.SplitGenerator(
            name=tfds.Split.TRAIN,
            gen_kwargs={"path": os.path.join(path, "train.json")},
        ),
        tfds.core.SplitGenerator(
            name=tfds.Split.VALIDATION,
            gen_kwargs={"path": os.path.join(path, "val.json")},
        ),
        tfds.core.SplitGenerator(
            name=tfds.Split.TEST,
            gen_kwargs={"path": os.path.join(path, "test.json")},
        ),
    ]

  def _generate_examples(self, path=None):
    """Yields examples."""
    # TODO(VLSP): Yields (key, example) tuples from the dataset
    with tf.io.gfile.GFile(path) as f:
      for line in f:
        # Possible keys are:
        # "article_id": str
        # _DOCUMENT: list[str] article (list of paragraphs).
        # _SUMMARY: list[str], abstract (list of paragraphs).
        # "meta_data": list[str], list of section names.
        # "sections": list[list[str]], list of sections (list of paragraphs)
        d = json.loads(line)
        summary = "\n".join(d[_SUMMARY])
        # In original paper, <S> and </S> are not used in vocab during training or during decoding.
        # https://github.com/armancohan/long-summarization/blob/master/data.py#L27
        summary = summary.replace("<S>", "").replace("</S>", "")
        yield d["article_id"], {
            _DOCUMENT: "\n".join(d[_DOCUMENT]),
            _SUMMARY: summary,
            "meta_data": "\n".join(d["meta_data"])
        }

