import os
import re
import rouge
from collections import Counter
from nltk import ngrams

alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|Mt)[.]"
suffixes = "(Jr|Sr|Assn|Assoc|Co|Comp|Corp|Inc|Intl|LLC|LLP|Ltd|Mfg|PLC|PLLC)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov|me|edu)"
digits = "([0-9])"


pattern1 = "(?<![.,\d])\d+(?:([.,])\d+(?:\1\d+)*)?(?:((?!\1)[.,])\d+)(?![,.\d])" # financial numeric values
pattern2 = "[-+]?(\d+([.,]\d*)?|[.,]\d+)([eE][-+]?\d+)?" # international_float
pattern3 = "[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?" # numeric_const_pattern
neg_pattern = "^(?:(?![A-Za-z](?=\d)).)*$" # avoid matching numbers followed by text, for e.g. q2

pattern4 = "[A-Za-z]\d+" # search for text followed by numbers, for e.g. q2
pattern5 = "\d+[A-Za-z]" # search for numbers followed by text, for e.g. 10q"
fiscal_year = "\'\d+" # Shorthand representation of fiscal years
pattern6 = "(?<![A-Za-z])\d+\.\d+|(?<![A-Za-z])\d+"

phone1 = "(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}"
phone2 = "\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*"
time1 = "\d{1,2}:\d{2}"
time2 = "\d{1,2}:\d{2}:\d{2}"


def split_into_sentences(text):
	text = " " + text + "  "
	text = text.replace("\n"," ")
	text = re.sub(prefixes,"\\1<prd>",text)
	text = re.sub(prefixes.upper(),"\\1<prd>",text)
	text = re.sub(websites,"<prd>\\1",text)
	text = re.sub(websites.upper(),"<prd>\\1",text)
	text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
	if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
	if "e.g." in text: text = text.replace("e.g.","e<prd>g<prd>")
	if "i.e." in text: text = text.replace("i.e.","i<prd>e<prd>")
	if "..." in text: text = text.replace("...","<prd><prd><prd>")
	text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
	text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
	text = re.sub(acronyms+" "+starters.upper(),"\\1<stop> \\2",text)
	text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
	text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
	text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
	text = re.sub(" "+suffixes.upper()+"[.] "+starters.upper()," \\1<stop> \\2",text)
	text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
	text = re.sub(" "+suffixes.upper()+"[.]"," \\1<prd>",text)
	text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
	if "”" in text: text = text.replace(".”","”.")
	if "\"" in text: text = text.replace(".\"","\".")
	if "!" in text: text = text.replace("!\"","\"!")
	if "?" in text: text = text.replace("?\"","\"?")
	text = text.replace(".",".<stop>")
	text = text.replace("?","?<stop>")
	text = text.replace("!","!<stop>")
	text = text.replace("<prd>",".")
	sentences = text.split("<stop>")
	sentences = sentences[:-1]
	sentences = [s.strip() for s in sentences]
	return sentences


def get_DocLines(fname):
	exclude_list = ["hello", "thank", "welcome", "morning", "afternoon", "all the best", "acknowledge", "this call", "webcast",
	"presentation", "replay of the call", "replay will be available", "with me are", "with us today", "with me today", 
	"joining me today", "our speakers today", "today's comments", "on today's call", "opening remarks", "prepared remarks", 
	"opening comments today", "forward-looking", "like to remind you", "turn to slide", "please refer to", "please look at", 
	"use of the words", "subject to risks", "see the risk factors", "further caution", "you are cautioned", "cautionary language", 
	"assumes no obligation", "undertake any obligation", "provide no assurance", "unless otherwise noted", "press release", 
	"earnings release", "guidance is based on", "our corporate website", "represent our current judgment", "introduce the members", 
	"like to introduce", "members of senior management", "management may reference", "accordance with reg g requirements", 
	"hearts go out to those affected", "turn the call", "for questions", "your questions", "please go ahead", "limit your questions", 
	"turn it back", "turn it over",  "open the floor", "posted to our", "cause actual results", "statements are predictions", 
	"sec's website"]
	all_sent = []
	f_in = open(fname, 'r')
	all_sent = f_in.readlines()
	all_sent = [line.strip() for line in all_sent if not (line.strip() == '' or line.startswith('Speaker'))]
	all_sent = [line for line in all_sent if not (re.search(phone1, line) or re.search(phone2, line))]
	all_sent = [line.replace('EPS', 'earnings per share') for line in all_sent]
	all_sent = [line for line in all_sent if len(line.split()) > 3]
	all_sent = [line for line in all_sent if len([phrase for phrase in exclude_list if phrase in line.lower()]) == 0]
	f_in.close()
	return all_sent


