import wx
import pyttsx
import sys
from speakermanager import SpeakerManager

class Log(wx.TextCtrl):

    def __init__(self, parent, writer):
        wx.TextCtrl.__init__(self, parent, style=wx.TE_MULTILINE|wx.TE_RICH2, size = (700,300))
        self.writer = writer
        self.performance = True
        if self.performance:
            self.font = wx.Font(40, wx.MODERN, wx.NORMAL, wx.NORMAL)
        else:            
            self.font = wx.Font(20, wx.MODERN, wx.NORMAL, wx.NORMAL)
        self.bgcolor = (20,20,20)
        self.fontcolor = "White"
        self.SetBackgroundColour(self.bgcolor)
        self.SetDefaultStyle(wx.TextAttr(self.fontcolor))
        self.SetFont(self.font)
        self.engine = pyttsx.init()
        self.sm = SpeakerManager().__enter__()
        

    def after(self):
        text = self.GetValue()
        insertion = self.GetInsertionPoint()
        return text[insertion:]

    def before(self):
        text = self.GetValue()
        insertion = self.GetInsertionPoint()
        return text[:insertion]

    # moves the cursor one word to the left
    def wordLeft(self):
        insertion = self.GetInsertionPoint()
        lastword = self.before().split()[-1]
        self.SetInsertionPoint(insertion-len(lastword)-1)

    # moves the cursor one word to the right
    def wordRight(self):
        insertion = self.GetInsertionPoint()
        nextword = self.after().split()[0]
        self.SetInsertionPoint(insertion+len(nextword)+1)

    def addWord(self, word):
        if self.writer.color_writing:
            new_color = self.writer.sourceboard.average_color()
            self.fontcolor = new_color
            #self.writer.bgcolor = new_color
            #self.writer.SetBackgroundColour(new_color)
        else:
            self.fontcolor = "White"
        self.SetDefaultStyle(wx.TextAttr(self.fontcolor))
        self.SetFont(self.font)

        if self.writer.speech:
            self.sm.say(word)

        self.WriteText(" " + word)

    def say(self, message):
        sys.stdout.write("say: " + message)
        self.engine.say(message)
        self.engine.iterate()        

    # deletes one word
    def deleteWord(self):
        word = self.before().split()[-1]
        insertion = self.GetInsertionPoint()
        self.Remove(insertion-(len(word)+1), insertion)

    def fontPlus(self):
        size = self.font.GetPointSize()
        size += 2
        self.font = wx.Font(size, wx.MODERN, wx.NORMAL, wx.NORMAL)
        self.SetFont(self.font)

    def fontMinus(self):
        size = self.font.GetPointSize()
        size -= 2
        self.font = wx.Font(size, wx.MODERN, wx.NORMAL, wx.NORMAL)
        self.SetFont(self.font)
