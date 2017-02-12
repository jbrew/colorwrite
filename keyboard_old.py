import wx

class Keyboard(wx.Panel):
	def __init__(self, parent, title, suggestions, log):
		wx.Panel.__init__(self, parent, size=wx.Size(200,-1))
		keyboardSizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(keyboardSizer)

		self.log = log
		self.channel = parent
		self.writer = parent.writer
		self.suggestions = suggestions
		self.options = [word for (word, value) in suggestions]
		self.font = wx.Font(16, wx.MODERN, wx.NORMAL, wx.NORMAL)
		self.SetFont(self.font)

		self.header = wx.StaticText(parent, label = title.upper(), size=wx.Size(200,40), style=wx.ALIGN_CENTRE)
		headerfont = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
		self.header.SetFont(headerfont)
		self.SetBackgroundColour((60,60,60))
		self.header.SetBackgroundColour("Black")
		if self.channel.active:
			self.SetForegroundColour((self.channel.color))
			self.header.SetForegroundColour(self.channel.color)
		else:
			self.SetForegroundColour(tuple([x/4 for x in(self.channel.color)]))
			self.header.SetForegroundColour(tuple([x/4 for x in(self.channel.color)]))
		
		keyboardSizer.Add(self.header)

		columnSizer1 = wx.BoxSizer(wx.VERTICAL)
		#columnSizer2 = wx.BoxSizer(wx.VERTICAL)
		keyPanelSizer = wx.BoxSizer(wx.HORIZONTAL)

		for i in range(len(self.options)):
			row = wx.BoxSizer(wx.HORIZONTAL)
			word = str(self.options[i])
			number_label = wx.StaticText(self, label=str((i+1) % 10), size=wx.Size(30,-1))
			word_label = wx.StaticText(self, label=word, style=wx.ALIGN_LEFT, size= wx.Size(200,-1))

			self.log.Unbind(wx.EVT_CHAR_HOOK)
			self.log.Bind(wx.EVT_CHAR_HOOK, lambda event: self.onKey(event))

			row.Add(number_label)
			row.Add(word_label)
			columnSizer1.Add(row)

		keyPanelSizer.Add(columnSizer1)
		keyboardSizer.Add(keyPanelSizer)
		columnSizer1.Layout()



	def onKey(self, event):
		keycode = event.GetKeyCode()
		shift_down = event.ShiftDown()
		command_down = event.CmdDown()
		#print keycode
		if keycode == wx.WXK_LEFT:
			self.log.wordLeft()
			self.channel.refresh()
		elif command_down:
			if keycode == 61:
				self.log.fontPlus()
			if keycode == 45:
				self.log.fontMinus()
			event.DoAllowNextEvent()
		elif keycode == 316:
			self.log.wordRight()
			self.channel.refresh()
		elif keycode > 255:
			event.DoAllowNextEvent()
		elif keycode == wx.WXK_TAB:
			if shift_down:
				self.writer.cycle_backward()
			else:
				self.writer.cycle_forward()
		elif keycode == wx.WXK_RETURN: # enter key
			if shift_down:
				toAdd = "\n\n%s:" % self.channel.doc.name.upper()
				self.log.addWord(toAdd, self.channel.color)
			else:
				self.writer.refresh()

		elif keycode == 8: # delete key
			self.log.deleteWord()
			self.channel.refresh()
		elif chr(keycode).isdigit():
			index = int(chr(keycode))
			if shift_down:
				index += 10
			#word = str(self.suggestions[index-1])
			word = str(self.options[index-1])
			self.log.addWord(word, self.channel.color)
			self.channel.refresh()
		else:
			event.DoAllowNextEvent()

		