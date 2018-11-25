
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
        self.image_file_names.sort()    # alphabetical
        self.addRule( ImageFileRule(self.image_file_names)  )

        # paragraph rule is last and default
        self.addRule( ParagraphRule() )

        # filters
        self.addFilter(r'\*(.+?)\*', 'emphasis')
        #self.addFilter(r'(http://[\.a-zA-Z/]+)', 'url')
        #self.addFilter(r'(https?://[\.a-zA-Z/]+)', 'url')
        self.addFilter(r'([\.a-zA-Z]+@[\.a-zA-Z]+[a-zA-Z]+)', 'mail')

        # self.image_file_names   = []

    def BuildHTMLIndex(self, Title):
        '''
        WARNING: This overwrites HTML files index.html, contents.html,
        and others with the prefixes matching the image files in
        self.image_file_names.
        '''

        from PIL import Image

        # build the main page
        with open('index.html', 'w' ) as IndexFile:
            IndexFile.write( '<html>\n'                                       )
            IndexFile.write( '<head>\n'                                       )
            IndexFile.write( '<meta name="GENERATOR" content="PV-WAVE">\n'    )
            IndexFile.write( '<title>' + Title + '</title>\n'                 )
            IndexFile.write( '</head>\n'                                      )
            IndexFile.write( '<frameset cols="150,*">\n'                      )
            IndexFile.write( '  <frame name="contents" ' +\
                             'target="main" src="contents.html">\n'           )
            IndexFile.write( '  <frame name="main">\n'                        )
            IndexFile.write( '  <noframes>\n'                                 )
            IndexFile.write( '  <body>\n'                                     )
            IndexFile.write( '  <p>This page uses frames, '  + \
                             'but your browser does not support them.</p>\n'  )
            IndexFile.write( '  </body>\n'                                    )
            IndexFile.write( '  </noframes>\n'                                )
            IndexFile.write( '</frameset>\n'                                  )
            IndexFile.write( '</html>\n'                                      )


        # build the contents page
        with open('contents.html', 'w') as ContentsFile:

            #   print header
            ContentsFile.write( '<html>\n' )
            ContentsFile.write( '<head>\n' )
            ContentsFile.write( '<title>'+Title+'</title>\n' )
            ContentsFile.write( '<meta name="GENERATOR" content="PV-WAVE">\n' )
            ContentsFile.write( '<meta name="Microsoft Border" content="none">\n' )
            ContentsFile.write( '<base target="main">\n' )
            ContentsFile.write( '</head>\n' )
            ContentsFile.write( '<body>\n' )

            # sort based on SortSchemeCtl
            SortSchemeChoice = SortSchemeCtl.GetSelection()
            SortSchemeChoice = SortSchemeCtl.GetString(SortSchemeChoice)
            print 'sorting images based on: ' + SortSchemeChoice
            if SortSchemeChoice == 'creation date':
                self.image_file_names.sort(key=os.path.getctime)
            else:
                self.image_file_names.sort()    # alphabetical

            # # index HTML notes first
            # ContentsFile.write( '<p><a href="' + OutputFile + $
            #     '" target="main">'+tok(0)+'</a></p>'

            #   build each page
            nPages  = len(self.image_file_names)
            print 'reading images',
            for i, IFileName in zip( range(nPages), self.image_file_names ):

                prefix  = IFileName.split('.')[0]
                HFileName   = prefix + '.html'

                # try to figure out if we have an image by reading
                # the image to get the dimensions. Trap error.
                try:
                    BadImage = False
                    img = Image.open(IFileName)
                except IOError:
                    BadImage = True
                    #IF images(i) NE NotesFile THEN BEGIN
                    # skip notes file, assume text file
                    ContentsFile.write( '<p><a href="' + IFileName +
                        '" target="main">' + IFileName + '</a></p>\n' )
                except:
                    print 'unknown error opening image ' + IFileName, \
                        sys.exc_info()[0]
                    raise
                else:   # good image file
                    ContentsFile.write( '<p><a href="' + HFileName + '"' +
                        ' target="main">' + IFileName + '</a></p>\n' )
                    w, h = img.size
                    # shrink display size if necessary
                    MaxWidth    = int( MaxImageWidthCtl.GetValue() )
                    MaxHeight   = int( MaxImageHeightCtl.GetValue() )
                    if w <= MaxWidth and h <= MaxHeight:
                        ScaleImage = False
                    else:
                        ScaleImage = True
                        if w > MaxWidth:
                            h   = int( h * float(MaxWidth)/w )
                            w   = MaxWidth
                        if h > MaxHeight:
                            w   = int( w * FLOAT(MaxHeight)/h )
                            h   = MaxHeight

                # generate the html file
