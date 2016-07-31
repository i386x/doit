#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/text/fmt/format.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-07-18 17:35:23 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Source code formatting library.\
"""

__license__ = """\
Copyright (c) 2014 - 2016 Jiří Kučera.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.\
"""

class TextNode(object):
    """
    """
    __slots__ = [ 'name' ]

    def __init__(self, name):
        """
        """

        self.name = name
    #-def
#-class

class TextBlock(TextNode):
    """
    """
    __slots__ = [ 'elements', 'alternative' ]

    def __init__(self, name, elements = [], alternative = 0):
        """
        """

        TextNode.__init__(self, name)
        self.elements = elements
        self.alternative = alternative
    #-def

    def make_subblocks(self, formatter, nobreak = False):
        """
        """

        rules = formatter.rules
        if self.name not in rules:
            raise FormatError(
                "I don't know how to process <%s> node" % self.name
            )
        rule = rules[self.name]
        if self.alternative >= len(rule.alts):
            raise FormatError("Rule <%s> has no [%d] alternative" % (
                rule.lhs, self.alternative
            ))
        alt = rule.alts[self.alternative]
        l = [Block()]
        i = j = 0
        while i < len(alt):
            node = alt[i]
            if isinstance(node, LineBreak):
                l[-1].add(node.clone())
                if node.data <= 0 and not nobreak:
                    l.append(Block())
                i += 1
            elif isinstance(node, TextOp):
                l[-1].add(node)
                i += 1
            elif isinstance(node, (Var, Term)):
                if j >= len(self.elements) \
                or not isinstance(self.elements[j], node.friend) \
                or self.elements[j].name != node.name \
                or (
                   isinstance(node, Var) \
                   and node.alternative != self.alternative
                ):
                    self.__nomatch(j, rule.lhs)
                l[-1].add(self.elements[j])
                i += 1
                j += 1
            else:
                self.__badnode(i)
        if j < len(self.elements):
            n = len(self.elements) - j
            raise FormatError(
                "The %d element%s of block [%s] remain%s unprocessed" % (
                    n,
                    "s" if n != 1 else "",
                    self.name,
                    "s" if n == 1 else ""
                )
            )
        while l and l[-1].empty():
            del l[-1]
        if l and (
            not isinstance(l[-1].elements[-1], LineBreak) \
            or l[-1].elements[-1].data > 0
        ):
            l[-1].add(LineBreak(0))
        return l
    #-def

    def __nomatch(self, j, lhs):
        """
        """

        raise FormatError(
            "Rule <%s> and block [%s] did not match at %d%s element (%s)" % (
                lhs, self.name,
                j + 1,
                "st" if (j % 10) == 0 and (j % 100) != 10 else \
                "nd" if (j % 10) == 1 and (j % 100) != 11 else \
                "rd" if (j % 10) == 2 and (j % 100) != 12 else \
                "th",
                "relatively to block"
            )
        )
    #-def

    def __badnode(self, i, lhs):
        """
        """

        raise FormatError(
            "Rule <%s>: Unknown element on %d%s position" % (
                lhs,
                i + 1,
                "st" if (i % 10) == 0 and (i % 100) != 10 else \
                "nd" if (i % 10) == 1 and (i % 100) != 11 else \
                "rd" if (i % 10) == 2 and (i % 100) != 12 else \
                "th"
            )
        )
    #-def
#-class

class TextTerminal(TextNode):
    """
    """
    __slots__ = []

    def __init__(self, name, data = None):
        """
        """

        TextNode.__init__(self, name)
        self.data = data
    #-def
#-class

class RuleNode(object):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        pass
    #-def
#-class

class Var(RuleNode):
    """
    """
    friend = TextBlock
    __slots__ = [ 'name' ]

    def __init__(self, name, alternative = 0):
        """
        """

        RuleNode.__init__(self)
        self.name = name
        self.alternative = alternative
    #-def
#-class

class Term(RuleNode):
    """
    """
    friend = TextTerminal
    __slots__ = [ 'name' ]

    def __init__(self, name = "???", data = None):
        """
        """

        RuleNode.__init__(self)
        self.name = name
        self.data = data
    #-def

    def clone(self):
        """
        """

        obj = self.__class__()
        obj.name = self.name
        obj.data = self.data
        return obj
    #-def
#-class

class TextOp(Term):
    """
    """
    __slots__ = []

    def __init__(self, name = "%??", data = None):
        """
        """

        Term.__init__(self, name, data)
    #-def
#-class

class Indent(TextOp):
    """
    """

    def __init__(self):
        """
        """

        name = '%%%s' % self.__class__.__name__.lower()
        TextOp.__init__(self, name)
    #-def
#-class

class Dedent(TextOp):
    """
    """

    def __init__(self):
        """
        """

        name = '%%%s' % self.__class__.__name__.lower()
        TextOp.__init__(self, name)
    #-def
#-class

class Space(TextOp):
    """
    """

    def __init__(self):
        """
        """

        name = '%%%s' % self.__class__.__name__.lower()
        TextOp.__init__(self, name)
    #-def
#-class

class LineBreak(TextOp):
    """
    """

    def __init__(self, cost = 0):
        """
        """

        name = '%%%s' % self.__class__.__name__.lower()
        TextOp.__init__(self, name, cost)
    #-def
#-class

class SpaceOrLineBreak(TextOp):
    """
    """

    def __init__(self, cost = 0):
        """
        """

        TextOp.__init__(self, '%space_or_linebreak', cost)
    #-def
#-class

class IncBreakCost(TextOp):
    """
    """

    def __init__(self):
        """
        """

        name = '%%%s' % self.__class__.__name__.lower()
        TextOp.__init__(self, name)
    #-def
#-class

class DecBreakCost(TextOp):
    """
    """

    def __init__(self):
        """
        """

        name = '%%%s' % self.__class__.__name__.lower()
        TextOp.__init__(self, name)
    #-def
#-class

class Rule(object):
    """
    """
    __slots__ = []

    def __init__(self, lhs, alts = []):
        """
        """

        self.lhs = lhs
        self.alts = alts
    #-def
#-class

#
# There are two kinds of blocks:
#
#   1) unexpanded, that is the block that was contained in a list returned by
#      TextBlock.make_subblocks(). Such a block contains these elements:
#
#        Indent, Dedent, Space, LineBreak, SpaceOrLineBreak, IncBreakCost,
#          DecBreakCost, TextBlock, TextTerminal
#
#      Each block in a list is terminated by LineBreak(0)
#
#   2) expanded, that is the block whose elements were expanded by
#      Block.expand_elements(). Such a block contains these elements:
#
#        Indent, Dedent, Space, LineBreak, SpaceOrLineBreak, IncBreakCost,
#          DecBreakCost, TextTerminal
#
# How to work with blocks:
#
#   Unexpanded blocks are gathered by TextBlock.make_subblocks() from input,
#   which is AST with extra informations. All nodes in such an AST are TextNode
#   instances. During the gathering, TextBlock uses the formatting rules. A
#   formatting rule contains metainformations which are not contained in AST.
#   An example of formatting rule can be
#
#     func ->
#       type %incbreakcost(3) %space_or_linebreak(1000) %decbreakcost(3)
#         ID %incbreakcost(1) fargs %decbreakcost(1) %space '{' %linebreak(0)
#       %indent
#       statements
#       %dedent
#       '}' %linebreak(0)
#
#     fargs -> '(' ')'
#     fargs -> '(' %linebreak(1000)
#              %indent
#              %incbreakcost(1)
#              fargs_
#              %decbreakcost(1)
#              %dedent
#              ')' %linebreak(0)
#     fargs_ -> farg %linebreak(1000)
#     fargs_ -> farg ',' %spaceorlinebreak(1000)
#               fargs_
#     farg -> type %space ID
#
#   Let the input (represented by AST) be
#
#     int sum ( int a , int b ) { ... }
#
#   The list returned by TextBlock.make_subblocks() for this input may looks
#   like:
#
#     [
#       Block([
#         TextBlock('type', [
#           TextTerminal(TYPENAME, 'int')
#         ]),
#         IncBreakCost(), IncBreakCost(), IncBreakCost(),
#         SpaceOrLineBreak(1000),
#         DecBreakCost(), DecBreakCost(), DecBreakCost(),
#         TextTerminal(ID, 'sum'),
#         IncBreakCost(),
#         TextBlock('fargs', [
#           TextTerminal(LPAR, '('),
#           TextBlock('fargs_', [
#             TextBlock('farg', [
#               TextBlock('type', [
#                 TextTerminal(TYPENAME, 'int')
#               ]),
#               TextTerminal(ID, 'a')
#             ]),
#             TextTerminal(COMMA, ','),
#             TextBlock('fargs_', [
#               TextBlock('farg', [
#                 TextBlock('type', [
#                   TextTerminal(TYPENAME, 'int')
#                 ]),
#                 TextTerminal(ID, 'b')
#               ])
#             ])
#           ]),
#           TextTerminal(RPAR, ')')
#         ]),
#         DecBreakCost(),
#         Space(),
#         TextTerminal(LBRC, '{'),
#         LineBreak(0)
#       ]),
#       Block([
#         Indent(),
#         TextBlock('statements', [
#           ...
#         ]),
#         Dedent(),
#         TextTerminal(RBRC, '}'),
#         LineBreak(0)
#       ])
#     ]
#
#   Given an unexpanded block, it is recommended to perform these operations
#   (in this order):
#
#     1. expand all elements
#     2. adjust break costs
#     3. call do_break first time to get a list of blocks with fixed
#        indentations
#     4. get a block
#     5. compute its length
#     6. if it satisfy the restrictions, emit it
#     7. otherwise, decrease break costs by 1 and call do_break again
#     8. repeat this from point 4 until no blocks are available or an error
#        has been encountered
#
class Block(object):
    """
    """
    __slots__ = []

    def __init__(self, elements = [], level = 0):
        """
        """

        self.elements = elements
        self.indentation_level = level
    #-def

    def add(self, element):
        """
        """

        self.elements.append(element)
    #-def

    def empty(self):
        """
        """

        return len(self.elements) == 0
    #-def

    def expand_elements(self, formatter):
        """
        """

        while self.expand_elements_once(formatter):
            pass
    #-def

    def expand_elements_once(self, formatter):
        """
        """

        expanded_elements = []
        expanded = False
        for e in self.elements:
            if isinstance(e, TextBlock):
                for b in e.make_subblocks(formatter, nobreak = True):
                    expanded_elements.extend(b.elements)
                expanded = True
            else:
                expanded_elements.append(e)
        self.elements = expanded_elements
        return expanded
    #-def

    def adjust_break_costs(self):
        """
        """

        l = []
        current_break_cost = 0

        for e in self.elements:
            if isinstance(e, LineBreak):
                l.append(e.__class__(current_break_cost))
            elif isinstance(e, IncBreakCost):
                current_break_cost += 1
            elif isinstance(e, DecBreakCost):
                current_break_cost -= 1
            else:
                l.append(e)
        self.elements = l
    #-def

    def decrease_break_costs(self, decrement = 1):
        """
        """

        for e in self.elements:
            if isinstance(e, LineBreak):
                e.data -= decrement
    #-def

    def compute_line_length(self, formatter):
        """
        """

        # Assume that this block was verified.
        l = formatter.rules.indentation * self.indentation_level

        # 1) Set the i and j to point to nonblanks:
        i, j = 0, len(self.elements)
        while i < j:
            if isinstance(self.elements[i], TextTerminal):
                break
            i += 1
        k = j
        while i < j - 1:
            if isinstance(self.elements[j - 1], TextTerminal):
                break
            j -= 1
        if i >= j:
            return k - 1, k, 1 # blank line
        # 2) Compute the line length:
        k = i
        while k < j:
            if isinstance(self.elements[k], (Space, SpaceOrLineBreak)):
                l += 1
            elif isinstance(self.elements[k], TextTerminal):
                l += len(self.elements[k].data)
            k += 1
        return i, j, l
    #-def

    def do_break(self):
        """
        """

        # Notes:
        # - before this block is broken, it should contains these types of
        #   elements: Indent, Dedent, Space, LineBreak, SpaceOrLineBreak, and
        #     TextTerminal
        # - every broken block should ends with LineBreak(0)
        # - if Indent is at the beginning of the block, then that block's
        #   indentation level is set to this block indentation level plus the
        #   increased indentation level increment
        # - if Dedent is at the beginning of the block, then that block's
        #   indentation level is set to this block indentation level plus the
        #   decreased indentation level increment
        # - the block that contains Indent/Dedent/Space should also contains
        #   TextTerminal

        blocks = []
        level = self.indentation_level
        dlevel = 0
        i = 0

        # 1) Break this block to blocks according to LineBreak(0):
        while True:
            block, i = self.get_block(i)
            if block is None:
                break
            blocks.append(block)
        # 2) Update indentation information for each block:
        for b in blocks:
            if not b.empty() and isinstance(b.elements[0], Indent):
                dlevel += 1
                del b.elements[0]
            elif not b.empty() and isinstance(b.elements[0], Dedent):
                dlevel -= 1
                del b.elements[0]
            b.indentation_level = level + dlevel
        # 3) Verify the block content for each block:
        for b in blocks:
            b.verify()
        return blocks
    #-def

    def get_block(self, i):
        """
        """

        b = Block()
        while i < len(self.elements):
            b.add(self.elements[i])
            i += 1
            if isinstance(b.elements[-1], LineBreak) \
            and b.elements[-1].data <= 0:
                break
        if b.empty():
            return None, i
        if not isinstance(b.elements[-1], LineBreak) \
        or b.elements[-1].data > 0:
            b.add(LineBreak(0))
        return b, i
    #-def

    def verify(self):
        """
        """

        for e in self.elements:
            if not isinstance(e, (
                Indent, Dedent, Space, LineBreak, TextTerminal
            )):
                raise FormatError("Forbidden element inside block")
        if self.empty() \
        or not isinstance(self.elements[-1], LineBreak) \
        or self.elements[-1].data > 0:
            raise FormatError("Block should ends with LineBreak(0)")
        i = 0
        while i < len(self.elements) - 1:
            if isinstance(self.elements[i], LineBreak) \
            and self.elements[i].data <= 0:
                raise FormatError("Block was not broken properly")
            i += 1
    #-def
#-class

class Formatter(object):
    """
    """
    __slots__ = [ 'rules' ]

    def __init__(self):
        """
        """

        self.rules = FormattingRules()
    #-def

    def format(self, text, output):
        """
        """

        unexpanded_blocks = []

        if isinstance(text, TextBlock):
            unexpanded_blocks.extend(text.make_subblocks(self))
        elif isinstance(text, TextTerminal):
            unexpanded_blocks.append(Block(elements = [text, LineBreak(0)]))
        else:
            raise FormatError("Invalid input")

        for b in unexpanded_blocks:
            b.expand_elements(self)
            b.adjust_break_costs()
            contribs = b.do_break()
            while contribs:
                c = contribs.pop(0)
                i, j, l = c.compute_line_length(self)
                if l < self.rules.line_limit:
                    output.write(c.to_str(i, j))
                    continue
                c.decrease_break_costs()
                new_contribs = c.do_break()
                if len(new_contribs) <= 1:
                    raise FormatError(
                        "Line is too long and cannot be broken properly"
                    )
                contribs[:0] = new_contribs
            #-while
        #-for
    #-def
#-class
