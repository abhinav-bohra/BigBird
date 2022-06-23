import os
import sys
from tqdm import tqdm 

docPath = "/content/Long-Text-Summarization/data/final/exp1/test/ects"
goldPath = "/content/Long-Text-Summarization/data/final/exp1/test/gt_summaries"

for file in tqdm(os.listdir(docPath)):
    inp= f'{docPath}/{file}'
    out = f'/content/Long-Text-Summarization/LexRank/test_results/pred/{file}'
    goldsum = open(f'{goldPath}/{file}').readlines()
    num_of_sent = str(len(goldsum))
    
    command = "sumy lex-rank --length="+num_of_sent+" --format=plaintext --file="+inp+" >>"+out
    os.system(command)