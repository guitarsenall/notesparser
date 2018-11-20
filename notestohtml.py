
# notestohtml.py
# provide a GUI for notes parsing
# cloned from listing12-6.py

################################################################################
################################################################################
###                         Notes to HTML Parser                             ###
################################################################################
################################################################################

import sys, re, os
from handlers import *
from util import *
from rules import *

class Parser:
    """
    A Parser reads a text file, applying rules and controlling a
    handler.
    """
    def __init__(self, handler):
        self.handler = handler
        self.rules = []
        self.filters = []
    def addRule(self, rule):
        self.rules.append(rule)
    def addFilter(self, pattern, name):
        def filter(block, handler):
            return re.sub(pattern, handler.sub(name), block)
        self.filters.append(filter)
    def parse(self, file):
        self.handler.start('document')
        for block in lines(file):  # for block in blocks(file):
            for filter in self.filters:
                block = filter(block, self.handler)
            for rule in self.rules:
                #print rule.type
                if rule.condition(block):
                    last = rule.action(block, self.handler)
                    if last: break
        self.handler.end('document')


class BasicTextParser(Parser):
    """
    A specific Parser that adds rules and filters in its
    constructor.
    """
    def __init__(self, handler):
        Parser.__init__(self, handler)

        self.addRule( TitleRule()       )
        self.addRule( HeadingRule()     )
        self.addRule( LongURLLineRule() )

        # ImageFileRule comes after URL
        directory   = os.getcwd()
        extensions = ['jpg', 'bmp', 'png', 'gif']
        self.image_file_names                                   \
            = [ fn for fn in os.listdir(directory)              \
                if any(fn.endswith(ext) for ext in extensions)  ]
        self.addRule( ImageFileRule(self.image_file_names)  )

        # paragraph rule is last and default
        self.addRule( ParagraphRule() )

        # filters
        self.addFilter(r'\*(.+?)\*', 'emphasis')
        #self.addFilter(r'(http://[\.a-zA-Z/]+)', 'url')
        #self.addFilter(r'(https?://[\.a-zA-Z/]+)', 'url')
        self.addFilter(r'([\.a-zA-Z]+@[\.a-zA-Z]+[a-zA-Z]+)', 'mail')

        self.image_file_names   = []

################################################################################
################################################################################
###                               GUI                                        ###
################################################################################
################################################################################

import wx

#---------------------------------------------------------------------------

# This is how you pre-establish a file filter so that the dialog
# only shows the extension(s) you want it to.
wildcard = "Text files (*.txt)|*.txt|"  \
           "Python source (*.py)|*.py|" \
           "All files (*.*)|*.*"

#---------------------------------------------------------------------------


def load(event):
    #    file = open(FileNameCtl.GetValue())
    #    ContentsCtl.SetValue(file.read())
    #    file.close()

    # Create the dialog. In this case the current directory is forced as the starting
    # directory for the dialog, and no default file name is forced.
    # Finally, if the directory is changed in the process of getting files, this
    # dialog is set up to change the current working directory to the path chosen.
    dlg = wx.FileDialog(
        None, message="Choose a file",
        defaultDir=os.getcwd(),
        defaultFile="",
        wildcard=wildcard,
        style=wx.FD_OPEN |
              wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST |
              wx.FD_PREVIEW
        )

    # Show the dialog and retrieve the user response. If it is the OK response,
    # process the data.
    if dlg.ShowModal() == wx.ID_OK:
        # This returns a Python list of files that were selected.
        paths = dlg.GetPaths()
        #contents.SetValue('You selected %d files:' % len(paths))
        OutStr = [ "CWD: %s" % os.getcwd() ]
        (head, NotesFN) = os.path.split(paths[0])
        OutStr.append( 'PATH: %s' % head )
        OutStr.append( 'FILE: %s' % NotesFN )
        ContentsCtl.SetValue( '\n'.join(OutStr) )
        FileNameCtl.SetValue( NotesFN )
        win.SetStatusText(os.getcwd(), number=0)
        prefix = NotesFN.split('.')[0]
        NotesHtmlFN = prefix + '.html'
        HTMLNotesNameCtl.SetValue( NotesHtmlFN )

    # Destroy the dialog.
    dlg.Destroy()


def WriteHTMLNotesFile(event):
    NotesHtmlFN = HTMLNotesNameCtl.GetValue()
    print 'write button called with ' + NotesHtmlFN
    print 'HTMLTitle: ' + HTMLTitleCtl.GetValue()
    print 'max image width & height: %s, %s' % \
        ( MaxImageWidthCtl.GetValue(), MaxImageHeightCtl.GetValue() )
    SortSchemeChoice = SortSchemeCtl.GetSelection()
    SortSchemeChoice = SortSchemeCtl.GetString(SortSchemeChoice)
    print 'sorting scheme choice: ' + SortSchemeChoice
    if os.path.exists(NotesHtmlFN):
        dlg = wx.MessageDialog(win,
                    'Output file exists! Do you want to overwrite?',
                    'WARNING',
                    wx.OK | wx.CANCEL | wx.ICON_EXCLAMATION
                    )
        if dlg.ShowModal() != wx.ID_OK:
            print 'wx.OK not chosen'
            dlg.Destroy()
            return
        print 'wx.OK chosen'
        dlg.Destroy()
    print 'processing file'
    handler = HTMLFileRenderer( NotesHtmlFN )
    parser = BasicTextParser(handler)
    with open('test_input.txt', 'r' ) as InputFile:
        parser.parse(InputFile)

