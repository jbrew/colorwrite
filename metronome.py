from wx import *
mspm = 60*1000 # milliseconds per minute
class MFrame(wx.Frame):
    def __init__(self,):
        wx.Frame.__init__(self,None)
        #define the components
        self.go = wx.Button(self,wx.ID_ANY,"Start")
        self.stop = wx.Button(self,wx.ID_ANY,"Stop")
        self.bpm = wx.SpinCtrl(self,wx.ID_ANY,value="120",min=0,max=240)
        #do the layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(self,wx.ID_ANY,"Set the beats per minute"))
        sizer.Add(self.bpm)
        sizer.Add(self.go)
        sizer.Add(self.stop)
        self.SetSizerAndFit(sizer)
        self.Layout()
        #Bind events
        self.Bind(wx.EVT_BUTTON,self.Start,self.go)
        self.Bind(wx.EVT_BUTTON,self.Stop,self.stop)
        self.Bind(wx.EVT_TIMER,self.Tick)
    def Start(self,evt):
        self.timer=wx.Timer(self)
        self.timer.Start(mspm/float(self.bpm.GetValue()))
        print "go!"
        self.go.Enable(False)
        self.stop.Enable(True)
    def Stop(self,evt):
        self.timer.Stop()
        print "stop!"
        del self.timer
        self.go.Enable(True)
        self.stop.Enable(False)
    def Tick(self,evt):
        print "tick",self.timer.GetInterval()
        sound = wx.Sound('sounds/tick2.wav')
        sound.Play(wx.SOUND_ASYNC)
        wx.YieldIfNeeded()
    def Note(self,evt):
        sound = wx.Sound('sounds/c.wav')
        sound.Play(wx.SOUND_ASYNC)
class TestApp(wx.App):
    def OnInit(self):
        mainframe = MFrame()
        self.SetTopWindow(mainframe)
        mainframe.Show()
        return 1
app = TestApp(0)
app.MainLoop()