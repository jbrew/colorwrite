import wx

class SettingsBox(wx.Panel):
	def __init__(self, parent, writer):
		wx.Panel.__init__(self, parent, size = wx.Size(200,200))
		self.Show()