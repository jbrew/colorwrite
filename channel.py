import wx
from corpus import Corpus
from keyboard import Keyboard
from inspector import Inspector

class Channel(wx.Panel):

	def __init__(self, parent, doc, log):
		wx.Panel.__init__(self, parent)
		self.writer = parent
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(self.sizer)
		self.doc = doc
		self.corpus = Corpus(doc)
		self.log = log
		self.active = False
		
		context = self.log.GetValue().split()[-2:]
		suggestions = self.corpus.suggest(context, 10)
		options = [word for (word, value) in suggestions]
		self.keyboard = Keyboard(self, self.doc.name, options, self.log)
		self.inspector = Inspector(self, doc)
		self.sizer.Add(self.keyboard)
		self.sizer.Add(wx.StaticLine(self, -1, wx.Point(10, 30), wx.Size(200, 30)))
		self.sizer.Add(self.inspector)
		

	def refresh(self):
		context = self.log.before().split()[-2:]
		suggestions = self.corpus.suggest(context, 10)
		options = [word for (word, value) in suggestions]
		self.keyboard.Hide()
		self.keyboard = Keyboard(self, self.doc.name, options, self.log)
		self.sizer.Prepend(self.keyboard)
		if self.active:
			self.keyboard.header.SetBackgroundColour((0,255,0))
		else:
			self.keyboard.header.SetBackgroundColour((0,0,0))
		self.Layout()


	