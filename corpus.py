from __future__ import division
from ngram import Ngram
import itertools
import operator
import string
import re
import math
import six
from collections import Counter


class Corpus(object):
	"""
	Takes a list of documents, each of which has a list of dictionaries of ngram counts by size called NGRAM_COUNTS
	"""
	def __init__(self, documents = []):		
		self.max_ngram_size = 5
		self.trees = [{} for n in range(self.max_ngram_size)] # stores continuations of length 1, 2...n
		self.documents = []
		self.TOTALS = []				# list of totals for each ngram size
		for doc in documents:
			self.add_document(doc)
		self.wt_to_frequency = 1
		self.wt_to_specificity_score = .1
		self.baseline = self.baseline_dict()

	def baseline_dict(self):
		rankings = {}
		for tree in self.trees:
			for key, ngram in six.iteritems(tree):
				if len(key.split()) == 1:
					rankings[key] = ngram.count * .0000000000000001

		top_hundred_list = list(reversed(sorted(rankings.items(), key=operator.itemgetter(1))))[0:100]
		top_hundred_dict = {key: value for key, value in top_hundred_list}
		return top_hundred_dict

	def add_document(self, doc):
		self.max_ngram_size = max(doc.max_ngram_size, self.max_ngram_size)
		self.documents.append(doc)
		for COUNT_DICT in doc.NGRAM_COUNTS:
			for ngram, count in COUNT_DICT.iteritems():
				for tree in self.trees:
					self.add_sequence(ngram, count, tree)

		self.TOTALS = [a + b for a, b in itertools.izip_longest(self.TOTALS,doc.TOTALS,fillvalue=0)]		# merge list of totals by ngram size
		self.baseline = self.baseline_dict()
		self.get_frequencies()


	def add_sequence(self, sequence, count, tree):
		tokens = sequence.split(' ')
		splits = [(tokens[:i], tokens[i:])    for i in range(len(tokens) + 1)]

		for split in splits:
			head, tail = split[0], split[1]
			#print head, tail
			#print len(head), len(tail)

			if len(head) > 0 and len(tail) > 0:
				context = ' '.join(head)
				continuation = ' '.join(tail)
				#print context, '...', continuation
				tree = self.trees[len(head)-1]
				self.increment_tree(context, count, tree, self.max_ngram_size)

				count_branch = tree[context].count_branches[0]
				self.increment_branch(continuation, count, count_branch)

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

	# adds frequency and specificity score information to a fully built count dictionary
	def get_frequencies(self):
		for tree in self.trees:
			for key, ngram in tree.iteritems():
				ngram_length = len(key.split())
				total_of_that_size = self.TOTALS[ngram_length-1]
				frequency = ngram.count / total_of_that_size
				ngram.frequency = frequency
				c_branch = ngram.count_branches[0]
				for key, count in c_branch.iteritems():
						
					# frequencies
					contingent_frequency = count+1/ngram.count # laplace smoothing
					ngram.frequency_branches[0][key] = contingent_frequency

					# specificity scores
					if key in tree:
						overall_frequency = tree[key].frequency
					else:
						overall_frequency = 1

					specificity_score = contingent_frequency/overall_frequency
					ngram.specificity_score_branches[0][key] = specificity_score


	"""
	takes an ngram frequency file formatted like so:
	
	word1 word2 word3 ...	 COUNT
	
	with the words separated by spaces and the count offset by a tab
	"""
	def eat_ngram_data(self, path):
		source_text = file(path).readlines()
		for line in source_text:
			sequence, count = line.split('\t')
			for tree in self.trees:
				self.enter_sequence(sequence, int(count), tree)

	"""
	takes a document with a list of dictionaries of ngram counts, split up by size
	"""
	def eat_document(self, document):
		for ngram_count_dict in document.NGRAM_COUNTS:
				for sequence, count in ngram_count_dict.iteritems():
					for tree in self.trees:
						self.enter_sequence(sequence, int(count), tree)


	# suggest continuations that are n words long
	def suggest_n(self, preceding, num_words, max_suggestions=20):
		
		for ngram_dict in self.doc.NGRAM_COUNTS:
			pass

	
	def suggest(self, preceding, max_suggestions=20):
		frequency_dict = self.assign_weight_to_dictionary(self.frequency_rank(preceding, max_suggestions*2), self.wt_to_frequency)
		specificity_score_dict = self.assign_weight_to_dictionary(self.specificity_score_rank(preceding, max_suggestions*2), self.wt_to_specificity_score)

		suggestions = self.merge_dictionaries([frequency_dict, specificity_score_dict])

		suggestion_list = list(reversed(sorted(suggestions.items(), key=operator.itemgetter(1))))
		#suggestion_list = self.filter_by_length(suggestion_list)
		return suggestion_list[0:max_suggestions]

	def filter_by_length(self, suggestion_list):
		return [s for s in suggestion_list if len(s[0].split(' ')) > 1]

	def count_rank(self, preceding, max_suggestions=20):
		rankings = self.baseline

		sequence_list = [preceding[i:] for i in range(len(preceding))]

		for sequence in sequence_list:
			ngram_size = len(sequence)
			ngram = " ".join(sequence)
			weight = (1 * math.pow(5, ngram_size))

			for i in range(len(self.trees)):
				tree = self.trees[i]
				if ngram in tree:
					component = tree[ngram].count_branches[0]
					new_component = self.assign_weight_to_dictionary(component, weight * math.pow(1000,i))
					rankings = self.merge_dictionaries([rankings, new_component])

		suggestion_list = list(reversed(sorted(rankings.items(), key=operator.itemgetter(1))))
		return suggestion_list[0:max_suggestions]


	def frequency_rank(self, preceding, max_suggestions=20):
		rankings = self.baseline

		sequence_list = [preceding[i:] for i in range(len(preceding))]

		for sequence in sequence_list:
			ngram_size = len(sequence)
			ngram = " ".join(sequence)
			weight = (1 * math.pow(5, ngram_size)) / 10

			for i in range(len(self.trees)):
				tree = self.trees[i]
				if ngram in tree:
					component = tree[ngram].frequency_branches[0]
					new_component = self.assign_weight_to_dictionary(component, weight * math.pow(1000,i))
					rankings = self.merge_dictionaries([rankings, new_component])

		return rankings
		#suggestion_list = list(reversed(sorted(suggestions.items(), key=operator.itemgetter(1))))
		#return suggestion_list[0:max_suggestions]

	# returns a list of words with associated specificity scores
	def specificity_score_rank(self, preceding, max_suggestions=20):
		rankings = self.baseline

		sequence_list = [preceding[i:] for i in range(len(preceding))]

		for sequence in sequence_list:
			ngram_size = len(sequence)
			ngram = " ".join(sequence)
			weight = (1 * math.pow(5, ngram_size))

			for i in range(len(self.trees)):
				tree = self.trees[i]
				if ngram in tree:
					component = tree[ngram].specificity_score_branches[0]
					new_component = self.assign_weight_to_dictionary(component, weight * math.pow(1000,i))
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