app = wx.App()
win = wx.Frame(None, title="Notes to HTML", size=(600, 400))

stBar   = win.CreateStatusBar(number=1, style=wx.STB_DEFAULT_STYLE, id=-1,
                                name='stBar')
win.SetStatusText(os.getcwd(), number=0)

bkg = wx.Panel(win)

notesText   = wx.StaticText(bkg, label="Select the notes file.")
hBox1 = wx.BoxSizer()
hBox1.Add(notesText, proportion=1, flag=wx.EXPAND)

# notes input filename
FileNameCtl = wx.TextCtrl(bkg)
loadButton = wx.Button(bkg, label='Open')
loadButton.Bind(wx.EVT_BUTTON, load)
hBox2 = wx.BoxSizer()
hBox2.Add(FileNameCtl, proportion=1, flag=wx.EXPAND)
hBox2.Add(loadButton, proportion=0, flag=wx.LEFT, border=5)

# outputs separator line
SeparatorText   = wx.StaticText(bkg, label = \
    "-------------------- outputs ---------------------")
hBox3 = wx.BoxSizer()
hBox3.Add(SeparatorText, proportion=1, flag=wx.EXPAND)

# HTML notes filename
HTMLNotesNameCtl = wx.TextCtrl(bkg)
saveButton = wx.Button(bkg, label='WRITE HTML')
saveButton.Bind(wx.EVT_BUTTON, WriteHTMLNotesFile)
hBox4 = wx.BoxSizer()
hBox4.Add(HTMLNotesNameCtl, proportion=1, flag=wx.EXPAND)
hBox4.Add(saveButton, proportion=0, flag=wx.LEFT, border=5)

#HTML Page Title
HTMLTitleTxt    = wx.StaticText(bkg, label = 'HTML Page Title:')
HTMLTitleCtl    = wx.TextCtrl(bkg, value='Default Page Title')
hBox5 = wx.BoxSizer()
hBox5.Add(HTMLTitleTxt, proportion=0, flag=wx.RIGHT, border=5)
hBox5.Add(HTMLTitleCtl, proportion=1, flag=wx.EXPAND)

#Sorting Scheme
SortSchemeTxt = wx.StaticText(bkg, label = "Index Sorting Scheme:" )
SortSchemeCtl = wx.Choice(bkg,
                        choices = ['alphabetical', 'creation date'])
SortSchemeCtl.SetSelection(1)
def SortEventChoice(event):
    print 'SortEventChoice: %s\n' % event.GetString()
bkg.Bind(wx.EVT_CHOICE, SortEventChoice, SortSchemeCtl)
hBox6 = wx.BoxSizer()
hBox6.Add(SortSchemeTxt, proportion=0, flag=wx.RIGHT, border=5)
hBox6.Add(SortSchemeCtl, proportion=0, flag=wx.EXPAND)

#Max Image Width and Max Image Height
import wxtextvalidators as tv
MaxImageWidthTxt    = wx.StaticText(bkg, label = 'Max Image Width:')
MaxImageWidthCtl    = wx.TextCtrl(bkg, value='2000',
                            validator = tv.MyValidator(tv.DIGIT_ONLY) )
MaxImageHeightTxt   = wx.StaticText(bkg, label = 'Max Image Height:')
MaxImageHeightCtl   = wx.TextCtrl(bkg, value='2000',
                            validator = tv.MyValidator(tv.DIGIT_ONLY) )
hBox7 = wx.BoxSizer()
hBox7.Add(MaxImageWidthTxt, proportion=0, flag=wx.RIGHT, border=5)
hBox7.Add(MaxImageWidthCtl, proportion=1, flag=wx.EXPAND | wx.RIGHT, border=5)
hBox7.Add(MaxImageHeightTxt, proportion=0, flag=wx.RIGHT, border=5)
hBox7.Add(MaxImageHeightCtl, proportion=1, flag=wx.EXPAND | wx.RIGHT, border=5)


#Behavior If Files Exist



ContentsCtl = wx.TextCtrl(bkg, style=wx.TE_MULTILINE | wx.HSCROLL)


vbox = wx.BoxSizer(wx.VERTICAL)
vbox.Add(hBox1, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
vbox.Add(hBox2, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
vbox.Add(hBox3, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
vbox.Add(hBox4, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
vbox.Add(hBox5, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
vbox.Add(hBox6, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
vbox.Add(hBox7, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
vbox.Add(ContentsCtl, proportion=1,
         flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=5)

bkg.SetSizer(vbox)
win.Show()

app.MainLoop()