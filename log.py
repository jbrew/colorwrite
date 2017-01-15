import wx

class Log(wx.TextCtrl):

    def __init__(self, parent):
        wx.TextCtrl.__init__(self, parent, style=wx.TE_MULTILINE, size = (500,500))
        self.writer = parent
        self.font = wx.Font(16, wx.MODERN, wx.NORMAL, wx.NORMAL)
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

    def addWord(self, word):
        if len(self.before()) > 0 and self.before()[-1] == ' ':
            addition = word
        else:
            addition = " " + word
        new_before = self.before() + addition
        self.SetValue(new_before + self.after())
        self.SetInsertionPoint(len(new_before))

    # deletes one word
    def deleteWord(self):
        after = self.after()
        self.wordLeft()
        insertion = self.GetInsertionPoint()
        self.SetValue(self.before() + after)
        self.SetInsertionPoint(insertion)

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
