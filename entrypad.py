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
		self.column_width = self.width/self.columns-7
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
		self.weight_highlighting = False
		self.highlight_selection = False
		self.refresh()
		
	# a full refresh. gets new suggestions from the corpus and then performs a superficial refresh
	def refresh(self):
		suggestions_list = [(c.suggest(self.max),c.weight) for c in self.sourceboard.channels]
		self.suggestions = self.weighted_combine(suggestions_list)
		self.surface_refresh()

	# only refreshes the skin of the entrypad
	def surface_refresh(self):
		suggestions = self.suggestions
		words = [word for word, score in suggestions]
		scores = [score for word, score in suggestions]
		if len(scores) > 0:
			colors = self.scores_to_colors(scores)
		self.options = words[0:self.max]
		self.epSizer.Clear(True)

		for i in range(len(self.options)):

			word = str(self.options[i])
			button_size = wx.Size(self.column_width,40)

			if self.highlight_selection and self.active_number() == i+1:
				outercolor = (0,255,0)
			elif self.weight_highlighting:
				outercolor=colors[i]
			else:
				outercolor=(0,0,0)
			
			innercolor=self.log.bgcolor

			button = WordButton(self, size=button_size, num=i, word=word, outercolor=outercolor, innercolor=innercolor, fontcolor="White")

			self.log.Unbind(wx.EVT_CHAR_HOOK)
			self.log.Bind(wx.EVT_CHAR_HOOK, lambda event: self.onKey(event))
			self.epSizer.Add(button)
			button.Bind(wx.EVT_LEFT_UP, lambda event, w = word: self.onClick(event,w))
		self.Layout()

	# returns the number of the active button
	def active_number(self):
		return (self.active_row-1) * self.columns + self.active_column

	# moves the button selector left one spot
	def nav_left(self):
		if self.active_column > 1:
			self.active_column -= 1

	# moves the button selector right one spot
	def nav_right(self):
		if self.active_column < self.columns:
			self.active_column += 1

	# moves the button selector down one spot	
	def nav_up(self):
		if self.active_row > 1:
			self.active_row -= 1

	# moves the button selector down one spot
	def nav_down(self):
		if self.active_row < self.max/self.columns:
			self.active_row += 1

	# enters the selected word
	def enter_selected(self):
		self.log.addWord(self.options[self.active_number()-1])


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
		if command_down:
			if keycode == wx.WXK_LEFT:
				self.log.wordLeft()
				self.refresh()
			elif keycode == wx.WXK_RIGHT:
				self.log.wordRight()
				self.refresh()
			elif keycode == 61:
				self.log.fontPlus()
			elif keycode == 45:
				self.log.fontMinus()
			event.DoAllowNextEvent()
		elif keycode == wx.WXK_LEFT:
			self.nav_left()
			self.surface_refresh()
		elif keycode == wx.WXK_RIGHT:
			self.nav_right()
			self.surface_refresh()
		elif keycode == wx.WXK_UP:
			self.nav_up()
			self.surface_refresh()
		elif keycode == wx.WXK_DOWN:
			self.nav_down()
			self.surface_refresh()
		elif keycode > 255:
			event.DoAllowNextEvent()
		elif keycode == wx.WXK_TAB:
			self.enter_selected()
			self.refresh()
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




