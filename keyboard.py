import wx

class Keyboard(wx.Panel):
	def __init__(self, parent, title, options, log):
		wx.Panel.__init__(self, parent, size=wx.Size(200,-1))
		keyboardSizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(keyboardSizer)

		self.log = log
		self.channel = parent
		self.options = options

		header = wx.StaticText(parent, label = title.upper(), size=wx.Size(200,40), style=wx.ALIGN_CENTRE)
		header.SetBackgroundColour((0,0,255))
		header.SetForegroundColour((255,255,255))
		keyboardSizer.Add(header)

		for i in range(len(options)):
			row = wx.BoxSizer(wx.HORIZONTAL)
			word = str(options[i])
			number_label = wx.StaticText(self, label=str(i+1))
			word_label = wx.StaticText(self, label=word, style=wx.ALIGN_LEFT)

			self.log.Unbind(wx.EVT_CHAR_HOOK)
			self.log.Bind(wx.EVT_CHAR_HOOK, lambda event: self.onKey(event))

			row.Add(number_label)
			row.Add(word_label)
			keyboardSizer.Add(row)


	def onKey(self, event):
		keycode = event.GetKeyCode()
		shiftdown = event.ShiftDown()
		print keycode
		if keycode == wx.WXK_LEFT:
			self.log.wordLeft()
			self.channel.refresh()
		elif keycode == 316:
			self.log.wordRight()
			self.channel.refresh()
		elif keycode > 255:
			event.DoAllowNextEvent()
		elif keycode == wx.WXK_TAB:
			self.cycle()
		elif keycode == wx.WXK_RETURN: # enter key
			self.channel.refresh()
		elif keycode == 8: # delete key
			self.log.deleteWord()
			self.channel.refresh()
		elif chr(keycode).isdigit():
			index = int(chr(keycode))
			word = self.options[index-1]
			self.log.addWord(word)
			self.channel.refresh()
		else:
			event.DoAllowNextEvent()
		
		