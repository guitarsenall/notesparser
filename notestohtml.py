
# notestohtml.py
# provide a GUI for notes parsing
# cloned from listing12-6.py

import wx
import os

#---------------------------------------------------------------------------

# This is how you pre-establish a file filter so that the dialog
# only shows the extension(s) you want it to.
wildcard = "Text files (*.txt)|*.txt|" \
           "Python source (*.py)|*.py|"     \
           "All files (*.*)|*.*"

#---------------------------------------------------------------------------


def load(event):
    #    file = open(filename.GetValue())
    #    contents.SetValue(file.read())
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
        (head, tail) = os.path.split(paths[0])
        OutStr.append( 'PATH: %s' % head )
        OutStr.append( 'FILE: %s' % tail )
        contents.SetValue( '\n'.join(OutStr) )
        filename.SetValue( tail )
        win.SetStatusText(os.getcwd(), number=0)

    # Destroy the dialog.
    dlg.Destroy()


def save(event):
    file = open(filename.GetValue(), 'w')
    file.write(contents.GetValue())
    file.close()

app = wx.App()
win = wx.Frame(None, title="Simple Editor", size=(410, 335))

stBar   = win.CreateStatusBar(number=1, style=wx.STB_DEFAULT_STYLE, id=-1,
                                name='stBar')
win.SetStatusText(os.getcwd(), number=0)

bkg = wx.Panel(win)

notesText   = wx.StaticText(bkg, label="Select the notes file.")


loadButton = wx.Button(bkg, label='Open')
loadButton.Bind(wx.EVT_BUTTON, load)

saveButton = wx.Button(bkg, label='Save')
saveButton.Bind(wx.EVT_BUTTON, save)

filename = wx.TextCtrl(bkg)
contents = wx.TextCtrl(bkg, style=wx.TE_MULTILINE | wx.HSCROLL)

hBox1 = wx.BoxSizer()
hBox1.Add(notesText, proportion=1, flag=wx.EXPAND)

hBox2 = wx.BoxSizer()
hBox2.Add(filename, proportion=1, flag=wx.EXPAND)
hBox2.Add(loadButton, proportion=0, flag=wx.LEFT, border=5)
hBox2.Add(saveButton, proportion=0, flag=wx.LEFT, border=5)

vbox = wx.BoxSizer(wx.VERTICAL)
vbox.Add(hBox1, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
vbox.Add(hBox2, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
vbox.Add(contents, proportion=1,
         flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=5)

bkg.SetSizer(vbox)
win.Show()

app.MainLoop()