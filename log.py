import wx

class Log(wx.TextCtrl):

    def __init__(self, parent):
        wx.TextCtrl.__init__(self, parent, style=wx.TE_MULTILINE, size = (800,200))
        self.writer = parent

    def after(self):
        text = self.GetValue()
        insertion = self.GetInsertionPoint()
        return text[insertion:]

    def before(self):
        text = self.GetValue()
        insertion = self.GetInsertionPoint()
        return text[:insertion]

    # moves the cursor one to the left
    def wordLeft(self):
        insertion = self.GetInsertionPoint()
        lastword = self.before().split()[-1]
        self.SetInsertionPoint(insertion-len(lastword)-1)

    # moves the cursor one to the left
    def wordRight(self):
        insertion = self.GetInsertionPoint()
        nextword = self.after().split()[0]
        self.SetInsertionPoint(insertion+len(nextword)+1)

    def addWord(self, word):
        new_before = self.before() + word + " "
        self.SetValue(new_before + self.after())
        self.SetInsertionPoint(len(new_before))

    # deletes one word
    def deleteWord(self):
        after = self.after()
        self.wordLeft()
        insertion = self.GetInsertionPoint()
        self.SetValue(self.before() + after)
        self.SetInsertionPoint(insertion)
