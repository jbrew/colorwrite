import wx
from document import Document
from channel import Channel
from log import Log
from sourceboard import SourceBoard
from settingsbox import SettingsBox
from controlpanel import ControlPanel
from entrypad import EntryPad
import threading

 
########################################################################
class Rainbowrite(wx.Panel):
	""""""
 
	#----------------------------------------------------------------------
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, size = (1050,600))

		self.frame = parent
		self.SetBackgroundColour((40,40,40))
		self.SetForegroundColour((255,255,255))

		self.color_writing = False
 
		self.mainSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.SetSizer(self.mainSizer)
		
		self.inputPanel = wx.Panel(self)
		self.inputSizer = wx.BoxSizer(wx.VERTICAL)
		self.inputPanel.SetSizer(self.inputSizer)

		self.outputPanel = wx.Panel(self)
		self.outputSizer = wx.BoxSizer(wx.VERTICAL)
		self.outputPanel.SetSizer(self.outputSizer)
		
		self.log = Log(self.outputPanel, self)           # text control for text output
		self.outputSizer.AddSpacer((0,50))
		self.outputSizer.Add(self.log)

		self.controlPanel = ControlPanel(self.inputPanel, self, size=wx.Size(205,-1))
		self.sourceboard = SourceBoard(self.inputPanel, self, self.log, channels=[])
		
		self.ep = EntryPad(self.outputPanel,self.sourceboard,self.log,self)
		self.outputSizer.AddSpacer((0,10))
		self.outputSizer.Add(self.ep)

		self.inputSizer.Add(self.controlPanel)
		self.inputSizer.Add(self.sourceboard)
		
		self.mainSizer.Add(self.inputPanel)
		self.mainSizer.AddSpacer((10,0))
		self.mainSizer.Add(self.outputPanel)

		self.addPathAsChannel('texts/terrible love.rtf')

		"""
		if len(self.sourceboard.channels) == 0:
			self.loadDialog()
		"""


	#----------------------------------------------------------------------
	def refresh(self):
		self.sourceboard.refresh()
		self.ep.Destroy()
		self.ep = EntryPad(self.outputPanel,self.sourceboard,self.log,self)
		self.outputSizer.Add(self.ep, wx.BOTTOM)
		self.Layout()


	#----------------------------------------------------------------------
	def addPathAsChannel(self, path):
		with open(path) as f:
			text = f.read()

		name = path.split('/')[-1]
		d = Document(name, text)
		self.sourceboard.addChannel(d)
		self.refresh()
		self.frame.fSizer.Layout()
		self.frame.Fit()

	def openSettingsBox(self):
		sb = SettingsBox(self, self)

	def loadDialog(self):
		loadChannelDialog = wx.FileDialog(self, style = wx.FD_MULTIPLE)

		loadChannelDialog.SetMessage("Select a source text.")

		loadChannelDialog.ShowModal()

		paths = loadChannelDialog.GetPaths()
		for path in paths:
			self.addPathAsChannel(path)
		

		loadChannelDialog.Destroy()

 
########################################################################
class TopFrame(wx.Frame):
	""""""
 
	#----------------------------------------------------------------------
	def __init__(self):
		"""Constructor"""
		wx.Frame.__init__(self, parent=None, title="Rainbowrite")
		menubar = wx.MenuBar()
		fileMenu = wx.Menu()
		menubar.Append(fileMenu, '&File')
		self.SetMenuBar(menubar)
		self.fSizer = wx.BoxSizer(wx.VERTICAL)
		panel = Rainbowrite(self)
		self.fSizer.Add(panel, 1, wx.EXPAND)
		self.SetSizer(self.fSizer)
		self.Fit()
		self.Center()
		self.Show()
 
#----------------------------------------------------------------------
if __name__ == "__main__":
	app = wx.App(False)
	frame = TopFrame()
	app.MainLoop()