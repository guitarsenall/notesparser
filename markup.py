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


handler = HTMLRenderer()
parser = BasicTextParser(handler)
parser.parse(sys.stdin)