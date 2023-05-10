# Long Text Summarization

* ECTSum: A New Benchmark Dataset For Bullet Point Summarization of Long Earnings Call Transcripts  
* The repsitory contains code and dataset to the EMNLP'2021 long paper. 
* Link: [https://aclanthology.org/2022.emnlp-main.748/](https://aclanthology.org/2022.emnlp-main.748/)

## Citation

If you use the code in your paper, please kindly star this repo and cite our paper
'''
@inproceedings{mukherjee-etal-2022-ectsum,
    title = "{ECTS}um: A New Benchmark Dataset For Bullet Point Summarization of Long Earnings Call Transcripts",
    author = "Mukherjee, Rajdeep  and
      Bohra, Abhinav  and
      Banerjee, Akash and Sharma, Soumya and Hegde, Manjunath and Shaikh, Afreen and Shrivastava, Shivani and Dasgupta, Koustuv and
      Ganguly, Niloy and Ghosh, Saptarshi  and Goyal, Pawan",
    booktitle = "Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing",
    month = dec,
    year = "2022",
    address = "Abu Dhabi, United Arab Emirates",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2022.emnlp-main.748",
    pages = "10893--10906",
    abstract = "Despite tremendous progress in automatic summarization, state-of-the-art methods are predominantly trained to excel in summarizing short newswire articles, or documents with strong layout biases such as scientific articles or government reports. Efficient techniques to summarize financial documents, discussing facts and figures, have largely been unexplored, majorly due to the unavailability of suitable datasets. In this work, we present ECTSum, a new dataset with transcripts of earnings calls (ECTs), hosted by publicly traded companies, as documents, and experts-written short telegram-style bullet point summaries derived from corresponding Reuters articles. ECTs are long unstructured documents without any prescribed length limit or format. We benchmark our dataset with state-of-the-art summarization methods across various metrics evaluating the content quality and factual consistency of the generated summaries. Finally, we present a simple yet effective approach, ECT-BPS, to generate a set of bullet points that precisely capture the important facts discussed in the calls.",
}
'''

Baselines for Long Text Summarization
  - BigBird
  - LongFormer
  - SummaRuNNer
  - MatchSum
  - PreSumm (BertSumExt)
  - PacSum
  - DSDR
  - LexRank
