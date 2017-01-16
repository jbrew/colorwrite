import wx
from document import Document
from channel import Channel
from log import Log
import threading
 
########################################################################
class ColorWrite(wx.Panel):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent, size = (1050,600))

        self.number_of_buttons = 0
        self.frame = parent
        self.SetBackgroundColour((50,50,50))
        self.SetForegroundColour((255,255,255))
        self.channels = []
        self.log = Log(self)
        self.colors = [(255,0,0),(0,255,0),(100,100,255),
                        (255,255,0),(0,255,255),(255,0,255)]
 
        self.mainSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.inputSizer = wx.BoxSizer(wx.VERTICAL)
        self.outputSizer = wx.BoxSizer(wx.VERTICAL)
        
        self.controlSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sourceSizer = wx.GridSizer(0,2,3,3)

        self.loadButton = wx.Button(self, label="Load another text")
        self.loadButton.Bind(wx.EVT_BUTTON, self.onLoadChannel)
        self.controlSizer.Add(self.loadButton, 0, wx.CENTER|wx.ALL, 15)

        self.logSizer = wx.BoxSizer(wx.VERTICAL) 
        self.logSizer.Add(self.log, 0, wx.CENTER|wx.ALL, 30)

        self.inputSizer.Add(self.controlSizer, 0, wx.ALIGN_CENTER)
        self.inputSizer.Add(self.sourceSizer, 0, wx.CENTER|wx.ALL, 10)
        self.outputSizer.Add(self.logSizer, 0, wx.ALIGN_CENTER)


        self.mainSizer.Add(self.outputSizer)
        self.mainSizer.Add(self.inputSizer)
        
        
 
        self.SetSizer(self.mainSizer)

        self.active_index = 0
        #self.addPathAsChannel('texts/theyoungpope')
        #self.addPathAsChannel('data/rawtranscripts/ai')
        self.addPathAsChannel('texts/bowie')
        self.addPathAsChannel('texts/proverbs')
        self.addPathAsChannel('texts/trump')

        #self.addPathAsChannel('data/counts/overall')
        
        


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
        self.refresh()

    def cycle_backward(self):
        self.activeChannel().active = False
        self.active_index = (self.active_index - 1) % len(self.channels)
        self.activeChannel().active = True
        self.refresh()

    #----------------------------------------------------------------------
    def addPathAsChannel(self, path):
        """"""
        self.number_of_buttons += 1

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
        c = Channel(self, document, self.log, self.colors[len(self.channels)-1])
        self.channels.append(c)
        self.sourceSizer.Add(c, 0, wx.ALL, 5)
        self.frame.fSizer.Layout()
        self.frame.Fit()        

    def setActive(self, new_index):
        self.activeChannel().active = False
        self.active_index = new_index
        self.refresh()


    def onLoadChannel(self,event):
        #loadChannelDialog = wx.FileDialog(self, style = wx.FD_MULTIPLE, defaultDir='/Users/jamiebrew/Desktop/github/librarian/data/tfidf/')
        loadChannelDialog = wx.FileDialog(self, style = wx.FD_MULTIPLE, defaultDir='texts/')

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
        wx.Frame.__init__(self, parent=None, title="Color Write")
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