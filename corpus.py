from __future__ import division
from ngram import Ngram
import operator
import string
import re
import math

class Corpus(object):
	def __init__(self, name, text):
		self.name = name
		self.text = text
		self.wordcount = 0
		self.max_reach = 2
		self.tree = {}
		self.build(text)
		
		#self.ccae_weight = .0001
		#self.eat_ccae_filtered('ngram_data/w2_.txt',set(self.tree.keys()))
		#self.eat_ccae_filtered('ngram_data/w3_.txt', set(self.tree.keys()))
		#self.eat_ccae_filtered('ngram_data/w4_.txt', set(self.tree.keys()))
		
		self.wordcount = self.get_wordcount()
		self.baseline_weight = .0001
		self.baseline = self.get_baseline()
		self.memory = {}
	
	"""
	baseline computation step: assign words a small score just for occurring in the dictionary
	"""
	def get_baseline(self):
		baseline = {}
		for key in self.tree:
			if len(key.split())==1:
				baseline[key] = self.baseline_weight * self.tree[key].count
		return baseline
		
	def get_wordcount(self):
		wordcount = 0
		for key in self.tree:
			if len(key.split())==1:
				wordcount += 1
		return wordcount
	
	# returns overall frequency of word w in the corpus
	def overall_frequency(self, w):
		if w in self.tree:
			return self.tree[w].count / self.wordcount
		else:
			return 0

	# given a context, looks forward r words from that ngram and returns the frequency of word w
	def conditional_frequency(self, preceding, r, w):
		entry = self.tree[preceding]
		if w in entry.after[r-1]:
			return entry.after[r-1][w] / entry.count
		else:
			return 0
	
	# given a context, looks forward n words from that ngram and returns the significance score of word w	
	def sigscore(self, preceding, r, w):
		try:
			return self.conditional_frequency(preceding, r, w) / self.overall_frequency(w)
		except ZeroDivisionError:
			return 0

	# increments the score in a dictionary
	def tallyscore(self, ngram, score, tree):
		if ngram in tree:
			tree[ngram] += score
		else:
			tree[ngram] = score

	
	"""
	takes a natural language source text
	"""
	def build(self, source_text):
		source_text = source_text.lower().replace('\xe2\x80\x99',"'") 	# last call gets rid of slanted apostrophe
		sentences = source_text.split('. ')
		
		for s in sentences:
			s = s.strip('\n') \
                        .translate(string.maketrans('', ''), string.punctuation.replace('\'', '')) \
                        .lower()
			self.eat_token_string(s.split())
		return
	
	"""
	s is a string of tokens
	reach is the number of tokens to look back and forward
	max_ngram_size is the largest chunks stored
	"""

	def eat_token_string(self, s, max_reach=2, max_ngram_size=3):
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
							self.tree[ngram].add_after(word, reach, 1)
						except IndexError:
							pass
						
						"""
						# update dictionary to reflect all words occurring before this ngram
						try:
							word = before[-1*(reach)]
							self.tree[ngram].add_before(word, reach, 1)
						except IndexError:
							pass
						"""

	""""
	ALTERNATE ENTRY METHODS
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
		
	"""
	takes an ngram frequency file from the Corpus of Contemporary American English, formatted like so:
	
	count	word1	word2	word3 ...
	"""
	def eat_ccae(self, path):
		database = file(path).readlines()
		for line in database:
			splitline = line.split()
			count = float(splitline[0])
			sequence = " ".join(splitline[1:])
			score = count * self.ccae_weight
			self.enter_sequence(sequence, float(score), self.tree)
	
	# only process data that is in the wordset
	def eat_ccae_filtered(self, path, whitelist):
		database = file(path).readlines()
		for line in database:
			splitline = line.split()
			count = float(splitline[0])
			sequence_set = set(splitline[1:])
			
			if sequence_set < whitelist:
				sequence = " ".join(splitline[1:])
				score = count * self.ccae_weight
				self.enter_sequence(sequence, float(score), self.tree)

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