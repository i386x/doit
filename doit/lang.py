#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/lang.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2014-05-28 09:43:05 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.1.0
#! \fdesc   @pyfile.docstr
#
"""\
DoIt! language support.\
"""

__license__ = """\
Copyright (c) 2014 Jiří Kučera.

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

@register_new_type
class String(CopyableValue):
    """
    """
    __slots__ = []

    def __init__(self, content):
        """
        """

        CopyableValue.__init__(self, content)
    #-def

    def clone(self):
        """
        """

        return String("%s" % self.content)
    #-def
#-class

class Variable(object):
    """
    """
    __slots__ = [ 'name', 'value' ]

    def __init__(self, name, value = nullobject):
        """
        """

        self.name = name
        self.value = value.attached_to(self)
    #-def

    def setvalue(self, value):
        """
        """

        if value is self.value:
            return
        self.value.detached_from(self)
        self.value = value.attached_to(self)
    #-def
#-class

class Environment(object):
    """
    """
    __slots__ = [ 'prev', 'variables' ]

    def __init__(self, env = None):
        """
        """

        self.prev = env
        self.variables = {}
        self.order_of_declarations = []
    #-def

    def newvar(self, name, value):
        """
        """

        assert name not in self.order_of_declarations,\
            "Variable '%s' is is still declared." % name
        self.variables[name] = Variable(name, value)
        self.order_of_declarations.append(name)
    #-def

    def setvar(self, var):
        """
        """

        self.setvalue(var.name, var.value)
    #-def

    def getvar(self, name):
        """
        """

        var = self.variables.get(name, None)
        if var is None and self.prev is not None:
            var = self.prev.getvar(name)
        return var
    #-def

    def setvalue(self, name, value):
        """
        """

        assert name in self.order_of_declarations,\
            "Variable '%s' is not declared." % name
        self.variables[name].setvalue(value)
    #-def

    def getvalue(self, name):
        """
        """

        var = self.getvar(name)
        if var:
            return var.value
        return None
    #-def

    def clear(self):
        """
        """

        while self.order_of_declarations:
            name = self.order_of_declarations.pop()
            self.variables[name].setvalue(nullobject)
            del self.variables[name]
    #-def
#-class

class AbstractSyntaxTree(object):
    """
    """
    __slots__ = [ 'parent', 'trees', 'ntrees', 'position' ]

    def __init__(self, parent, pos):
        """
        """

        self.parent = parent
        self.trees = []
        self.ntrees = 0
        self.position = pos
    #-def

    def add_tree(self, tree):
        """
        """

        self.trees.append(tree)
        self.ntrees += 1
    #-def
#-class
