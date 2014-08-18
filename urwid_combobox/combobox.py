# coding: utf8


"""A ComboBox like widget for urwid based on the popup example by Ian Ward

"""


__all__ = [ "ComboBox" ]


import urwid
from urwid.command_map import command_map
from itertools import cycle


_STYLE = "popbg"


class MenuItem(urwid.RadioButton):
    """A RadioButton with a 'click' signal

    """
    signals = urwid.RadioButton.signals + ["click", "quit"]

    def keypress(self, size, key):
        command = command_map[key]
        if command == "activate":
            self._emit("click", True)
        elif command == "menu":
            self._emit("quit")
        super(MenuItem, self).keypress(size, key)
        return key


class ComboBoxMenu(urwid.WidgetWrap):
    """A menu shown when parent is activated

    """
    signals = ["close"]

    def __init__(self, items):
        """Initialize items list

        """
        self.group = []
        self.items = []
        self._nav_search_key = None
        self._nav_iter = cycle([])
        for i in items:
            self.append(i)
        self.walker = urwid.Pile(self.items)
        self.__super.__init__(urwid.AttrWrap(urwid.Filler(
                        urwid.LineBox(self.walker)), "selectable", _STYLE))

    def keypress(self, size, key):
        """Intercept keystroke when the menu is popped.
        The focus will be set to the entry whose label starts with 
        the letter pressed on the keyboard"""
        if self._nav_search_key != key.lower():
            self._nav_search_key = key.lower()
            nav_candidates = []
            for entry in self.walker.contents:
                if entry[0].get_label().lower().startswith(key.lower()):
                    nav_candidates.append(self.walker.contents.index(entry))
            self._nav_iter = cycle(sorted(nav_candidates))
        try:
            nf = self._nav_iter.next()
            self.walker.set_focus(self.walker.contents[nf][0])


        except StopIteration, e:
            return super(ComboBoxMenu, self).keypress(size, key)
        return super(ComboBoxMenu, self).keypress(size, key)

    def append(self, item):
        """Append an item to the menu

        """
        r = MenuItem(self.group, unicode(item))
        self.items.append(r)

    def get_item(self, index):
        """Get an item by index

        """
        return self.items[index].get_label()

    def get_selection(self):
        """Return the index of the selected item

        """
        for index, item in enumerate(self.items):
            if item.state is True:
                return index


class ComboBox(urwid.PopUpLauncher):
    """A button launcher for the combobox menu

    """
    _combobox_mark = u"↓"
    signals = ["change"]

    def __init__(self, items, default=0, on_state_change=None):

        self.menu = ComboBoxMenu(items)
        self.on_state_change = on_state_change
        self.menu.items[default].set_state(True)
        self._button = DDButton(self.menu.get_item(default))
        self.__super.__init__(self._button)
        urwid.connect_signal(self.original_widget, 'click',
                lambda b: self.open_pop_up())
        for i in self.menu.items:
            urwid.connect_signal(i, 'click', self.item_changed)
            urwid.connect_signal(i, 'quit', self.quit_menu)

    def create_pop_up(self):
        """Create the pop up widget

        """
        return self.menu

    def get_pop_up_parameters(self):
        """Configuration dictionary for the pop up

        """
        return {'left':0, 'top':0, 'overlay_width':32,
                'overlay_height': len(self.menu.items) + 2}

    def item_changed(self, item, state):
        if state:
            selection = item.get_label()
            self._button.set_label(selection)
        if self.on_state_change:
            self.on_state_change(self, item, state)
        self.close_pop_up()
        self._emit("change", item, state)

    def quit_menu(self, widget):
        self.close_pop_up()

    def get_selection(self):
        return self.menu.get_selection()


class DDButton(urwid.Button):

    button_right = urwid.Text(">")
    button_left = urwid.Text("<")

    def set_label(self, s):
        s = s + " " + ComboBox._combobox_mark
        super(DDButton, self).set_label(s)


if __name__ == "__main__":
    #example

    class Lilo(object):

        def __unicode__(self):

            return unicode(str(self), "utf8")

        def __str__(self):

            return "LiLo"

    combobox = ComboBox([Lilo(), "Grub"])
    fill = urwid.Filler(urwid.Padding(combobox, 'center', 15))
    loop = urwid.MainLoop(fill, [(_STYLE, 'white', 'dark blue')], pop_ups=True)
    loop.run()
