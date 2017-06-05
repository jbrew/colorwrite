from __future__ import division
import wx
from corpus import Corpus
from sourcetile import SourceTile
from inspector import Inspector
import random

class Channel(wx.Panel):

	def __init__(self, parent, writer, doc, log, color=(0,0,0)):
		wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)
		self.sourceboard = parent
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
		self.inspector = False

		self.sourcetile = SourceTile(self, self.doc.name, self.log)
		self.sizer.Add(self.sourcetile)

		self.label = wx.StaticText(self, label='Weight')
		self.label.SetForegroundColour(self.color)
		self.sizer.Add(self.label)
		self.wt_slider = wx.Slider(self, value=100, minValue=0, maxValue=100)
		self.wt_slider.Bind(wx.EVT_COMMAND_SCROLL_THUMBRELEASE, self.OnWtSliderScroll)
		self.sizer.Add(self.wt_slider)

		"""
		self.f_label = wx.StaticText(self, label='Frequency')
		self.f_label.SetForegroundColour(self.color)
		self.sizer.Add(self.f_label)
		self.f_slider = wx.Slider(self, value=100, minValue=0, maxValue=100)
		self.f_slider.Bind(wx.EVT_COMMAND_SCROLL_THUMBRELEASE, self.OnFreqSliderScroll)
		self.sizer.Add(self.f_slider)

		self.sig_label = wx.StaticText(self, label='Sigscore')
		self.sig_label.SetForegroundColour(self.color)
		self.sizer.Add(self.sig_label)
		self.sig_slider = wx.Slider(self, value=100, minValue=0, maxValue=100)
		self.sig_slider.Bind(wx.EVT_COMMAND_SCROLL_THUMBRELEASE, self.OnSigSliderScroll)
		self.sizer.Add(self.sig_slider)
		"""

		#self.sourcetile.header.Bind(wx.EVT_LEFT_UP, self.OnClick)

		if self.inspector:
			self.sizer.Add(wx.StaticLine(self, -1, wx.Point(10, 30), wx.Size(200, 30)))
			self.inspector = Inspector(self, doc)
			self.inspector.SetBackgroundColour((150,150,150))
			self.sizer.Add(self.inspector)
		
	def OnWtSliderScroll(self, e):
		obj = e.GetEventObject()
		val = obj.GetValue()
		self.weight = val
		self.writer.refresh()

	def OnFreqSliderScroll(self, e):
		obj = e.GetEventObject()
		val = obj.GetValue()
		self.corpus.wt_to_frequency = val
		self.writer.refresh()

	def OnSigSliderScroll(self, e):
		obj = e.GetEventObject()
		val = obj.GetValue()
		self.corpus.wt_to_sigscore = val/1000
		self.writer.refresh()

	def OnDelete(self, e):
		self.sourceboard.removeChannel(self)


	def OnClick(self, e):
		self.writer.sourceboard.set_solo(self)

	def suggest(self, number):
		preceding = self.log.GetValue()[0:self.log.GetInsertionPoint()].split()[-2:]
		following = self.log.GetValue()[self.log.GetInsertionPoint():].split()[:2]
		return self.corpus.suggest(preceding, number)

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
		self.sourcetile.Hide()
		self.sourcetile = SourceTile(self, self.doc.name, self.log)
		self.sizer.Prepend(self.sourcetile)
		self.Layout()


	