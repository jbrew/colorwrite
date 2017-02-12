import wx
from document import Document
from channel import Channel
from log import Log
from sourceboard import SourceBoard
from entrypad import EntryPad
import threading

 
########################################################################
class ColorWrite(wx.Panel):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent, size = (1050,600))

        self.frame = parent
        self.SetBackgroundColour((50,50,50))
        self.SetForegroundColour((255,255,255))
        self.channels = []
        
        self.colors = [(255,0,0),(0,255,0),(100,100,255),
                        (255,255,0),(0,255,255),(255,0,255)]
 
        self.mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.mainSizer)
        
        self.outputPanel = wx.Panel(self)
        self.outputSizer = wx.BoxSizer(wx.VERTICAL)
        self.outputPanel.SetSizer(self.outputSizer)
        self.log = Log(self.outputPanel, self)            # text control for text output
        #self.ep = EntryPad(self.outputPanel,['one','two','three'],self.log)

        #self.outputHeader = wx.Panel(self.outputPanel)
        #headerSizer = wx.BoxSizer(wx.HORIZONTAL)
        #self.outputHeader.SetSizer(headerSizer)
        #headerSizer.AddSpacer((230,0))
        #l = wx.StaticText(self.outputPanel, wx.CENTER, label="Output")
        #l.SetForegroundColour("White")
        #headerSizer.Add(l)
        #self.outputSizer.Add(self.outputHeader)
        self.outputSizer.AddSpacer((0,50))
        self.outputSizer.Add(self.log)
        #self.outputSizer.Add(self.ep)

        self.inputPanel = wx.Panel(self)
        self.inputSizer = wx.BoxSizer(wx.VERTICAL)
        self.inputPanel.SetSizer(self.inputSizer)
        self.sourceboard = SourceBoard(self.inputPanel, self.log)

        self.controlPanel = wx.Panel(self.inputPanel)
        self.controlSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.loadButton = wx.Button(self.controlPanel, label="Load another source")
        self.loadButton.Bind(wx.EVT_BUTTON, self.onLoadChannel)
        self.controlSizer.Add(self.loadButton, 0, wx.CENTER|wx.ALL, 15)

        self.inputSizer.Add(self.controlPanel)
        self.inputSizer.Add(self.sourceboard)

        self.mainSizer.Add(self.inputPanel)
        self.mainSizer.AddSpacer((10,0))
        self.mainSizer.Add(self.outputPanel)
        

        self.active_index = 0

        
        #self.addPathAsChannel('texts/pbs history')
        #self.addPathAsChannel('texts/pbs nature')
        #self.addPathAsChannel('texts/pbs tech')

        
        


    def activeChannel(self):
        return self.channels[self.active_index]

    def refresh(self):
        self.channels[self.active_index].active = True
        for c in self.channels:
            c.refresh()
        self.activeChannel().refresh()

    def cycle_forward(self):
        self.activeChannel().active = False
        self.active_index = (self.active_index + 1) % len(self.channels)
        self.activeChannel().active = True
        self.sourceboard.ScrollChildIntoView(self.activeChannel())
        self.refresh()

    def cycle_backward(self):
        self.activeChannel().active = False
        self.active_index = (self.active_index - 1) % len(self.channels)
        self.activeChannel().active = True
        self.sourceboard.ScrollChildIntoView(self.activeChannel())
        self.refresh()

    #----------------------------------------------------------------------
    def addPathAsChannel(self, path):

        with open(path) as f:
            text = f.read()

        name = path.split('/')[-1]

        d = Document(name, text)
        self.addChannel(d)
        self.setActive(len(self.channels)-1)
        self.frame.fSizer.Layout()
        self.frame.Fit()

    #----------------------------------------------------------------------
    def addChannel(self, document):
        c = Channel(self.sourceboard, self, document, self.log, self.colors[len(self.channels)])
        self.channels.append(c)
        self.sourceboard.addChannel(c)
        self.sourceboard.Layout()
        self.sourceboard.Fit()        

    def setActive(self, new_index):
        self.activeChannel().active = False
        self.active_index = new_index
        self.refresh()


    def onLoadChannel(self,event):
        #loadChannelDialog = wx.FileDialog(self, style = wx.FD_MULTIPLE, defaultDir='/Users/jamiebrew/Desktop/github/librarian/data/tfidf/')
        loadChannelDialog = wx.FileDialog(self, style = wx.FD_MULTIPLE, defaultDir='~/Desktop/github/dredger/texts')

        loadChannelDialog.ShowModal()

        paths = loadChannelDialog.GetPaths()
        for path in paths:
            self.addPathAsChannel(path)
        

        loadChannelDialog.Destroy()

 
########################################################################
class MyFrame(wx.Frame):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, parent=None, title="ColorWrite")
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)
        self.fSizer = wx.BoxSizer(wx.VERTICAL)
        panel = ColorWrite(self)
        self.fSizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(self.fSizer)
        self.Fit()
        self.Center()
        self.Show()
 
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame()
    app.MainLoop()