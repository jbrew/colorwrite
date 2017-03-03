from __future__ import division
import math
import operator

class Analyst(object):

	def __init__(self, corpus):
		self.corpus = corpus
		self.wordcount = self.get_wordcount()
		self.baseline_weight = .0001
		self.baseline = self.get_baseline()
		self.memory = {}
	
	"""
	baseline computation step: assign words a small score just for occurring in the dictionary
	"""
	def get_baseline(self):
		baseline = {}
		for key in self.corpus.tree:
			if len(key.split())==1:
				baseline[key] = self.baseline_weight * self.corpus.tree[key].count
		return baseline
		
	def get_wordcount(self):
		wordcount = 0
		for key in self.corpus.tree:
			if len(key.split())==1:
				wordcount += 1
		return wordcount
	
	"""
	given a list of words preceding the insertion point and a list of words following it,
	returns a list of top suggestions
	"""
	def suggest(self, preceding, max_suggestions = 50):	
	
		corpus = self.corpus
		
		suggestions = dict(self.baseline)
		
		for reach in range(1, corpus.max_reach+1):
			if reach == 1:
				ngram_list = [preceding[i:] for i in range(len(preceding))]
			else:
				ngram_list = [preceding[i:reach*-1+1] for i in range(len(preceding))]
				
			for ngram in ngram_list:
				ngram_size = len(ngram)
				ngram = " ".join(ngram)
				if ngram in self.corpus.tree:
					for word, count in self.corpus.tree[ngram].after[reach-1].iteritems():
						frequency = self.conditional_frequency(ngram, reach, word)
						score = frequency * 1/math.pow(2,reach) * math.pow(2,ngram_size)
						self.tallyscore(word, score, suggestions)
				else:
					pass
					#print '%s not in follower tree!' % ngram
					
		suggestion_list = list(reversed(sorted(suggestions.items(), key=operator.itemgetter(1))))
		
		# hash this state so next time it's encountered, no calculation needed
		context = (''.join(preceding))
		self.memory[context] = suggestion_list
			
		return suggestion_list[0:max_suggestions]
		
	
	# returns overall frequency of word w in the corpus
	def overall_frequency(self, w):
		if w in self.corpus.tree:
			return self.corpus.tree[w].count / self.wordcount
		else:
			return 0

	# given a context, looks forward r words from that ngram and returns the frequency of word w
	def conditional_frequency(self, preceding, r, w):
		entry = self.corpus.tree[preceding]
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