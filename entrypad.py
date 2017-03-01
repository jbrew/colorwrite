from __future__ import division
import wx
from collections import Counter
import operator
from wordbutton import WordButton

class EntryPad(wx.Panel):

	def __init__(self, parent, sourceboard, log):
		self.width = log.GetSize()[0]
		wx.Panel.__init__(self, parent, size=wx.Size(self.width,-1))
		self.sourceboard = sourceboard
		self.columns = 3
		self.rows = 0
		self.epSizer = wx.GridSizer(self.rows,self.columns,5,5)
		self.SetSizer(self.epSizer)
		self.log = log
		self.font = wx.Font(16, wx.MODERN, wx.NORMAL, wx.NORMAL)
		self.SetFont(self.font)
		self.fontcolor = "White"
		self.max = 9
		self.active_row = 1
		self.active_column = 1
		self.options = []
		self.refresh()
		

	def refresh(self):
		suggestions_list = [(c.suggest(self.max),c.weight) for c in self.sourceboard.channels]
		suggestions = self.weighted_combine(suggestions_list)
		words = [word for word, score in suggestions]
		scores = [score for word, score in suggestions]
		if len(scores) > 0:
			colors = self.scores_to_colors(scores)
		self.options = words[0:self.max]
		self.epSizer.Clear(True)
		for i in range(len(self.options)):
			word = str(self.options[i])
			#print word, scores[i], colors[i]
			
			column_width = self.width/self.columns-7

			button = WordButton(self, size=wx.Size(column_width,40), num=i, word=word, outercolor=colors[i], innercolor=self.log.bgcolor, fontcolor="White")
			"""
			b_frame = wx.Panel(self, size = wx.Size(column_width,40))
			bf_sizer = wx.BoxSizer(wx.VERTICAL)
			h_sizer = wx.BoxSizer(wx.HORIZONTAL)
			button = wx.Panel(b_frame, style = wx.NO_BORDER, size = wx.Size(column_width-4,36))
			h_sizer.Add(button, 0, wx.CENTER)
			bf_sizer.AddStretchSpacer(1)
			bf_sizer.Add(h_sizer,0, wx.CENTER)
			bf_sizer.AddStretchSpacer(1)
			b_frame.SetSizer(bf_sizer)

			b_frame.SetBackgroundColour(colors[i])
			button.SetBackgroundColour(self.log.bgcolor)
			buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
			button.SetSizer(buttonSizer)
			number_label = wx.StaticText(button, label=str((i+1)), size=wx.Size(30,-1))
			word_label = wx.StaticText(button, label=word, style=wx.ALIGN_LEFT)
			word_label.SetForegroundColour(self.fontcolor)
			number_label.SetForegroundColour(self.fontcolor)
			buttonSizer.Add(number_label)
			buttonSizer.Add(word_label)
			button.Layout()
			b_frame.Layout()
			"""
			self.log.Unbind(wx.EVT_CHAR_HOOK)
			self.log.Bind(wx.EVT_CHAR_HOOK, lambda event: self.onKey(event))
			self.epSizer.Add(button)
			button.Bind(wx.EVT_LEFT_UP, lambda event, w = word: self.onClick(event,w))
		self.Layout()

	# returns the number of the active button
	def active_number(self):
		return self.active_row * self.columns + self.active_column

	# moves the button selector down one spot	
	def nav_up(self):
		if self.active_row > 1:
			self.active_row -= 1

	# moves the button selector down one spot
	def nav_down(self):
		if self.active_row < self.max/self.columns:
			self.active_row += 1

	# moves the button selector left one spot
	def nav_left(self):
		if self.active_column > 1:
			self.active_column -= 1

	# moves the button selector right one spot
	def nav_right(self):
		if self.active_column < self.columns:
			self.active_column += 1



	def weighted_combine(self, suggestions_list):
		suggestions = {}
		for x, weight in suggestions_list:
			for word, value in x:
				if word in suggestions:
					suggestions[word] += value * weight
				else:
					suggestions[word] = value * weight
		top_suggestions = list(reversed(sorted(suggestions.items(),key=operator.itemgetter(1))))
		return [(word, score) for word, score in top_suggestions]

	# given a list of scores, returns a list of colors in the format (R,G,B)
	def scores_to_colors(self, scores):
		min_score = min(scores)
		max_score = max(scores)
		score_range = max_score - min_score
		difs_from_min = [score-min_score for score in scores]
		proportional_difs = [dif/score_range for dif in difs_from_min]
		intensities = [55+proportion*200 for proportion in proportional_difs]
		colors = [(intensity, intensity, 0) for intensity in intensities]
		return colors


	def onClick(self, event, word):
		self.log.addWord(word)
		wx.CallAfter(self.refresh)


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
			self.refresh()

		elif keycode == 8: # delete key
			self.log.deleteWord()
			self.refresh()
		elif chr(keycode).isdigit():
			index = int(chr(keycode))
			if shift_down:
				index += 10
			#word = str(self.suggestions[index-1])
			word = str(self.options[index-1])
			self.log.addWord(word)
			self.refresh()
		else:
			event.DoAllowNextEvent()




