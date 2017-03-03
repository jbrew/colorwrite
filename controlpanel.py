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

		self.settingsButton = wx.Button(self, label="Settings")
		self.settingsButton.Bind(wx.EVT_BUTTON, self.onSettingsButton)
		self.controlSizer.Add(self.settingsButton, 0, wx.CENTER|wx.ALL, self.spacing)

		self.colorCheckbox = wx.CheckBox(self, label="Color writing")
		self.colorCheckbox.Bind(wx.EVT_CHECKBOX, self.onChecked)
		self.controlSizer.Add(self.colorCheckbox, 0, wx.CENTER|wx.ALL, self.spacing)

	def onChecked(self,e):
		cb = e.GetEventObject()
		self.writer.color_writing = cb.GetValue()

	def onLoadChannel(self,e):
		self.writer.loadDialog()

	def onSettingsButton(self,e):
		self.writer.openSettingsBox()