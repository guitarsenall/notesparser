class Handler:
    """
    An object that handles method calls from the Parser.

    The Parser will call the start() and end() methods at the
    beginning of each block, with the proper block name as a
    parameter. The sub() method will be used in regular expression
    substitution. When called with a name such as 'emphasis', it will
    return a proper substitution function.
    """
    def callback(self, prefix, name, *args):
        method = getattr(self, prefix+name, None)
        if callable(method): return method(*args)
    def start(self, name):
        self.callback('start_', name)
    def end(self, name):
        self.callback('end_', name)
    def sub(self, name):
        def substitution(match):
            result = self.callback('sub_', name, match)
            if result is None: match.group(0)
            return result
        return substitution

class HTMLRenderer(Handler):
    """
    A specific handler used for rendering HTML.

    The methods in HTMLRenderer are accessed from the superclass
    Handler's start(), end(), and sub() methods. They implement basic
    markup as used in HTML documents.
    """
    def start_document(self):
        print '<html><head><title>...</title></head><body><PRE>'
    def end_document(self):
        print '</PRE></body></html>'
    def start_paragraph(self):
        pass #print '<p>'
    def end_paragraph(self):
        pass #print '</p>'
    def start_heading(self):
        print '<h2>'
    def end_heading(self):
        print '</h2>'
    def start_list(self):
        print '<ul>'
    def end_list(self):
        print '</ul>'
    def start_listitem(self):
        print '<li>'
    def end_listitem(self):
        print '</li>'
    def start_imagefile(self):
        pass
    def end_imagefile(self):
        pass
    def start_LongURLLine(self):
        pass    #print '$',
    def end_LongURLLine(self):
        pass
    def writeout_LongURLLine(self, longurl, indent):
        if len(longurl) == 1:   # short URL
            print indent*' ' + ( '<a href="%s">%s</a>' %
                                 ( longurl[0], longurl[0] ) )
        else:                   # long URL
            print indent*' ' + ( '<a href="%s">%s...</a>' %
                                 ( ''.join(longurl), longurl[0] ) )
    def start_title(self):
        print '<h1>'
    def end_title(self):
        print '</h1>'
    def sub_emphasis(self, match):
        return '<em>%s</em>' % match.group(1)
    def sub_url(self, match):
        return '<a href="%s">%s</a>' % (match.group(1), match.group(1))
    def sub_mail(self, match):
        return '<a href="mailto:%s">%s</a>' % (match.group(1), match.group(1))
    def feed(self, data):
        print data,


class HTMLFileRenderer(Handler):
    """
    A specific handler used for rendering to a specified HTML file.

    The methods in HTMLRenderer are accessed from the superclass
    Handler's start(), end(), and sub() methods. They implement basic
    markup as used in HTML documents.
    """
    def __init__(self, HTMLFileName):
        #Handler.__init__(self)
        self.HTMLFileName = HTMLFileName
        self.HTMLFile   = open(HTMLFileName, 'w')
    def CloseHTMLFile(self):
        self.HTMLFile.close()
    def start_document(self):
        self.HTMLFile.write( '<html><head><title>...</title></head><body><PRE>')
    def end_document(self):
        self.HTMLFile.write(  '</PRE></body></html>')
        self.CloseHTMLFile()
    def start_paragraph(self):
        pass
    def end_paragraph(self):
        pass
    def start_heading(self):
        self.HTMLFile.write(  '<h2>')
    def end_heading(self):
        self.HTMLFile.write(  '</h2>')
    def start_list(self):
        self.HTMLFile.write( '<ul>')
    def end_list(self):
        self.HTMLFile.write( '</ul>')
    def start_listitem(self):
        self.HTMLFile.write( '<li>')
    def end_listitem(self):
        self.HTMLFile.write( '</li>')
    def start_imagefile(self):
        pass
    def end_imagefile(self):
        pass
    def start_LongURLLine(self):
        pass
    def end_LongURLLine(self):
        pass
    def writeout_LongURLLine(self, longurl, indent):
        if len(longurl) == 1:   # short URL
            self.HTMLFile.write( indent*' ' + ( '<a href="%s">%s</a>' %
                                                ( longurl[0], longurl[0] ) ) )
        else:                   # long URL
            self.HTMLFile.write( indent*' ' + ( '<a href="%s">%s...</a>' %
                                                ( ''.join(longurl), longurl[0] ) ))
        self.HTMLFile.write( '\n' ) # line feed
    def start_title(self):
        self.HTMLFile.write( '<h1>')
    def end_title(self):
        self.HTMLFile.write( '</h1>')
    def sub_emphasis(self, match):
        return '<em>%s</em>' % match.group(1)
    def sub_url(self, match):
        return '<a href="%s">%s</a>' % (match.group(1), match.group(1))
    def sub_mail(self, match):
        return '<a href="mailto:%s">%s</a>' % (match.group(1), match.group(1))
    def feed(self, data):
        self.HTMLFile.write( data,)
