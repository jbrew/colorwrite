import wx

class Inspector(wx.Panel):

	def __init__(self, parent, doc):
		wx.Panel.__init__(self, parent)
		contents = wx.StaticText(self, label = '')
		searchbox = wx.TextCtrl(self)
		searchbox.Bind(wx.EVT_CHAR_HOOK, lambda event: self.OnSearchEntry(event, searchbox, doc, contents))
		#searchbutton = wx.Button(self, label = 'search')
		#searchbutton.Bind(wx.EVT_BUTTON, lambda event: self.OnSearchButton(event, searchbox, doc, contents))

		inspectorSizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(inspectorSizer)
		inspectorSizer.Add(searchbox, flag =wx.CENTER)
		inspectorSizer.Add(contents, proportion=1, flag=wx.EXPAND)
		#inspectorSizer.Add(searchbutton, flag=wx.CENTER)


	def OnSearchEntry(self, event, searchbox, doc, contents):
		keycode = event.GetKeyCode()
		if keycode == wx.WXK_RETURN:
			self.OnSearch(searchbox, doc, contents)
		event.Skip()

	def OnSearchButton(self, event, searchbox, doc, contents):
		self.OnSearch(searchbox, doc, contents)

	def OnSearch(self, searchbox, doc, contents):
		term = searchbox.GetValue()
		count = str(doc.term_count(term))
		line = '%s:\t %s' % (term, count)
		contents.SetLabel(line)
		searchbox.SetValue('')