import wx
from corpus import Corpus
from analyst import Analyst
from keyboard import Keyboard
from inspector import Inspector
import random

class Channel(wx.Panel):

	def __init__(self, parent, writer, doc, log, color=(0,0,0)):
		wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)
		self.writer = writer
		self.color = color
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(self.sizer)
		self.doc = doc
		self.corpus = Corpus([doc])
		self.log = log
		self.active = False
		self.weight = 100
		self.suggestions = self.suggest(20)

		self.keyboard = Keyboard(self, self.doc.name, self.log)
		self.sizer.Add(self.keyboard)
		label = wx.StaticText(self, label='Weight')
		label.SetForegroundColour(self.color)
		self.sizer.Add(label)
		self.wt_slider = wx.Slider(self, value=100, minValue=0, maxValue=100)
		self.wt_slider.Bind(wx.EVT_SLIDER, self.OnSliderScroll)
		self.sizer.Add(self.wt_slider)

		self.Bind(wx.EVT_LEFT_UP, self.OnClick)
		#self.keyboard.header.Bind(wx.EVT_LEFT_UP, self.OnClick)


		#self.sizer.Add(wx.StaticLine(self, -1, wx.Point(10, 30), wx.Size(200, 30)))
		#self.inspector = Inspector(self, doc)
		#self.inspector.SetBackgroundColour((150,150,150))
		#self.sizer.Add(self.inspector)
		
	def OnSliderScroll(self, e):
		obj = e.GetEventObject()
		val = obj.GetValue()
		self.weight = val
		#new_color = self.writer.sourceboard.average_color()
		#self.writer.SetBackgroundColour(new_color)
		#self.writer.frame.Layout()

	def OnClick(self, e):
		self.writer.sourceboard.set_solo(self)

	def suggest(self, number):
		context = self.log.GetValue().split()[-2:]
		return self.corpus.suggest(context, number)

	def weighted_choice(self, choices):
		total = sum(w for (c, w) in choices)
		r = random.uniform(0, total)
		upto = 0
		for c, w in choices:
			if upto + w >= r:
				return c
			upto += w
		assert False, "Shouldn't get here"

	def refresh(self):
		context = self.log.before().split()[-2:]
		suggestions = self.corpus.suggest(context, 20)
		self.keyboard.Hide()
		self.keyboard = Keyboard(self, self.doc.name, self.log)
		self.sizer.Prepend(self.keyboard)
		self.Layout()


	