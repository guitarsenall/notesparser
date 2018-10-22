from util import *

class Rule:
    """
    Base class for all rules.
    """
    def action(self, block, handler):
        handler.start(self.type)
        handler.feed(block)
        handler.end(self.type)
        return True

class HeadingRule(Rule):
    """
    A heading is a single line that is at most 70 characters and
    that doesn't end with a colon.
    """
    type = 'heading'
    def condition(self, block):
        #print self.type + ' condition called'
        return not '\n' in block and len(block) <= 70 and not block[-1] == ':'

class TitleRule(HeadingRule):
    """
    The title is the first block in the document, provided that it is
    a heading.
    """
    type = 'title'
    first = True

    def condition(self, block):
        if not self.first: return False
        self.first = False
        return HeadingRule.condition(self, block)

class ListItemRule(Rule):
    """
    A list item is a paragraph that begins with a hyphen. As part of
    the formatting, the hyphen is removed.
    """
    type = 'listitem'
    def condition(self, block):
        return block[0] == '-'
    def action(self, block, handler):
        handler.start(self.type)
        handler.feed(block[1:].strip())
        handler.end(self.type)
        return True

class ListRule(ListItemRule):
    """
    A list begins between a block that is not a list item and a
    subsequent list item. It ends after the last consecutive list
    item.
    """
    type = 'list'
    inside = False
    def condition(self, block):
        return True
    def action(self, block, handler):
        if not self.inside and ListItemRule.condition(self, block):
            handler.start(self.type)
            self.inside = True
        elif self.inside and not ListItemRule.condition(self, block):
            handler.end(self.type)
            self.inside = False
        return False

class LongURLLineRule(Rule):
    """
    A Long URL Line begins with 'http' or occurs inside a URL.
    It is inside a URL if it is indented further than the first URL line.
    """
    type            = 'LongURLLine'
    inside          = False
    ParentIndent    = 0
    FullURL         = []
    def condition(self, block):
        BeganURL    = block.strip()[0:4].lower() == 'http'
        ContinueURL = self.inside and leadingspaces(block) > self.ParentIndent
        return BeganURL or ContinueURL
    def action(self, block, handler):
        if not self.inside:
            self.ParentIndent = leadingspaces(block)
            handler.start(self.type)
            handler.feed(block)
            self.FullURL.append( block.strip() )
            self.inside = True
        elif self.inside:
            if leadingspaces(block) > self.ParentIndent:
                handler.start(self.type)
                handler.feed(block)
                self.FullURL.append( block.strip() )
            else:   # no longer in URL
                handler.end(self.type)
                self.inside = False
        return True

class ParagraphRule(Rule):
    """
    A paragraph is simply a block that isn't covered by any of the
    other rules.
    """
    type = 'paragraph'
    def condition(self, block):
        return True