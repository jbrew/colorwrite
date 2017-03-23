from __future__ import division
import os
import re
import math
import string
import operator
from collections import Counter

class Document(object):
	def __init__(self, name, text, max_ngram_size=4):
		self.name = self.simple_name(name)
		self.text = text
		self.max_ngram_size = max_ngram_size
		self.NGRAM_COUNTS = self.ngram_counts(text)
		self.TOTALS = self.totals(self.NGRAM_COUNTS)
	
	# removes file extension from source's display name
	def simple_name(self, name):
		if name.split('.')[-1] == 'txt':
			name = '.'.join(name.split('.')[:-1])
		return name

	# given a term one or more words, return how many times it occurs in this document
	def term_count(self, term):
		num_words = len(term.split())
		if num_words > 0 and term in self.NGRAM_COUNTS[num_words-1]:
			return self.NGRAM_COUNTS[num_words-1][term]
		else:
			return 0

	def ngram_counts(self, text):
		lines = text.split('\n')
		if len(lines[0].split('\t')) == 2:	# true if this is a tab delimited file of the form [ngram TAB count]
			return self.ngram_counts_from_data(lines, self.max_ngram_size)
		else:
			return self.ngram_counts_from_text(text, self.max_ngram_size)

	# gets ngram count data from a tab delimited file associating ngrams with counts
	def ngram_counts_from_data(self, lines, max_ngram_size):
		counters = [{} for _ in range(max_ngram_size)]
		for line in lines:
			if len(line.split('\t')) == 2:
				ngram, count = line.split('\t')
				ngram_size = len(ngram.split(' '))
				if not ngram in counters[ngram_size - 1]:
					counters[ngram_size - 1][ngram] = float(count)
				else:
					counters[ngram_size - 1][ngram] += float(count)
		return counters

	# gets ngram count data from a raw text file
	def ngram_counts_from_text(self, text, max_ngram_size):
		counters = []
		word_re = "'?\w[\w']*(?:-\w+)*'?"
		space_re = "\s"
		for ngram_size in range(1, max_ngram_size+1):
			regex_string = word_re + (space_re+word_re) *(ngram_size-1)
			full_expression = "(?=(%s))(?<!\w)" % regex_string
			newcounter = Counter(re.findall(full_expression, text.lower().replace(".","").replace("\n"," ").replace("'","")))
			cleancounter = {key: val for key, val in newcounter.iteritems()} # stopgap that can perform adhoc replacements of stubborn apostrophe words
			counters.append(cleancounter)


		return counters	

	# splits the text into sentences, lowercases them and cleans punctuation
	def make_sentences(self, str):
		# split at period followed by newline or space, or question mark, or exclamation point
		sentences = str.split('.\n' or '. ' or '?' or '!')

		for sentence in range (0,len(sentences)):
			sentences[sentence] = sentences[sentence].strip('\n')
			sentences[sentence] = sentences[sentence].translate(string.maketrans("",""), string.punctuation.replace("'","")) # removes all punctuation except apostrophe
			sentences[sentence] = sentences[sentence].lower()
		return sentences

	# returns all the text that occurs in quotes
	def inside_quotes(self):
		paragraphs = self.text.split('\n')
		snowball = ''
		for p in paragraphs:
			in_quotes = " ".join(re.findall('"([^"]*)"', p))
			snowball += "\n " + in_quotes
		return snowball

	# returns all the text that occurs outside quotes
	def outside_quotes(self):
		paragraphs = self.text.split('\n')
		snowball = ''
		for p in paragraphs:
			out_of_quotes = re.sub('"([^"]*)"','', p)
			snowball += "\n " + out_of_quotes

		return snowball
	# for each dictionary of ngrams, returns the total number of ngrams of that size in this document
	def totals(self, ngram_counts):
		totals = []
		for c in ngram_counts:
			total = sum([val for val in c.values()])
			totals.append(total)
		return totals

	# returns the dictionary of ngrams of the specified size, mapped to counts
	def get_ngrams(self, n):
		return self.NGRAM_COUNTS[n-1]

	# term frequency
	def tf(self, term):
		num_words = len(term.split())
		return self.NGRAM_COUNTS[num_words-1][term] / self.TOTALS[num_words-1]

	# sigscore given a baseline frequency
	def sigscore(self, term, baseline):
		frequency = self.tf(term)
		expected_frequency = baseline
		return frequency / expected_frequency

"""
path = 'texts/ncaa_recaps'
with open(path, 'r') as f:
	text = f.read()

d = Document('ncaa', text, 2)
print d.outside_quotes()
"""		