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
    A Long URL Line is a line inside a URL that is indented further
    than the parent line.
    """
    type = 'LongURLLine'
    def condition(self, block):
        print self.type + ' condition called'
        return leadingspaces(block) > ParentIndent
    def action(self, block, handler):
        handler.start(self.type)
        handler.feed(block)
        handler.end(self.type)
        return True

class LongURLParentRule(LongURLLineRule):
    """
    A Long URL Parent Line is a paragraph that begins with 'http'
    """
    type = 'LongURLParent'
    inside = False
    ParentIndent = 0
    def condition(self, block):
        print self.type + ' condition called'
        return block.strip()[0:4].lower() == 'http'
    def action(self, block, handler):
        if not self.inside:
            ParentIndent = leadingspaces(block)
            handler.start(self.type)
            self.inside = True
        elif self.inside and leadingspaces(block) <= ParentIndent:
            handler.end(self.type)
            self.inside = False
        return False

class ParagraphRule(Rule):
    """
    A paragraph is simply a block that isn't covered by any of the
    other rules.
    """
    type = 'paragraph'
    def condition(self, block):
        return True