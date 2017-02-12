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

		self.header = wx.StaticText(parent, label = title.upper(), size=wx.Size(200,40), style=wx.ALIGN_CENTRE)
		headerfont = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
		self.header.SetFont(headerfont)
		self.SetForegroundColour((self.channel.color))
		self.header.SetForegroundColour(self.channel.color)
		self.SetBackgroundColour((60,60,60))
		self.header.SetBackgroundColour("Black")
		keyboardSizer.Add(self.header)

		