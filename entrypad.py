import wx

class EntryPad(wx.Panel):

	def __init__(self, parent, options, log):
		wx.Panel.__init__(self, parent, size=wx.Size(log.GetSize()[0],-1))
		self.epSizer = wx.GridSizer(3,3,5,5)
		self.SetSizer(self.epSizer)
		
		for o in options[0:3]:
			self.epSizer.Add(wx.StaticText(self, label=o))




