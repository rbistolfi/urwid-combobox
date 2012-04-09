#####################
Urwid ComboBox Widget
#####################

A ComboBox like widget for urwid.


Install
=======

As usual, run `python setup.py install`.


Using
=====

Just create a ComboBox instance using the list of items you want to show:

    from urwid_combobox import ComboBox
    import urwid

    combobox = ComboBox(["Item1", "Item2"])
    fill = urwid.Filler(urwid.Padding(combobox, 'center', 15))
    loop = urwid.MainLoop(fill, [('popbg', 'white', 'dark blue')], pop_ups=True)
    loop.run()

This looks like a button. The button label is set to the first item of the
input list. When activated, the button is replaced with a popup containing a
list of CheckButton instances, one for each item. When an item is activated the
button label is set to the new selection, the popup is closed and the button
with the new label is visible again.


Testing
=======

See `urwid_combobox/tests.py`.


License
=======

Released under the MIT license.

