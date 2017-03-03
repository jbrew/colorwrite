import wx
from collections import Counter
import operator

class WordButton(wx.Panel):

	def __init__(self, parent, size, num, word, outercolor, innercolor, settings, fontcolor = "White"):
		wx.Panel.__init__(self, parent, size = size)

		self.width = self.GetSize()[0]
		self.height = self.GetSize()[1]
		self.color_off = 'Black'
		self.color_on = outercolor
		self.innercolor = innercolor
		self.fontcolor = fontcolor
		self.inset_button = wx.Panel(self, style = wx.NO_BORDER, size = wx.Size(self.width-4,36))
		self.settings = settings

		main_sizer = wx.BoxSizer(wx.VERTICAL)
		h_sizer = wx.BoxSizer(wx.HORIZONTAL)
		h_sizer.Add(self.inset_button, 0, wx.CENTER)
		main_sizer.AddStretchSpacer(1)
		main_sizer.Add(h_sizer,0, wx.CENTER)
		main_sizer.AddStretchSpacer(1)
		self.SetSizer(main_sizer)
		if self.settings.highlight_selection:
			self.SetBackgroundColour(self.color_on)
		self.inset_button.SetBackgroundColour(self.innercolor)
		buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.inset_button.SetSizer(buttonSizer)
		number_label = wx.StaticText(self.inset_button, label=str((num+1)), size=wx.Size(30,-1))
		word_label = wx.StaticText(self.inset_button, label=word, style=wx.ALIGN_LEFT)
		word_label.SetForegroundColour(self.fontcolor)
		number_label.SetForegroundColour(self.fontcolor)
		buttonSizer.Add(number_label)
		buttonSizer.Add(word_label)
		self.inset_button.Layout()
		if settings.mouse_highlighting:
			self.Bind(wx.EVT_ENTER_WINDOW, self.highlight)
			self.Bind(wx.EVT_LEAVE_WINDOW, self.unhighlight)
		self.Layout()

	def highlight(self, e):
		self.SetBackgroundColour(self.color_on)
		self.Refresh()

	def unhighlight(self, e):
		self.SetBackgroundColour(self.color_off)
		self.Refresh()