def get_SummLines(fname):
	f_in = open(fname, 'r')
	lines = f_in.readlines()
	lines = [line.strip() for line in lines if line.strip() != '']
	lines = [re.sub(r'\s\s+', r' ', line) for line in lines]
	f_in.close()
	return lines


def getProcessedLines(lines):
	covid = ['Covid-19', 'Covid 19', "Covid'19"]
	months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'September', 'October', 'November', 'December']
	months_short = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Sep', 'Sept', 'Oct', 'Nov', 'Dec']
	years = [f'20{year}' for year in range(10, 25)]
	processed_lines = []
	for line in lines:
		text = line.strip()
		for match in covid:
			text = text.replace(match, 'Covid')
			text = text.replace(match.lower(), 'covid')
			text = text.replace(match.upper(), 'COVID')
		for match in re.findall(phone1, text):
			text = text.replace(match, '[PHONENUM]')
		for match in re.findall(phone2, text):
			text = text.replace(match, '[PHONENUM]')
		for match in re.findall(pattern4, text):
			text = text.replace(match, '[TXT-NUM]')
		for match in re.findall(pattern5, text):
			text = text.replace(match, '[NUM-TXT]')
		for match in re.findall(fiscal_year, text):
			# text = text.replace(match, f' 20{match[1:]}')
			text = text.replace(match, ' [YEAR]')
		for short_year in range(10, 25):
			text = text.replace(f'fy{short_year}', f'financial year [YEAR]')
			text = text.replace(f'FY{short_year}', f'financial year [YEAR]')
			text = text.replace(f'Fy{short_year}', f'financial year [YEAR]')
		for match in re.findall(time1, text):
			text = text.replace(match, '[TIME] ')
		for match in re.findall(time2, text):
			text = text.replace(match, '[TIME] ')
		text = re.sub(r'\s\s+', r' ', text)
		text = text.replace('[TIME] a.m.', '[TIME]')
		text = text.replace('[TIME] A.M.', '[TIME]')
		text = text.replace('[TIME] p.m.', '[TIME]')
		text = text.replace('[TIME] P.M.', '[TIME]')
		if re.search(pattern6, text):
			for match in re.findall(pattern6, text):
				if match in years:
					text = text.replace(match, '[YEAR]')
			if re.search(pattern6, text):
				for match in re.findall(pattern6, text):
					text = text.replace(match, '[NUM]')
				for month in months:
					text = text.replace(f'{month} [NUM]', '[DATE]')
					text = text.replace(f'{month.lower()} [NUM]', '[DATE]')
					text = text.replace(f'{month.upper()} [NUM]', '[DATE]')
				for month in months_short:
					text = text.replace(f'{month} [NUM]', '[DATE]')
					text = text.replace(f'{month.lower()} [NUM]', '[DATE]')
					text = text.replace(f'{month.upper()} [NUM]', '[DATE]')
		processed_lines.append(text)
	
	return processed_lines


