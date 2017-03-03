import wx
from document import Document
from channel import Channel
from log import Log
 
########################################################################
class MyPanel(wx.Panel):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)

        self.number_of_buttons = 0
        self.frame = parent
        self.log = Log(self)
        self.log.AppendText('it ')

        self.log.Bind(wx.EVT_CHAR_HOOK, self.onKey)
 
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        controlSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.widgetSizer = wx.GridSizer(2,2,3,3)
 
        self.addButton = wx.Button(self, label="Add")
        self.addButton.Bind(wx.EVT_BUTTON, self.onAddWidget)
        controlSizer.Add(self.addButton, 0, wx.CENTER|wx.ALL, 5)
 
        self.removeButton = wx.Button(self, label="Remove")
        self.removeButton.Bind(wx.EVT_BUTTON, self.onRemoveWidget)
        controlSizer.Add(self.removeButton, 0, wx.CENTER|wx.ALL, 5)
 
        self.mainSizer.Add(self.log)
        self.mainSizer.Add(controlSizer, 0, wx.CENTER)
        self.mainSizer.Add(self.widgetSizer, 0, wx.CENTER|wx.ALL, 10)
 
        self.SetSizer(self.mainSizer)
 
    #----------------------------------------------------------------------
    def onKey(self, event):
        keycode = event.GetKeyCode()
        if chr(keycode).isdigit():
            self.log.AppendText(" it's " + chr(keycode))
        event.Skip()


    #----------------------------------------------------------------------
    def onAddWidget(self, event):
        """"""
        self.number_of_buttons += 1
        label = "Button %s" %  self.number_of_buttons
        name = "button%s" % self.number_of_buttons
        d = Document('test', 'it was the best of times it was the worst of times')
        c = Channel(self, d, self.log)
        #new_button = wx.Button(self, label=label, name=name)
        self.widgetSizer.Add(c, 0, wx.ALL, 5)
        self.frame.fSizer.Layout()
        self.frame.Fit()
 
    #----------------------------------------------------------------------
    def onRemoveWidget(self, event):
        """"""
        if self.widgetSizer.GetChildren():
            self.widgetSizer.Hide(self.number_of_buttons-1)
            self.widgetSizer.Remove(self.number_of_buttons-1)
            self.number_of_buttons -= 1
            self.frame.fSizer.Layout()
            self.frame.Fit()
 
########################################################################
class MyFrame(wx.Frame):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, parent=None, title="Add / Remove Buttons")
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)
        self.fSizer = wx.BoxSizer(wx.VERTICAL)
        panel = MyPanel(self)
        self.fSizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(self.fSizer)
        self.Fit()
        self.Show()
 
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame()
    app.MainLoop()