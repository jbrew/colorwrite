import wx
from collections import Counter
import operator

class WordButton(wx.Panel):

	def __init__(self, parent, size, num, word, outercolor, innercolor, fontcolor = "White"):
		wx.Panel.__init__(self, parent, size = size)

		self.width = self.GetSize()[0]
		self.height = self.GetSize()[1]

		main_sizer = wx.BoxSizer(wx.VERTICAL)
		h_sizer = wx.BoxSizer(wx.HORIZONTAL)
		inset_button = wx.Panel(self, style = wx.NO_BORDER, size = wx.Size(self.width-4,36))
		h_sizer.Add(inset_button, 0, wx.CENTER)
		main_sizer.AddStretchSpacer(1)
		main_sizer.Add(h_sizer,0, wx.CENTER)
		main_sizer.AddStretchSpacer(1)
		self.SetSizer(main_sizer)
		self.SetBackgroundColour(outercolor)
		inset_button.SetBackgroundColour(innercolor)
		buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
		inset_button.SetSizer(buttonSizer)
		number_label = wx.StaticText(inset_button, label=str((num+1)), size=wx.Size(30,-1))
		word_label = wx.StaticText(inset_button, label=word, style=wx.ALIGN_LEFT)
		word_label.SetForegroundColour(fontcolor)
		number_label.SetForegroundColour(fontcolor)
		buttonSizer.Add(number_label)
		buttonSizer.Add(word_label)
		inset_button.Layout()
		self.Layout()
