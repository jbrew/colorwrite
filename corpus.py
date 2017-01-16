from __future__ import division
from ngram import Ngram
import operator
import string
import re
import math
from collections import Counter


class Corpus(object):
	"""
	Takes a list of documents, each of which has a list of dictionaries of ngram counts by size called NGRAM_COUNTS
	"""

	def __init__(self, documents = []):		
		self.tree = {}
		self.wordcount = 0
		self.documents = {}
		self.max_ngram_size = 0
		for doc in documents:
			self.add_document(doc)


	def add_document(self, doc):
		self.max_ngram_size = max(doc.max_ngram_size, self.max_ngram_size)
		self.documents[doc.name] = doc
		for COUNT_DICT in doc.NGRAM_COUNTS:
			for ngram, count in COUNT_DICT.iteritems():
				self.add_sequence(ngram, count, self.tree)

	def add_sequence(self, sequence, count, tree):
		tokens = sequence.split(' ')
		#print '\nsequence', tokens
		sequence_length = len(tokens)

		if sequence_length == 1:
			word = sequence
			self.increment_tree(word, count, tree, self.max_ngram_size)
			self.wordcount += 1
		
		elif sequence_length > 1:
			for reach in range(1, self.max_ngram_size):
				endpoint = len(tokens)-reach
				context = " ".join(tokens[:endpoint])
				word = tokens[-1]
				#print "context", context
				if len(context) > 0:
					self.increment_tree(context, count, tree, self.max_ngram_size)
					branch = tree[context].after[reach-1]
					self.increment_branch(word, count, branch)
			
			
			
			"""
			if ngram_size > 1:
				head = " ".join(tokens[:-2])
				self.increment_tree(head, count, tree, self.max_ngram_size)

				branch = tree[head].after[ngram_size-1]
				self.increment_branch(tail, count, branch)
			"""

	def increment_tree(self, ngram, count, tree, max_ngram_size):
		if ngram in tree:
			tree[ngram].count += count
		else:
			tree[ngram] = Ngram(ngram, count, max_ngram_size)


	def increment_branch(self, ngram, count, branch):
		if ngram in branch:
			branch[ngram] += count
		else:
			branch[ngram] = count

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


	def suggest_multiple(self, preceding, num_words, max_suggestions=20):
		
		for ngram_dict in self.doc.NGRAM_COUNTS:
			pass


	
	def suggest(self, preceding, max_suggestions=20):
		suggestions = {}

		# construct the baseline dictionary
		for key, ngram in self.tree.iteritems():
			if len(key.split()) == 1:
				suggestions[key] = ngram.count * .0000000000000001

		for reach in range(1, self.max_ngram_size+1):

			if reach == 1:
				sequence_list = [preceding[i:] for i in range(len(preceding))]
			else:
				sequence_list = [preceding[i:reach*-1+1] for i in range(len(preceding)-1)]

			#print "sequence list", sequence_list
			#print "reach", reach
			#print self.tree

			for sequence in sequence_list:
				ngram_size = len(sequence)
				ngram = " ".join(sequence)
				weight = (1 * math.pow(ngram_size, 10)) / math.pow(reach, 10)
				#print "\n", sequence
				#print "size", ngram_size
				#print "reach", reach
				#print "weight:",weight

				if ngram in self.tree:
					component = self.tree[ngram].after[reach-1]
					new_component = self.weight_dictionary(component, weight)
					suggestions = self.merge_dictionaries([suggestions, new_component])

		suggestion_list = list(reversed(sorted(suggestions.items(), key=operator.itemgetter(1))))
		return suggestion_list[0:max_suggestions]


	def merge_dictionaries(self, dict_list):
		return sum((Counter(dict(x)) for x in dict_list), Counter())

	def weight_dictionary(self, dict, weight):
		new_dict = {}
		for word, score in dict.items():
			newscore = float(score) * weight
			new_dict[word] = newscore
		return new_dict


from document import Document

def best_test():
	d = Document('test', 'it was the best of times', 4)
	c = Corpus()
	c.add_document(d)
	print c.suggest(['it'])
	print '\n'
	print c.suggest(['it', 'was'])
	print '\n'
	print c.suggest(['it','was','the'])
	print '\n'
	print c.max_ngram_size

def ai_test():
	path = 'data/rawtranscripts/ai'
	with open(path) as f:
		text = f.read()[0:8000]
	d = Document('ai', text, 4)
	c = Corpus()
	c.add_document(d)
	print c.suggest(['it'])
	print c.suggest(['we','cannot','see'])


#ai_test()