#                IF Behavior EQ 'Error' THEN BEGIN
#                    IF (FINDFILE(HFileName))(0) NE '' THEN MESSAGE, $
#                        HFileName + ' exists and Behavior = Error'
#                ENDIF
                with open(HFileName, 'w') as ImageHFile:
                    ImageHFile.write( '<html>\n' )
                    ImageHFile.write( '<head>\n' )
                    ImageHFile.write( '<title>'+Title+'</title>\n' )
                    ImageHFile.write( '</head>\n' )
                    ImageHFile.write( '<body>\n' )
                    if ScaleImage:
                        ImageHFile.write( '<p><img src="'+IFileName+'"' +
                                     ' width="' + str(w) + '" height="' + str(h) + '"\n' )
                    else:
                        ImageHFile.write( '<p><img src="'+IFileName+'"\n' )
                    ImageHFile.write( '    alt="'+IFileName+'"></p>\n' )
                    ImageHFile.write( '</body>\n' )
                    ImageHFile.write( '</html>\n' )

                print '.', #format='(A,$)'
            # endfor

            print 'done'

            # contents remainder
            ContentsFile.write( '</body>\n' )
            ContentsFile.write( '</html>\n' )




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
        # ContentsCtl.SetValue( '\n'.join(OutStr) )
        for s in OutStr:
            print s  #OutStr
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
    BehaviorChoice  = BehaviorCtl.GetSelection()
    BehaviorChoice  = BehaviorCtl.GetString(BehaviorChoice)
    print 'behavior choice: ' + BehaviorChoice
    if (   os.path.exists(NotesHtmlFN)          \
        or os.path.exists('index.html')         \
        or os.path.exists('contents.html') )    \
      and BehaviorChoice == 'warning':
        dlg = wx.MessageDialog(win,
                    'One or more output files exists!\n' + \
                    'Do you want to overwrite?',
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
    parser.BuildHTMLIndex( HTMLTitleCtl.GetValue() )

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
BehaviorTxt = wx.StaticText(bkg, label = "Behavior if Output Exists:" )
BehaviorCtl = wx.Choice(bkg,
                        choices = ['warning', 'overwrite'])
BehaviorCtl.SetSelection(0)
def BehaviorEventChoice(event):
    print 'BehaviorEventChoice: %s\n' % event.GetString()
bkg.Bind( wx.EVT_CHOICE, BehaviorEventChoice, BehaviorCtl )
hBox8 = wx.BoxSizer()
hBox8.Add(BehaviorTxt, proportion=0, flag=wx.RIGHT, border=5)
hBox8.Add(BehaviorCtl, proportion=0, flag=wx.EXPAND)

# vertical box sizer
vbox = wx.BoxSizer(wx.VERTICAL)
vbox.Add(hBox1, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
vbox.Add(hBox2, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
vbox.Add(hBox3, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
vbox.Add(hBox4, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
vbox.Add(hBox5, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
vbox.Add(hBox6, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
vbox.Add(hBox7, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
vbox.Add(hBox8, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
#ContentsCtl = wx.TextCtrl(bkg, style=wx.TE_MULTILINE | wx.HSCROLL)
#vbox.Add(ContentsCtl, proportion=1,
#         flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=5)

bkg.SetSizer(vbox)
win.Show()

app.MainLoop()