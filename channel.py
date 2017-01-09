import wx
from corpus import Corpus
from keyboard import Keyboard
from inspector import Inspector

class Channel(wx.Panel):

	def __init__(self, parent, doc):
		wx.Panel.__init__(self, parent)
		channelSizer = wx.BoxSizer(wx.VERTICAL)
		self.doc = doc
		self.corpus = Corpus(doc)
		suggestions = self.corpus.suggest('we', 10)
		self.log = parent.log

		options = [word for (word, value) in suggestions]
		self.keyboard = Keyboard(self, self.doc.name, options)
		channelSizer.Add(self.keyboard)

	def OnAddWordFromSuggestions(self, event, word, suggestions):
		keycode = event.GetKeyCode()
		if chr(keycode).isdigit():
			index = int(chr(keycode))
		word = suggestions[index]
		self.log.AppendText(word + " ")
		self.refresh()

	def refresh(self):
		context = self.log.GetValue().split()[-1]
		suggestions = self.corpus.suggest(context, 10)
		options = [word for (word, value) in suggestions]
		self.keyboard.Hide()
		self.Layout()
		self.keyboard = Keyboard(self, self.doc.name, options)
		self.Layout()
		

	def OnWordButton(self, event, log):
		text = event.GetEventObject().text
		log.AppendText(text + " ")


	