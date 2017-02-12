import wx
from collections import Counter
import operator

class EntryPad(wx.Panel):

	def __init__(self, parent, sourceboard, log):
		wx.Panel.__init__(self, parent, size=wx.Size(log.GetSize()[0],-1))
		self.sourceboard = sourceboard
		self.epSizer = wx.GridSizer(2,3,20,5)
		self.SetSizer(self.epSizer)
		self.log = log
		self.font = wx.Font(16, wx.MODERN, wx.NORMAL, wx.NORMAL)
		self.SetFont(self.font)
		self.fontcolor = "White"
		self.max = 6
		self.options = []
		self.refresh()
		

	def refresh(self):
		suggestions_list = [(c.suggest(self.max),c.weight) for c in self.sourceboard.channels]
		suggestions = self.weighted_combine(suggestions_list)
		self.options = suggestions[0:self.max]
		self.epSizer.Clear(True)
		for i in range(len(self.options)):
			word = str(self.options[i])
			button = wx.BoxSizer(wx.HORIZONTAL)
			number_label = wx.StaticText(self, label=str((i+1) % 10), size=wx.Size(30,-1))
			word_label = wx.StaticText(self, label=word, style=wx.ALIGN_LEFT, size= wx.Size(200,-1))
			word_label.SetForegroundColour(self.fontcolor)
			number_label.SetForegroundColour(self.fontcolor)
			button.Add(number_label)
			button.Add(word_label)
			self.log.Unbind(wx.EVT_CHAR_HOOK)
			self.log.Bind(wx.EVT_CHAR_HOOK, lambda event: self.onKey(event))
			self.epSizer.Add(button)
		self.Layout()


	def weighted_combine(self, suggestions_list):
		suggestions = {}
		for x, weight in suggestions_list:
			for word, value in x:
				if word in suggestions:
					suggestions[word] += value * weight
				else:
					suggestions[word] = value * weight
		#suggestions = sum((Counter(dict(x)) for x in suggestions_list),Counter())
		top_suggestions = list(reversed(sorted(suggestions.items(),key=operator.itemgetter(1))))
		return [word for word, score in top_suggestions]

	def onKey(self, event):
		keycode = event.GetKeyCode()
		shift_down = event.ShiftDown()
		command_down = event.CmdDown()
		#print keycode
		if keycode == wx.WXK_LEFT:
			self.log.wordLeft()
			self.refresh()
		elif command_down:
			if keycode == 61:
				self.log.fontPlus()
			if keycode == 45:
				self.log.fontMinus()
			event.DoAllowNextEvent()
		elif keycode == 316:
			self.log.wordRight()
			self.refresh()
		elif keycode > 255:
			event.DoAllowNextEvent()
		elif keycode == wx.WXK_TAB:
			pass
		elif keycode == wx.WXK_RETURN: # enter key
			self.sourceboard.refresh()

		elif keycode == 8: # delete key
			self.log.deleteWord()
			self.refresh()
		elif chr(keycode).isdigit():
			index = int(chr(keycode))
			if shift_down:
				index += 10
			#word = str(self.suggestions[index-1])
			word = str(self.options[index-1])
			self.log.addWord(word, "WHITE")#, self.channel.color)
			self.refresh()
		else:
			event.DoAllowNextEvent()