def getPartiallyProcessedText(line):
	covid = ['Covid-19', 'Covid 19', "Covid'19"]
	months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'September', 'October', 'November', 'December']
	months_short = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Sep', 'Sept', 'Oct', 'Nov', 'Dec']	
	years = [f'20{year}' for year in range(10, 25)]	
	text = line.strip()
	for match in covid:
		text = text.replace(match, 'Covid')
		text = text.replace(match.lower(), 'covid')
		text = text.replace(match.upper(), 'COVID')
	for match in re.findall(phone1, text):
		text = text.replace(match, '[PHONENUM]')
	for match in re.findall(phone2, text):
		text = text.replace(match, '[PHONENUM]')
	for match in re.findall(pattern4, text):
		text = text.replace(match, '[TXT-NUM]')
	for match in re.findall(pattern5, text):
		text = text.replace(match, '[NUM-TXT]')
	for match in re.findall(fiscal_year, text):
		# text = text.replace(match, f' 20{match[1:]}')
		text = text.replace(match, ' [YEAR]')
	for short_year in range(10, 25):
		text = text.replace(f'fy{short_year}', f'financial year [YEAR]')
		text = text.replace(f'FY{short_year}', f'financial year [YEAR]')
		text = text.replace(f'Fy{short_year}', f'financial year [YEAR]')
	for match in re.findall(time1, text):
		text = text.replace(match, '[TIME] ')
	for match in re.findall(time2, text):
		text = text.replace(match, '[TIME] ')
	text = re.sub(r'\s\s+', r' ', text)
	text = text.replace('[TIME] a.m.', '[TIME]')
	text = text.replace('[TIME] A.M.', '[TIME]')
	text = text.replace('[TIME] p.m.', '[TIME]')
	text = text.replace('[TIME] P.M.', '[TIME]')
	for match in re.findall(pattern6, text):
		if match in years:
			text = text.replace(match, '[YEAR]')
		for month in months:
			text = text.replace(f'{month} {match}', '[DATE]')
			text = text.replace(f'{month.lower()} {match}', '[DATE]')
			text = text.replace(f'{month.upper()} {match}', '[DATE]')
		for month in months_short:
			text = text.replace(f'{month} {match}', '[DATE]')
			text = text.replace(f'{month.lower()} {match}', '[DATE]')
			text = text.replace(f'{month.upper()} {match}', '[DATE]')						
	return text


def prepare_results(metric, p, r, f):
	return '\t{}:\t{}: {:5.2f}\t{}: {:5.2f}\t{}: {:5.2f}'.format(metric, 'P', 100.0 * p, 'R', 100.0 * r, 'F1', 100.0 * f)


def getRouge(pred_summary, gt_summary, f_out):
	f_out.write('\n\n\nSummary Evaluation\n\n')
	# for aggregator in ['Avg', 'Best', 'Individual']:
	metric_scores = {}
	for aggregator in ['Avg']:
		f_out.write('Evaluation with {}'.format(aggregator) + '\n')
		apply_avg = aggregator == 'Avg'
		apply_best = aggregator == 'Best'

		evaluator = rouge.Rouge(metrics=['rouge-n', 'rouge-l'],
							   max_n=2,
							   # limit_length=True,
							   # length_limit=100,
							   length_limit_type='words',
							   apply_avg=apply_avg,
							   apply_best=apply_best,
							   alpha=0.5, # Default F1_score
							   weight_factor=1.2,
							   stemming=True)

		all_hypothesis = [pred_summary]
		all_references = [gt_summary]

		scores = evaluator.get_scores(all_hypothesis, all_references)
		
		for metric, results in sorted(scores.items(), key=lambda x: x[0]):
			if not apply_avg and not apply_best: # value is a type of list as we evaluate each summary vs each reference
				for hypothesis_id, results_per_ref in enumerate(results):
					nb_references = len(results_per_ref['p'])
					for reference_id in range(nb_references):
						f_out.write('\tHypothesis #{} & Reference #{}: '.format(hypothesis_id, reference_id) + '\n')
						f_out.write('\t' + prepare_results(metric, results_per_ref['p'][reference_id], results_per_ref['r'][reference_id], results_per_ref['f'][reference_id]))
				f_out.write('\n')
			else:
				f_out.write(prepare_results(metric, results['p'], results['r'], results['f']))
				f_out.write('\n\n')
				metric_scores[metric] = [results['p'], results['r'], results['f']]
		print()

	return metric_scores
