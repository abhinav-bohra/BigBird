import os, json

def preprocessSummaries(s_):
    s = []
    for line in s_:
        if line.startswith("Speaker ::") or line=="\n":
            continue
        else:
            line = line.replace('\n',"").replace("  "," ")
            line = "<S> " + str(line) + " </S>"
            s.append(line)
    return s

splits = ["train", "test", "val"] 
for split in splits:
  path_articles = f"/content/Long-Text-Summarization/data/final/exp1/{split}/ects" 
  path_summaries = f"/content/Long-Text-Summarization/data/final/exp1/{split}/gt_summaries"
  outfile = f"/content/Long-Text-Summarization/BigBird/ect/{split}.txt"
  articles = os.listdir(path_articles)
  summaries = os.listdir(path_summaries)
  assert (len(articles) == len(summaries))
  
  data = []
  for article in articles:
    data_point = {}
    a = open(os.path.join(path_articles, article), 'r').readlines()
    s = preprocessSummaries( open(os.path.join(path_summaries, article), 'r').readlines() )
    data_point["doc_id"] = article
    data_point["document"] = a
    data_point["summary"] = s
    data_str = json.dumps(data_point)
    data.append(data_str)
    
  with open(outfile, mode='wt', encoding='utf-8') as myfile:
    myfile.write('\n'.join(data))
    print(f"{split} done {len(data)}")
  myfile.close()

  if split=="test":
    test_files = {}
    cnt=0
    for art in articles:
        cnt=cnt+1
        test_files[cnt] = art

    with open(f"/content/Long-Text-Summarization/BigBird/test_files.json", "w") as f:
        json.dump(test_files, f)
        print("Saving test file names")
