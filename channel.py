import wx
from corpus import Corpus
from analyst import Analyst
from keyboard import Keyboard
from inspector import Inspector
import random

class Channel(wx.Panel):

	def __init__(self, parent, doc, log):
		wx.Panel.__init__(self, parent)
		self.writer = parent
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(self.sizer)
		self.doc = doc
		#self.corpus = Corpus(doc)
		self.corpus = Corpus([doc])
		self.log = log
		self.active = False
		
		context = self.log.GetValue().split()[-2:]
		suggestions = self.corpus.suggest(context, 10)
		self.keyboard = Keyboard(self, self.doc.name, suggestions, self.log)
		self.inspector = Inspector(self, doc)
		self.sizer.Add(self.keyboard)
		self.sizer.Add(wx.StaticLine(self, -1, wx.Point(10, 30), wx.Size(200, 30)))
		self.sizer.Add(self.inspector)
		

	def weighted_choice(self, choices):
		total = sum(w for (c, w) in choices)
		r = random.uniform(0, total)
		upto = 0
		for c, w in choices:
			if upto + w >= r:
				return c
			upto += w
		assert False, "Shouldn't get here"

	def refresh(self):
		context = self.log.before().split()[-2:]
		suggestions = self.corpus.suggest(context, 20)
		#print self.weighted_choice(suggestions)
		self.keyboard.Hide()
		self.keyboard = Keyboard(self, self.doc.name, suggestions, self.log)
		self.sizer.Prepend(self.keyboard)
		if self.active:
			self.keyboard.header.SetBackgroundColour((0,255,0))
		else:
			self.keyboard.header.SetBackgroundColour((0,0,0))
		self.Layout()


	