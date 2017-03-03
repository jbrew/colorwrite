import wx
import os
from document import Document


class Channel(wx.BoxSizer):

    def __init__(self, parent, title):
        super(Channel, self).__init__(parent, title=title)
        header = wx.StaticText(self, label = title.upper(), style=wx.ALIGN_CENTRE)
        header.SetBackgroundColour((0,0,255))
        header.SetForegroundColour((255,255,255))
        contents = wx.StaticText(self, label = '')
        searchbox = wx.TextCtrl(self)
        #searchbox.Bind(wx.EVT_CHAR_HOOK, lambda event: self.OnSearchEntry(event, searchbox, doc, contents))
        b = wx.Button(self, label = 'search')
        
        #self.Bind(wx.EVT_BUTTON, lambda event: self.OnSearchButton(event, searchbox, doc, contents), b)
        

        self.Add(header, proportion=1, flag=wx.EXPAND, border=1)
        self.Add(contents, proportion=1, flag=wx.EXPAND)
        self.Add(searchbox, flag =wx.CENTER)
        self.Add(b, flag=wx.CENTER)


class Writer(wx.Frame):
  
    def __init__(self, parent, title):
        super(Writer, self).__init__(parent, title=title, 
            size=(800, 600))
        self.sourcedir = 'data/rawtranscripts'

        self.doc_list = self.set_doc_list(number_sources=5, ngram_size=3)
        
        self.InitUI()
        self.Centre()
        self.Show()
    

    def set_doc_list(self, number_sources, ngram_size):
        doc_list = []
        for filename in os.listdir('data/rawtranscripts')[1:number_sources+1]:
            path = 'data/rawtranscripts/' + filename
            with open(path, 'r') as f:
                text = f.read()
                doc = Document(filename, text, ngram_size)
            doc_list.append(doc)
        return doc_list

    def InitUI(self):
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        doc_grid = wx.BoxSizer(wx.VERTICAL)
        

        self.Bind(wx.EVT_CHAR, self.onKey)

        gs = wx.GridSizer(4, 4, 3, 3)

        for doc in self.doc_list:
            score = str(doc.term_count('each'))
            gs.Add(self.node(doc.name, score, doc), flag = wx.EXPAND)
        
        self.log = wx.TextCtrl(self, style=wx.TE_MULTILINE, size = (200,100))

        doc_grid.Add(self.log, flag=wx.EXPAND|wx.TOP|wx.BOTTOM, border=4)
        doc_grid.Add(gs, proportion=1,flag=wx.EXPAND)

        self.SetSizer(doc_grid)

    def text_log(self):
        log = TextCtrl(self)

    def node(self, headertext, contents, doc):
        header = wx.StaticText(self, label = headertext.upper(), style=wx.ALIGN_CENTRE)
        header.SetBackgroundColour((0,0,255))
        header.SetForegroundColour((255,255,255))
        contents = wx.StaticText(self, label = '')
        searchbox = wx.TextCtrl(self)
        searchbox.Bind(wx.EVT_CHAR_HOOK, lambda event: self.OnSearchEntry(event, searchbox, doc, contents))
        b = wx.Button(self, label = 'search')
        
        self.Bind(wx.EVT_BUTTON, lambda event: self.OnSearchButton(event, searchbox, doc, contents), b)
        
        box = wx.BoxSizer(wx.VERTICAL)

        box.Add(header, proportion=1, flag=wx.EXPAND, border=1)
        box.Add(contents, proportion=1, flag=wx.EXPAND)
        box.Add(searchbox, flag =wx.CENTER)
        box.Add(b, flag=wx.CENTER)

        return box

    def OnSearchEntry(self, event, searchbox, doc, contents):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_RETURN:
            self.OnSearch(searchbox, doc, contents)
        event.Skip()

    def OnSearchButton(self, event, searchbox, doc, contents):
        self.OnSearch(searchbox, doc, value)

    def OnSearch(self, searchbox, doc, contents):
        term = searchbox.GetValue()
        count = str(doc.term_count(term))
        line = '%s:\t %s' % (term, count)
        contents.SetLabel(line)
        searchbox.SetValue('')


    def onKey(self, event):
        keycode = event.GetKeyCode()
        print keycode



if __name__ == '__main__':
  
    app = wx.App()
    Writer(None, title='Voicebox')
    app.MainLoop()