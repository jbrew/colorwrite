from __future__ import division
from ngram import Ngram
import operator
import string
import re
import math
from collections import Counter

class Corpus(object):
	"""
	Takes a document, which has a list of dictionaries of ngram counts by size called NGRAM_COUNTS
	"""

	def __init__(self, document):		
		self.tree = {}
		self.wordcount = 0
		self.eat_document(document)
		#self.build(document.text)
		self.name = document.name
		self.text = document.text


		"""
		for word, ngram in self.tree.items()[1:100]:
			print ngram.string
			for word, count in ngram.after[0].iteritems():
				print "\t%s" % (word + " :" + str(count))
				self.wordcount = self.get_wordcount()
		"""
				
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
	

	def build(self, s, max_reach=2, max_ngram_size=2):
		for ngram_size in range(1, max_ngram_size+1):
			for i in range(len(s)):
				start = i
				end = i + ngram_size
				if start >= 0 and end < len(s)+1:
					before, current, after = s[:start],s[start:end],s[end:]
					
					if len(current) == 1:
						self.wordcount += 1
					
					ngram = " ".join(current)
					
					if ngram in self.tree:
						self.tree[ngram].count += 1
					else:
						self.tree[ngram] = Ngram(ngram, 1, max_reach)
					
					for reach in range(1,max_reach + 1):
					
						# update dictionary to reflect all words occurring after this ngram
						try:
							word = after[reach-1]
							#print 'after "%s" is "%s" with reach %s' % (ngram, word, reach)
							self.tree[ngram].add_after(word, reach, max_reach)
						except IndexError:
							pass

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
			tree[head] = Ngram(head, count, 2)
			
		self.wordcount += count * len(components)
		
		branch = tree[head].after[0]
		if tail in branch:
			branch[tail] += count
		else:
			branch[tail] = count

		if len(head) > 1:
			head = " ".join(components[:-2])
			if head in tree:
				tree[head].count += count
			else:
				tree[head] = Ngram(head, count, 2)

			branch = tree[head].after[0]
			if tail in branch:
				branch[tail] += count
			else:
				branch[tail] = count

	
	def suggest(self, preceding, max_suggestions=20):
		suggestions = {}

		for reach in range(1, 3):
			if reach == 1:
				sequence_list = [preceding[i:] for i in range(len(preceding))]
			else:
				sequence_list = [preceding[i:reach*-1+1] for i in range(len(preceding))]

			for sequence in sequence_list:
				ngram = " ".join(sequence)
				if ngram in self.tree:
					component = self.tree[ngram].after[reach-1]
					suggestions = self.merge_dictionaries([suggestions, component])

		suggestion_list = list(reversed(sorted(suggestions.items(), key=operator.itemgetter(1))))
		return suggestion_list[0:max_suggestions]


	def merge_dictionaries(self, dict_list):
		return sum((Counter(dict(x)) for x in dict_list), Counter())





