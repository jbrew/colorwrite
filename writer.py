import wx
import os
from document import Document
from channel import Channel
from log import Log
from analyst import Analyst
from corpus import Corpus

class Writer(wx.Frame):
  
    def __init__(self, parent, title):
        super(Writer, self).__init__(parent, title=title, 
            size=(800, 600))
        self.sourcedir = 'data/rawtranscripts'

        self.doc_list = self.set_doc_list(number_sources=2, ngram_size=3)

        self.log = Log(self)

        # TODO: this must change to receive the processed ngram data about the corpus
        #self.channel_list = [(doc, Corpus(doc.name, doc.text)) for doc in self.doc_list]
        
        self.active_channel = 0

        self.InitUI()
        self.Centre()
        self.Show()
    

    def InitUI(self):
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        doc_grid = wx.BoxSizer(wx.VERTICAL)
        
        #self.Bind(wx.EVT_CHAR, self.onKey) # NB: this is how to bind events to the whole window

        gs = wx.GridSizer(1, 4, 3, 3)

        # add a new channel for each document in the list
        for doc in self.doc_list:
            score = str(doc.term_count('each'))
            newchannel = Channel(self, doc)
            gs.Add(newchannel, flag = wx.EXPAND)


        doc_grid.Add(self.log, flag=wx.EXPAND|wx.TOP|wx.BOTTOM, border=4)
        doc_grid.Add(gs, proportion=1,flag=wx.EXPAND)

        testing = wx.GridSizer(4, 1, 3, 3)
        testing.Add(wx.Button(self, label = 'test'))
        doc_grid.Add(testing, proportion=1,flag=wx.EXPAND)

        self.SetSizer(doc_grid)

    def set_doc_list(self, number_sources, ngram_size):
        doc_list = []
        for filename in os.listdir('data/rawtranscripts')[0:number_sources]:
            path = 'data/rawtranscripts/' + filename
            with open(path, 'r') as f:
                text = f.read()
                doc = Document(filename, text, ngram_size)
            doc_list.append(doc)
        return doc_list



if __name__ == '__main__':
  
    app = wx.App()
    Writer(None, title='Voicebox')
    app.MainLoop()