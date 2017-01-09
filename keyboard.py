import wx

class Keyboard(wx.Panel):
	def __init__(self, parent, title, options):
		wx.Panel.__init__(self, parent, size=wx.Size(200,-1))
		keyboardSizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(keyboardSizer)

		self.log = parent.log
		self.channel = parent

		header = wx.StaticText(parent, label = title.upper(), size=wx.Size(200,40), style=wx.ALIGN_CENTRE)
		header.SetBackgroundColour((0,0,255))
		header.SetForegroundColour((255,255,255))
		keyboardSizer.Add(header)

		for i in range(len(options)):
			row = wx.BoxSizer(wx.HORIZONTAL)
			text = str(options[i])
			number_label = wx.StaticText(self, label=str(i+1))
			word_label = wx.StaticText(self, label=text, style=wx.ALIGN_LEFT)

			#word_button.text = text
			#word_button.Bind(wx.EVT_BUTTON, lambda event: self.OnWordButton(event, self.log))

			self.log.Bind(wx.EVT_CHAR_HOOK, lambda event: self.OnAddWordFromSuggestions(event, text, options))

			row.Add(number_label)
			row.Add(word_label)
			keyboardSizer.Add(row)
		self.Layout()


		parentsizer = wx.BoxSizer(wx.VERTICAL)
		parent.SetSizer(parentsizer)
		parentsizer.Add(self)

	def OnAddWordFromSuggestions(self, event, word, suggestions):
		keycode = event.GetKeyCode()
		if chr(keycode).isdigit():
			index = int(chr(keycode))
		word = suggestions[index-1]
		self.log.AppendText(word + " ")
		self.channel.refresh()

	def OnWordButton(self, event, log):
		text = event.GetEventObject().text
		log.AppendText(text + " ")