from __future__ import division
from __future__ import print_function
import os
import math
import operator
from document import Document
from collections import Counter

class Librarian(object):
	def __init__(self, path, max_ngram_size):
		self.max_ngram_size = max_ngram_size
		transcripts = os.listdir(path)[1:10] # ignores DS_store, the first file in the directory
		self.docs = [self.make_doc(filename) for filename in transcripts] 
	
	def make_doc(self, filename):
		path = 'data/rawtranscripts/%s' % filename
		with open(path, 'r') as f:
			text = f.read()
			d = Document(filename, text,self.max_ngram_size)
			return d
	
	def idf(self, term):
		return math.log(len(self.docs)/len(self.search_docs(term)))	

	def tf_idf(self, term, doc):
		return doc.tf(term) * self.idf(term)
	
	def search_docs(self, term):
		num_words = len(term.split())
		hits = [doc for doc in self.docs if term in doc.NGRAM_COUNTS[num_words-1]]
		return hits
	
	def key_ngrams(self, doc, ngram_size, rank_depth):
		scores = {}
		for term in doc.NGRAM_COUNTS[ngram_size-1].keys():
			scores[term] = l.tf_idf(term, doc)
		return list(reversed(sorted(scores.items(), key = operator.itemgetter(1))))[0:rank_depth]

	def full_tfidf_analysis(self):
		for doc in self.docs:
			for n in range(1,self.max_ngram_size+1):
				key_terms = self.key_ngrams(doc,n,500)
				path = 'data/%s__%sgrams' % (doc.name, n)
				with open(path, 'w') as f:
					print(key_terms, file=f)

	def merge_dictionary_list(self, dict_list):
		return sum((Counter(dict(x)) for x in dict_list), Counter())

	def full_count_analysis(self, ngram_size, doc_threshold, overall_threshold):
		for doc in self.docs:
			for dict in doc.NGRAM_COUNTS:
				dict = {k:v for k, v in dict.items() if v > doc_threshold} # prunes each dictionary

		counts = self.merge_dictionary_list([doc.NGRAM_COUNTS[ngram_size-1] for doc in self.docs])
		counts = {k:v for k, v in counts.items() if v > overall_threshold} 
		counts = list(reversed(sorted(counts.items(), key = operator.itemgetter(1))))
		path = '%sgram__counts' % ngram_size
		with open(path,'w') as f:
			for word, count in counts:
				line = '%s\t%s' % (word, count)
				print(line, file=f)



	def investigate(self, word, doc):
		print('\n')
		print (word)
		print ('idf: %s' % self.idf(word))
		print ('tf in %s: %s' % (doc.name, doc.tf(word)))
		print ('tf idf: %s' % self.tf_idf(word, doc))
	


"""
for d in l.docs:
	print d.term_frequency('well')


print l.idf('the')
print l.idf('so')
print l.idf('expel')

l.investigate('asked', l.docs[10])
l.investigate('working', l.docs[10])

"""
#a = {'A': 1, 'B': 5}
#b = {'B': 6, 'C': 100}
#print (l.merge_dictionary_list([a, b]))




#l = Librarian('transcripts',4)
#l.full_tfidf_analysis()
#l.full_count_analysis(1, 1, 50)
#l.full_count_analysis(2, 1, 20)
#l.full_count_analysis(3, 1, 15)
#l.full_count_analysis(4, 1, 10)
	

#	key_terms = l.key_ngrams(l.docs[i]2,500)
#	path = 'data/%s_2grams' % doc.name
#	with open(path, 'w') as f:
#		print(key_terms, file=f)
	
	