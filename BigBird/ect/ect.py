import json
import os
import tensorflow as tf
import tensorflow_datasets.public_api as tfds

_DOCUMENT = "document"
_SUMMARY = "summary"

class EctConfig(tfds.core.BuilderConfig):
  """BuilderConfig for Ect Dataset."""

  def __init__(self, *, filename=None, **kwargs):
    super(EctConfig, self).__init__(
        version=tfds.core.Version("1.1.1"),
        supported_versions=[tfds.core.Version("1.1.0")],
        **kwargs)  # pytype: disable=wrong-arg-types  # gen-stub-imports
    self.filename = filename


class Ect(tfds.core.GeneratorBasedBuilder):
  """Ect Dataset."""

  BUILDER_CONFIGS = [ EctConfig(name="ect", description="ECT Dataset") ]
  def _info(self):
    return tfds.core.DatasetInfo(
        builder=self,
        features=tfds.features.FeaturesDict({
            _DOCUMENT: tfds.features.Text(),
            _SUMMARY: tfds.features.Text(),
        }),
        supervised_keys=(_DOCUMENT, _SUMMARY)
    )

  def _split_generators(self, dl_manager):
    """Returns SplitGenerators."""
    data_dir = "/content/Long-Text-Summarization/BigBird/ect/"
    return [
        tfds.core.SplitGenerator(
            name=tfds.Split.TRAIN,
            gen_kwargs={"path": os.path.join(data_dir, "train.txt")},
        ),
        tfds.core.SplitGenerator(
            name=tfds.Split.VALIDATION,
            gen_kwargs={"path": os.path.join(data_dir, "val.txt")},
        ),
        tfds.core.SplitGenerator(
            name=tfds.Split.TEST,
            gen_kwargs={"path": os.path.join(data_dir, "test.txt")},
        ),
    ]

  def _generate_examples(self, path=None):
    """Yields examples."""
    with tf.io.gfile.GFile(path) as f:
      for line in f:
        d = json.loads(line)
        doc = "\n".join(d["document"])
        summ = "\n".join(d["summary"])
        summ = summ.replace("<S>", "").replace("</S>", "")
        yield d["doc_id"],{
            _DOCUMENT: doc,
            _SUMMARY: summ
        }