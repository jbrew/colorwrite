from __future__ import division
__author__ = 'jamiebrew'


# information about a unique string within a corpus
class Ngram(object):

	def __init__(self, string, count=1, reach = 0):
		self.string = string
		self.count = count
		self.after = [{} for _ in range(reach)]
		self.before = [{} for _ in range(reach)]
	
	def add_before(self, token, reach, count):
		target_dict = self.before[reach-1]
		if token in target_dict:
			target_dict[token] += count
		else:
			target_dict[token] = count
			
	def add_after(self, token, reach, count):
		target_dict = self.after[reach-1]	
		if token in target_dict:
			target_dict[token] += count
		else:
			target_dict[token] = count
	
	
	def __str__(self):
		return self.string+"\ncount: "+str(self.count)

	def __repr__(self):
		return self.string

	def __len__(self):
		return len(self.string)

	def __eq__(self, other):
		return self.__dict__ == other.__dict__