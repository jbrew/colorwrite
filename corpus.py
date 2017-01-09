from __future__ import division
from ngram import Ngram
import operator
import string
import re
import math

class Corpus(object):
	"""
	Takes a document, which has a list of dictionaries of ngram counts by size called NGRAM_COUNTS
	"""

	def __init__(self, document):		
		self.tree = {}
		self.wordcount = 0
		self.eat_document(document)
		self.name = document.name
		self.text = document.text
		


				
	"""
	takes an ngram frequency file formatted like so:
	
	word1 word2 word3 ...	 COUNT
	
	with the words separated by spaces and the count offset by a tab
	"""
	def eat_ngram_data(self, path):
		source_text = file(path).readlines()
		for line in source_text:
			sequence, count = line.split('\t')
			self.enter_sequence(sequence, int(count), self.tree)
	
	"""
	takes a document with a list of dictionaries of ngram counts, split up by size
	"""
	def eat_document(self, document):
		for ngram_count_dict in document.NGRAM_COUNTS:
				for sequence, count in ngram_count_dict.iteritems():
					self.enter_sequence(sequence, count, self.tree)

	# enters this ngram in the tree
	def enter_sequence(self, ngram, count, tree):
		components = ngram.split(' ')
		head = " ".join(components[:-1])
		tail = components[-1]
		
		if head in tree:
			tree[head].count += count
		else:
			tree[head] = Ngram(ngram, count, 1)
			
		self.wordcount += count * len(components)
		
		branch = tree[head].after[0]
		if tail in branch:
			branch[tail] += count
		else:
			branch[tail] = count

	def suggest(self, preceding, max_suggestions=20):
		if preceding in self.tree:
			suggestions = self.tree[preceding].after[0]
			suggestion_list = list(reversed(sorted(suggestions.items(), key=operator.itemgetter(1))))
			return suggestion_list[0:max_suggestions]
		else:
			return []



