import wx

class Log(wx.TextCtrl):

    def __init__(self, parent, writer):
        wx.TextCtrl.__init__(self, parent, style=wx.TE_MULTILINE|wx.TE_RICH2, size = (700,300))
        self.writer = writer
        self.font = wx.Font(16, wx.MODERN, wx.NORMAL, wx.NORMAL)
        self.bgcolor = (60,60,60)
        self.SetBackgroundColour(self.bgcolor)
        self.SetFont(self.font)

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

    def addWord(self, word, color):
        self.SetDefaultStyle(wx.TextAttr(color, self.bgcolor))
        self.SetFont(self.font)

        self.WriteText(" " + word)
        """
        if len(self.before()) > 0 and self.before()[-1] == ' ':
            addition = word
        else:
            addition = " " + word

        new_before = self.before() + addition
        self.SetValue(new_before + self.after())
        self.SetInsertionPoint(len(new_before))
        current = self.GetInsertionPoint()
        print current
        """
        

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
