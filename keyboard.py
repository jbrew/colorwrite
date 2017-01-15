import wx

class Keyboard(wx.Panel):
	def __init__(self, parent, title, options, log):
		wx.Panel.__init__(self, parent, size=wx.Size(300,-1))
		keyboardSizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(keyboardSizer)

		self.log = log
		self.channel = parent
		self.writer = parent.writer
		self.options = options
		self.font = wx.Font(16, wx.MODERN, wx.NORMAL, wx.NORMAL)
		self.SetFont(self.font)

		self.header = wx.StaticText(parent, label = title.upper(), size=wx.Size(300,40), style=wx.ALIGN_CENTRE)
		self.header.SetBackgroundColour((0,0,0))
		self.header.SetForegroundColour((255,255,255))
		keyboardSizer.Add(self.header)

		columnSizer1 = wx.BoxSizer(wx.VERTICAL)
		columnSizer2 = wx.BoxSizer(wx.VERTICAL)
		keyPanelSizer = wx.BoxSizer(wx.HORIZONTAL)

		for i in range(len(options)):
			row = wx.BoxSizer(wx.HORIZONTAL)
			word = str(options[i])
			number_label = wx.StaticText(self, label=str(i+1))
			word_label = wx.StaticText(self, label=word, style=wx.ALIGN_LEFT, size= wx.Size(140,-1))

			self.log.Unbind(wx.EVT_CHAR_HOOK)
			self.log.Bind(wx.EVT_CHAR_HOOK, lambda event: self.onKey(event))

			row.Add(number_label)
			row.Add(word_label)
			if i < 10:
				columnSizer1.Add(row)
			else:
				columnSizer2.Add(row)

		keyPanelSizer.Add(columnSizer1)
		keyPanelSizer.Add(columnSizer2)
		keyboardSizer.Add(keyPanelSizer)


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
			self.channel.refresh()
		elif keycode == 8: # delete key
			self.log.deleteWord()
			self.channel.refresh()
		elif chr(keycode).isdigit():
			index = int(chr(keycode))
			if shift_down:
				index += 10
			word = self.options[index-1]
			self.log.addWord(word)
			self.channel.refresh()
		else:
			event.DoAllowNextEvent()
		
		