# -*- coding: utf-8 -*-

from gustav_forms import qt_ClosedSet as theForm

choices = [ ['Bill', 'Joe',  'Ruth', 'Rick',  'Kate', 'Mike', 'Jack', 'Ned',  'Tom',  'Lynn'],
            ['took', 'gave', 'lost', 'found', 'had',  'bought', 'sold', 'saw', 'got', 'brought'],
            ['no',  'two',  'three', 'four', 'five', 'six',  'eight', 'nine', 'ten', 'twelve'],
            ['red', 'blue', 'green', 'brown', 'gray', 'black', 'white', 'beige', 'tan', 'dark'],
            ['clips', 'pens', 'cards', 'toys', 'wires', 'gloves', 'hats', 'socks', 'blocks', 'tops']
           ]

interface = theForm.Interface(choices)
resp = interface.get_resp("What?")
print(resp)

