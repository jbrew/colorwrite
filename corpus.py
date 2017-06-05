from __future__ import division
from ngram import Ngram
import itertools
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
		self.documents = []
		self.max_ngram_size = 0
		self.TOTALS = []				# list of totals for each ngram size
		for doc in documents:
			self.add_document(doc)
		self.wt_to_frequency = 1
		self.wt_to_sigscore = .00000001

	def add_document(self, doc):
		self.max_ngram_size = max(doc.max_ngram_size, self.max_ngram_size)
		self.documents.append(doc)
		for COUNT_DICT in doc.NGRAM_COUNTS:
			for ngram, count in COUNT_DICT.iteritems():
				self.add_sequence(ngram, count, self.tree)
		self.TOTALS = [a + b for a, b in itertools.izip_longest(self.TOTALS,doc.TOTALS,fillvalue=0)]		# merge list of totals by ngram size
		print 'totals', doc.TOTALS
		self.get_frequencies()
		

	def add_sequence(self, sequence, count, tree):
		tokens = sequence.split(' ')
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
				if len(context) > 0:
					self.increment_tree(context, count, tree, self.max_ngram_size)

					count_branch = tree[context].count_branches[reach-1]
					self.increment_branch(word, count, count_branch)

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

	# adds frequency and significance score information to a fully built count dictionary
	def get_frequencies(self):
		for key, ngram in self.tree.iteritems():
			ngram_length = len(key.split())
			total_of_that_size = self.TOTALS[ngram_length-1]
			frequency = ngram.count / total_of_that_size
			ngram.frequency = frequency
			for reach in range(len(ngram.count_branches)):
				c_branch = ngram.count_branches[reach]
				for key, count in c_branch.iteritems():
					
					# frequencies
					contingent_frequency = count/ngram.count
					ngram.frequency_branches[reach][key] = contingent_frequency

					# significance scores
					overall_frequency = self.tree[key].frequency
					significance_score = contingent_frequency/overall_frequency
					#print key, overall_frequency, contingent_frequency, significance_score
					ngram.sigscore_branches[reach][key] = significance_score





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


	def suggest_n(self, preceding, num_words, max_suggestions=20):
		
		for ngram_dict in self.doc.NGRAM_COUNTS:
			pass

	
	def suggest(self, preceding, max_suggestions=20):
		frequency_dict = self.assign_weight_to_dictionary(self.frequency_rank(preceding, max_suggestions*2), self.wt_to_frequency)
		sigscore_dict = self.assign_weight_to_dictionary(self.sigscore_rank(preceding, max_suggestions*2), self.wt_to_sigscore)

		suggestions = self.merge_dictionaries([frequency_dict, sigscore_dict])

		suggestion_list = list(reversed(sorted(suggestions.items(), key=operator.itemgetter(1))))
		return suggestion_list[0:max_suggestions]

	def count_rank(self, preceding, max_suggestions=20):
		rankings = {}

		# construct the baseline dictionary
		for key, ngram in self.tree.iteritems():
			if len(key.split()) == 1:
				rankings[key] = ngram.count * .0000000000000001

		for reach in range(1, self.max_ngram_size+1):

			if reach == 1:
				sequence_list = [preceding[i:] for i in range(len(preceding))]
			else:
				sequence_list = [preceding[i:reach*-1+1] for i in range(len(preceding)-1)]

			for sequence in sequence_list:
				ngram_size = len(sequence)
				ngram = " ".join(sequence)
				weight = (1 * math.pow(5, ngram_size)) / math.pow(10, reach)

				if ngram in self.tree:
					component = self.tree[ngram].count_branches[reach-1]
					new_component = self.assign_weight_to_dictionary(component, weight)
					rankings = self.merge_dictionaries([rankings, new_component])

		suggestion_list = list(reversed(sorted(rankings.items(), key=operator.itemgetter(1))))
		return suggestion_list[0:max_suggestions]


	def frequency_rank(self, preceding, max_suggestions=20):
		rankings = {}

		# construct the baseline dictionary
		for key, ngram in self.tree.iteritems():
			if len(key.split()) == 1:
				rankings[key] = ngram.count * .0000000000000001

		for reach in range(1, self.max_ngram_size+1):

			if reach == 1:
				sequence_list = [preceding[i:] for i in range(len(preceding))]
			else:
				sequence_list = [preceding[i:reach*-1+1] for i in range(len(preceding)-1)]

			for sequence in sequence_list:
				ngram_size = len(sequence)
				ngram = " ".join(sequence)
				weight = (1 * math.pow(5, ngram_size)) / math.pow(10, reach)

				if ngram in self.tree:
					component = self.tree[ngram].frequency_branches[reach-1]
					new_component = self.assign_weight_to_dictionary(component, weight)
					rankings = self.merge_dictionaries([rankings, new_component])

		return rankings
		#suggestion_list = list(reversed(sorted(suggestions.items(), key=operator.itemgetter(1))))
		#return suggestion_list[0:max_suggestions]

	# returns a list of words with associated significance scores
	def sigscore_rank(self, preceding, max_suggestions=20):
		rankings = {}

		# construct the baseline dictionary
		for key, ngram in self.tree.iteritems():
			if len(key.split()) == 1:
				rankings[key] = ngram.count * .0000000000000001

		for reach in range(1, self.max_ngram_size+1):

			if reach == 1:
				sequence_list = [preceding[i:] for i in range(len(preceding))]
			else:
				sequence_list = [preceding[i:reach*-1+1] for i in range(len(preceding)-1)]

			for sequence in sequence_list:
				ngram_size = len(sequence)
				ngram = " ".join(sequence)
				weight = (1 * math.pow(5, ngram_size)) / math.pow(10, reach)

				if ngram in self.tree:
					component = self.tree[ngram].sigscore_branches[reach-1]
					new_component = self.assign_weight_to_dictionary(component, weight)
					rankings = self.merge_dictionaries([rankings, new_component])

		return rankings
		#suggestion_list = list(reversed(sorted(rankings.items(), key=operator.itemgetter(1))))
		#return suggestion_list[0:max_suggestions]

	# given a list of ngram dictionaries, adds together the counts for shared entries
	def merge_dictionaries(self, dict_list):
		return sum((Counter(dict(x)) for x in dict_list), Counter())

	# returns a new dictionary derived by multiplying each entry's score by a given weight
	def assign_weight_to_dictionary(self, dict, weight):
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


