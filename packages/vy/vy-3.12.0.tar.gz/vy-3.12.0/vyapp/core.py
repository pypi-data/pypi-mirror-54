"""
This module implements widgets that permit managing tabs, panes in vy.
"""

from tkinter import *
from .areavi import AreaVi
from tkinter.ttk import Notebook

class PanedHorizontalWindow(PanedWindow):
    """
    This widget is used to create horizontal panes.
    """

    def __init__(self, *args, **kwargs):
        PanedWindow.__init__(self, orient=HORIZONTAL, *args, **kwargs)

    def create(self, filename='none'):
        """
        This method creates a horizontal AreaVi widget. It returns the
        AreaVi widget that was created. It as well installs the plugins
        that appear in the vyrc file in the AreaVi widget.
        """
        frame     = Frame(master=self)
        scrollbar = Scrollbar(master=frame)
        area      = AreaVi(filename, frame , border=3, relief=RAISED, 
                           yscrollcommand=scrollbar.set)
        scrollbar.config(command=area.yview)
        scrollbar.pack(side='right', fill=Y)

        from vyapp.plugins import HANDLE

        for handle, args, kwargs in HANDLE:
            handle(area, *args, **kwargs)

        area.focus_set()
        area.pack(expand=True, side='left', fill=BOTH)
        self.add(frame)

        def save_focus(event):
            self.master.focused_area = area

        self.master.focused_area = area
        area.bind('<FocusIn>', save_focus)
        return area

    def load(self, filename):
        """
        It creates a horizontal split and loads the content of filename
        into the new AreaVi instance. It returns the AreaVi widget that
        was created.
        """

        area = self.create()
        area.load_data(filename)
        return area

class PanedVerticalWindow(PanedWindow):
    """
    This widget implements vertical panes.
    """

    def __init__(self, *args, **kwargs):
        PanedWindow.__init__(self, orient=VERTICAL, *args, **kwargs)
        self.focused_area = None

    def create(self, filename='none'):
        """
        This method creates a new horizontal window in which
        it is possible to create new horizontal splits. The argument filename
        is set as attribute for the new AreaVi widget.
        """

        base = PanedHorizontalWindow(master=self)
        self.add(base)
        area = base.create(filename)
        return area

    def open(self, filename):
        base = PanedHorizontalWindow(master=self)
        self.add(base)
        area = base.load(filename)
        return area

    def load(self, *args):
        """
        This method adds a new horizontal window and loads
        the content of the files passed as args in the new AreaVi

        widgets.
        """

        base = PanedHorizontalWindow(master=self)
        self.add(base)

        for ind in args:
            base.load(ind)
        return base

class NoteVi(Notebook):
    """
    This class implements vy tabs.
    """

    def __init__(self, *args, **kwargs):
        Notebook.__init__(self, *args, **kwargs)
        self.bindtags((self, '.', 'all'))

    def create(self, filename):
        """
        This method creates a new tab whose title is the string
        passed as filename.
        """

        base = PanedVerticalWindow(master=self)
        area = base.create(filename)
        self.add(base, text=filename)
        return area

    def open(self, filename):
        base = PanedVerticalWindow(master=self)
        self.add(base)
        area = base.open(filename)
        return area

    def load(self, *args):
        """
        This method opens the files that are specified in args into new tabs and panes.
        The structure of args is like:

        args = ((('file1', 'file2'), ('file3', 'file4')), (('file5', 'file6'), ))

        It would create two tabs, the first tab would have four panes, the second tab
        would be two panes.
        """

        for indi in args:
            base = PanedVerticalWindow(master=self)
            base.pack(side='left', expand=True, fill=BOTH)
            self.add(base)        
            for indj in indi:
                base.load(*indj)

    def next(self, func):
        """
        """

        tabs  = self.tabs()
        index = self.index(self.select())

        for ind in tabs[index + 1:]:
            if func(self.tab(ind, 'text')): 
                yield ind
    
    def back(self, func):
        """
        """

        tabs  = self.tabs()
        index = self.index(self.select())
        tabs  = tabs[:index]

        for ind in reversed(tabs):
            if func(self.tab(ind, 'text')): 
                yield ind

    def find(self, func):
        for ind in self.tabs():
            if func(self.tab(ind, 'text')):
                yield ind

    def set_area_focus(self):
        wid  = self.nametowidget(self.select())
        wid.focused_area.focus_set()

    def restore_area_focus(self):
        """
        When an AreaVi is destroyed, the focused_area
        is a dead widget, so it gives focus to the first AreaVi
        in the active tab.
        """

        wid  = self.nametowidget(self.select())
        seq  = AreaVi.areavi_widgets(wid)
        area = next(seq)
        area.focus_set()

    def on(self, *args):
        """
        When the method Notebook.select is called it sets the application
        focus to the last visible widget in the selected tab. This method
        calls select then restores the focus. It may sound like a bug in tkinter.
        """

        wid=self.focus_get()
        self.select(*args)
        self.after(30, lambda : wid.focus_set())



