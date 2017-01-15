import wx
from document import Document
from channel import Channel
from log import Log
 
########################################################################
class GridWriter(wx.Panel):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent, size = (900,750))

        self.number_of_buttons = 0
        self.frame = parent
        self.channels = []
        self.log = Log(self)
 
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        
        controlSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.widgetSizer = wx.GridSizer(1,4,3,3)

        self.loadButton = wx.Button(self, label="Load Corpus")
        self.loadButton.Bind(wx.EVT_BUTTON, self.onLoadChannel)
        controlSizer.Add(self.loadButton, 0, wx.CENTER|wx.LEFT, 15)

        logsizer = wx.BoxSizer(wx.HORIZONTAL) 
        logsizer.Add(self.log, 0, wx.CENTER|wx.ALL, 30)


        self.mainSizer.Add(logsizer, 0, wx.ALIGN_CENTER)
        self.mainSizer.Add(controlSizer, 0, wx.ALIGN_LEFT)
        self.mainSizer.Add(self.widgetSizer, 0, wx.CENTER|wx.ALL, 10)
 
        self.SetSizer(self.mainSizer)

        self.active_index = 0
        self.addPathAsChannel('texts/theyoungpope')
        #self.addPathAsChannel('data/rawtranscripts/ai')
        self.refresh()
        
        print self.activeChannel().doc.name


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

    #----------------------------------------------------------------------
    def addChannel(self, document):
        c = Channel(self, document, self.log)
        self.channels.append(c)
        self.widgetSizer.Add(c, 0, wx.ALL, 5)
        self.frame.fSizer.Layout()
        self.frame.Fit()        


    def onLoadChannel(self,event):
        #loadChannelDialog = wx.FileDialog(self, style = wx.FD_MULTIPLE, defaultDir='/Users/jamiebrew/Desktop/github/librarian/data/tfidf/')
        loadChannelDialog = wx.FileDialog(self, style = wx.FD_MULTIPLE, defaultDir='data/rawtranscripts/')

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
        wx.Frame.__init__(self, parent=None, title="Voicebox")
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)
        self.fSizer = wx.BoxSizer(wx.VERTICAL)
        panel = GridWriter(self)
        self.fSizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(self.fSizer)
        self.Fit()
        self.Show()
 
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame()
    app.MainLoop()