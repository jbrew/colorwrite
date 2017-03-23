import wx

class ControlPanel(wx.Panel):
	def __init__(self, parent, writer, size=wx.Size(205,-1)):
		wx.Panel.__init__(self, parent, size=size)

		self.writer = writer
		self.spacing = 8

		self.controlSizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(self.controlSizer)
		self.SetBackgroundColour((80,80,80))
		
		self.loadButton = wx.Button(self, label="Load a source")
		self.loadButton.Bind(wx.EVT_BUTTON, self.onLoadChannel)
		self.controlSizer.Add(self.loadButton, 0, wx.CENTER|wx.ALL, self.spacing)

		"""
		self.settingsButton = wx.Button(self, label="Settings")
		self.settingsButton.Bind(wx.EVT_BUTTON, self.onSettingsButton)
		self.controlSizer.Add(self.settingsButton, 0, wx.CENTER|wx.ALL, self.spacing)
		"""
		
		self.colorCheckbox = wx.CheckBox(self, label="Color writing")
		self.colorCheckbox.Bind(wx.EVT_CHECKBOX, self.onColorCheck)
		self.controlSizer.Add(self.colorCheckbox, 0, wx.CENTER|wx.ALL, self.spacing)

		self.colorCheckbox = wx.CheckBox(self, label="Text to speech")
		self.colorCheckbox.Bind(wx.EVT_CHECKBOX, self.onSpeechCheck)
		self.controlSizer.Add(self.colorCheckbox, 0, wx.CENTER|wx.ALL, self.spacing)

		self.colorCheckbox = wx.CheckBox(self, label="Highlight select")
		self.colorCheckbox.Bind(wx.EVT_CHECKBOX, self.onHighlightCheck)
		self.colorCheckbox.SetValue(True)
		self.controlSizer.Add(self.colorCheckbox, 0, wx.CENTER|wx.ALL, self.spacing)
		
	# responds when color writing checkbox is clicked
	def onColorCheck(self,e):
		cb = e.GetEventObject()
		self.writer.color_writing = cb.GetValue()

	# responds when tts checkbox is clicked
	def onSpeechCheck(self,e):
		cb = e.GetEventObject()
		self.writer.speech = cb.GetValue()

	# responds when highlighting checkbox is clicked
	def onHighlightCheck(self,e):
		cb = e.GetEventObject()
		self.writer.highlighting = cb.GetValue()

	# responds when load button is clicked
	def onLoadChannel(self,e):
		self.writer.loadDialog()

	# responds when settings button is clicked
	def onSettingsButton(self,e):
		self.writer.openSettingsBox()