#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

voices_lst = ['Daniel', 'Chris', 'Jake- Smart, Formal, Confident', 'Sarah',
                  'New York Nick - Modern NYC Wiseguy', 'Eric', 'Alice', 'Callum',
                  'Olivier Calm', 'Liam', 'Laura', 'Jake - Smart, Formal, Confident',
                   'Will', 'Natasha - Valley girl', 'Sonia', 'Charlotte', 'Jessica',
                   'Frederick - Old Gnarly Narrator', 'George', 'Matilda',
                    'Charlie', 'Bill', 'Brian', 'Maya', 'Lily', 'Hugo']
if __name__ == '__main__':
    from my.text2speech import fart_and_apologize
    if len(sys.argv) == 1 or sys.argv[1] not in voices_lst:
        print("Options:", voices_lst)
        sys.exit(1)

    fart_and_apologize(sys.argv[1])





