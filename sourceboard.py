import wx
from channel import Channel
from document import Document
from log import Log
import wx.lib.scrolledpanel

class SourceBoard(wx.lib.scrolledpanel.ScrolledPanel):

	def __init__(self,parent,log):

		wx.lib.scrolledpanel.ScrolledPanel.__init__(self, parent, size=(205,450), pos=(0,28), style=wx.SIMPLE_BORDER)

		self.log = log

		self.sbSizer = wx.GridSizer(0, 1, 5, 5)
		self.SetSizer( self.sbSizer )

	def addChannel(self, channel):
		self.sbSizer.Add(channel)
		self.sbSizer.Layout()
		self.Layout()
		self.SetupScrolling(scroll_x = False, scroll_y = True)

class MyFrame(wx.Frame):

	def __init__(self):
		wx.Frame.__init__(self,parent=None, title="BoardTest")
		menubar = wx.MenuBar()
		fileMenu = wx.Menu()
		menubar.Append(fileMenu, '&File')
		self.SetMenuBar(menubar)
		self.fSizer = wx.BoxSizer(wx.VERTICAL)
		panel = Board(self)
		self.fSizer.Add(panel, 1, wx.EXPAND)
		self.SetSizer(self.fSizer)
		self.Fit()
		self.Center()
		self.Show()

if __name__=='__main__':
	app = wx.App()
	frame = MyFrame()
	frame.Show()
	app.MainLoop()