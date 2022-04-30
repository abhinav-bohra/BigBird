"""VLSP dataset."""

import tensorflow_datasets as tfds

# TODO(VLSP): Markdown description  that will appear on the catalog page.
_DESCRIPTION = """
"""

# TODO(VLSP): BibTeX citation
_CITATION = """
"""


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
            # These are the features of your dataset like images, labels ...
        }),
        # If there's a common (input, target) tuple from the
        # features, specify them here. They'll be used if
        # `as_supervised=True` in `builder.as_dataset`.
        supervised_keys=None,  # e.g. ('image', 'label')
        homepage='https://dataset-homepage/',
        citation=_CITATION,
    )

  def _split_generators(self, dl_manager: tfds.download.DownloadManager):
    """Returns SplitGenerators."""
    # TODO(VLSP): Downloads the data and defines the splits
    # dl_manager is a tfds.download.DownloadManager that can be used to
    # download and extract URLs
    return [
        tfds.core.SplitGenerator(
            name=tfds.Split.TRAIN,
            # These kwargs will be passed to _generate_examples
            gen_kwargs={},
        ),
    ]

  def _generate_examples(self):
    """Yields examples."""
    # TODO(VLSP): Yields (key, example) tuples from the dataset
    yield 'key', {}
