import wx

class Log(wx.TextCtrl):

    def __init__(self, parent):
        wx.TextCtrl.__init__(self, parent, style=wx.TE_MULTILINE, size = (200,100))
        self.writer = parent
        self.Bind(wx.EVT_CHAR_HOOK, self.onKey)


    def onKey(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_TAB:
            self.cycle()
        else:
            self.AppendText(str(keycode)+" ")
