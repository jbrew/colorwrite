import wx

class Keyboard(wx.Panel):
	def __init__(self, parent, title, log):
		wx.Panel.__init__(self, parent, size=wx.Size(-1,-1))
		keyboardSizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(keyboardSizer)

		self.log = log
		self.channel = parent
		self.writer = parent.writer
		self.font = wx.Font(16, wx.MODERN, wx.NORMAL, wx.NORMAL)
		self.SetFont(self.font)

		headerSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.header = wx.StaticText(self, label = title.upper(), size=wx.Size(180,40), style=wx.ALIGN_CENTRE)
		self.del_panel = wx.Panel(self)
		self.del_button = wx.StaticText(self.del_panel, label="X")
		self.del_panel.Bind(wx.EVT_LEFT_UP, self.OnDelete)
		headerSizer.Add(self.header)
		headerSizer.Add(self.del_panel)
		headerfont = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
		self.header.SetFont(headerfont)
		self.SetForegroundColour((self.channel.color))
		self.header.SetForegroundColour(self.channel.color)
		self.SetBackgroundColour((60,60,60))
		self.header.SetBackgroundColour("Black")
		keyboardSizer.Add(headerSizer)

	def OnDelete(self, e):
		wx.CallAfter(self.delete)

	def delete(self):
		self.channel.sourceboard.removeChannel(self.channel)