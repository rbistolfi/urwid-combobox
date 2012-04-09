# coding: utf8


import unittest, urwid
from .combobox import *


class ComboBoxTest(unittest.TestCase):

    def testDefault(self):

        dd = ComboBox(["Item1", "Item2"], default=0)
        selection = dd.get_selection()
        self.assertEqual(selection, 0)

        dd = ComboBox(["Item1", "Item2"], default=1)
        selection = dd.get_selection()
        self.assertEqual(selection, 1)

    def testItemSelection(self):

        dd = ComboBox(["Item1", "Item2"], default=0)
        dd.menu.items[1].keypress((15,), "enter")
        selection = dd.get_selection()
        self.assertEqual(selection, 1)

    def testSignal(self):

        c = []
        def callback(ddown, item, newstate):
            c.append(ddown)
            c.append(item)
            c.append(newstate)
        dd = ComboBox(["Item1", "Item2"])
        urwid.connect_signal(dd, "change", callback)
        dd.menu.items[1].keypress((15,), "enter")
        self.assertEqual(c[0], dd)
        self.assertEqual(c[1], dd.menu.items[1])
        self.assertTrue(c[2])

    def testOnStateChange(self):

        c = []
        def callback(ddown, item, newstate):
            c.append(ddown)
            c.append(item)
            c.append(newstate)
        dd = ComboBox(["Item1", "Item2"], on_state_change=callback)
        dd.menu.items[1].keypress((15,), "enter")
        self.assertEqual(c[0], dd)
        self.assertEqual(c[1], dd.menu.items[1])
        self.assertTrue(c[2])

