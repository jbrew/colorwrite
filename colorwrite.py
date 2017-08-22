import wx
from document import Document
from corpus import Corpus
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
		wx.Panel.__init__(self, parent, size = (1100,700))

		self.frame = parent
		self.SetBackgroundColour((40,40,40))
		self.SetForegroundColour((255,255,255))

		self.color_writing = True
		self.speech = True
		self.highlighting = True

		self.mainSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.SetSizer(self.mainSizer)
		
		self.inputPanel = wx.Panel(self)
		self.inputSizer = wx.BoxSizer(wx.VERTICAL)
		self.inputPanel.SetSizer(self.inputSizer)

		self.outputPanel = wx.Panel(self)
		self.outputSizer = wx.BoxSizer(wx.VERTICAL)
		self.outputPanel.SetSizer(self.outputSizer)
		
		self.log = Log(self.outputPanel, self)           # text control for text output
		#self.outputSizer.AddSpacer((0,50))
		self.outputSizer.Add(self.log)

		self.controlPanel = ControlPanel(self.inputPanel, self, size=wx.Size(205,-1))
		self.sourceboard = SourceBoard(self.inputPanel, self, self.log, channels=[])
		
		self.ep = EntryPad(self.outputPanel,self.sourceboard,self.log,self)
		#self.outputSizer.AddSpacer((0,10))
		self.outputSizer.Add(self.ep)

		self.inputSizer.Add(self.controlPanel)
		self.inputSizer.Add(self.sourceboard)
		
		self.mainSizer.Add(self.inputPanel)
		#self.mainSizer.AddSpacer((10,0))
		self.mainSizer.Add(self.outputPanel)
		#self.load_TED()

		#self.load_assembly_module()
		self.addChannel(['/Users/jbrew/Desktop/library/spaceneedle_low'])
		#self.addChannel(['/Users/jbrew/Desktop/library/lyrics/bowie'])
		#self.addPathAsChannel('/Users/jbrew/Desktop/library/beehive_manual.txt')
		#self.addPathAsChannel('/Users/jbrew/Desktop/library/prose/bible/genesis')
		#self.addPathAsChannel('/Users/jbrew/Desktop/library/speeches/feynman/1/_cleaner/all')
		"""
		if len(self.sourceboard.channels) == 0:
			self.loadDialog()
		"""

	def load_TED(self):
		self.sourceboard.clear_all_channels()
		self.addChannel(['/Users/jbrew/Desktop/library/TED/data/counts/1gram_counts', 
			'/Users/jbrew/Desktop/library/TED/data/counts/2gram_counts', 
			'/Users/jbrew/Desktop/library/TED/data/counts/3gram_counts', 
			'/Users/jbrew/Desktop/library/TED/data/counts/4gram_counts'])
		self.addChannel(['/Users/jbrew/Desktop/library/TED/data/rawtranscripts/ai'])

	def load_lyrics_module(self):
		self.sourceboard.clear_all_channels()
		self.addChannel(['/Users/jbrew/Desktop/library/lyrics/bowie'])
		self.addChannel(['/Users/jbrew/Desktop/library/lyrics/bjork.txt'])
		self.addChannel(['/Users/jbrew/Desktop/library/lyrics/bieber.txt'])


	#----------------------------------------------------------------------
	def refresh(self):
		self.sourceboard.refresh()
		self.ep.Destroy()
		self.ep = EntryPad(self.outputPanel,self.sourceboard,self.log,self)
		self.outputSizer.Add(self.ep, wx.BOTTOM)
		self.Layout()


	#----------------------------------------------------------------------
	def addChannel(self, paths):
		c = Corpus()
		for path in paths:
			print path
			with open(path) as f:
				text = f.read()
				name = path.split('/')[-1]
				d = Document(name, text)
				c.add_document(d)
		self.sourceboard.addChannel(c)
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
		self.addChannel(paths)
		

		loadChannelDialog.Destroy()

 
########################################################################
class TopFrame(wx.Frame):
	""""""
 
	#----------------------------------------------------------------------
	def __init__(self):
		"""Constructor"""
		wx.Frame.__init__(self, parent=None, title="Voicebox")
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