from __future__ import division
__author__ = 'jamiebrew'


# information about a unique string within a corpus
class Ngram(object):

	def __init__(self, string, count=1, reach=0):
		self.string = string
		self.count = count
		self.frequency = -1
		self.count_branches = [{} for _ in range(reach+1)]
		self.frequency_branches = [{} for _ in range(reach+1)]
		self.specificity_score_branches = [{} for _ in range(reach+1)]
	
	def __str__(self):
		return "%s (%s)" % (self.string, str(self.count))

	def __repr__(self):
		return self.string

	def __len__(self):
		return len(self.string)

	def __eq__(self, other):
		return self.__dict__ == other.__dict__