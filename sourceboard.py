from __future__ import division
import wx
from channel import Channel
from document import Document
from log import Log
import wx.lib.scrolledpanel

class SourceBoard(wx.lib.scrolledpanel.ScrolledPanel):

	def __init__(self,parent,writer,log,channels=[]):

		wx.lib.scrolledpanel.ScrolledPanel.__init__(self, parent, size=(205,450), pos=(0,28), style=wx.SIMPLE_BORDER)

		self.log = log
		self.writer = writer
		self.channels = channels
		self.colors = [(255,0,0),(0,255,0),(0,0,255),
						(255,255,0),(0,255,255),(255,0,255)]

		self.sbSizer = wx.GridSizer(0, 1, 5, 5)
		self.SetSizer( self.sbSizer )
		for c in self.channels:
			self.addChannel(c)

	def addChannel(self, document):
		c = Channel(self, self.writer, document, self.log, self.colors[len(self.channels)])
		self.channels.append(c)
		self.sbSizer.Add(c)
		self.sbSizer.Layout()
		self.Layout()
		self.SetupScrolling(scroll_x = False, scroll_y = True)

	def removeChannel(self, c):
		if c in self.channels:
			self.channels.remove(c)
			self.sbSizer.Remove(c)
			c.Destroy()
		self.sbSizer.Layout()
		self.Layout()

	def refresh(self):
		for c in self.channels:
			c.refresh()

	# activates only the given channel
	def set_solo(self, solo_channel):
		for c in self.channels:
			c.weight = 0
			c.wt_slider.SetValue(0)
		solo_channel.weight = 100
		solo_channel.wt_slider.SetValue(100)


	def average_color(self):
		max_value = 100*255
		color_list = [tuple([c.weight*x for x in c.color]) for c in self.channels]
		r_total = 0
		g_total = 0
		b_total = 0
		for r, g, b in color_list:
			r_total += r
			g_total += g
			b_total += b
		return (r_total/max_value*255, g_total/max_value*255, b_total/max_value*255)



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