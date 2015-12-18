#!/usr/bin/env python3.4

import argparse
import sys
import os

categories = {
    'Basic Pkmn':               1,
    'Stage 1 Pkmn':             2,
    'Stage 2 Pkmn':             3,
    'Mega Evolution':           4,
    'Restored Pkmn':            5,
    'BREAK Pkmn':               6,
    'Item':                     7,
    'Supporter':                8,
    'Stadium':                  9,
    'Tool':                     10,
    'Technical Machine':        11,
    'Basic Energy':             12,
    'Special Energy':           13,
}

sets = {
    'XY':                       59,
    'Flashfire':                60,
    'Furious Fists':            61,
    'Phantom Forces':           62,
    'Primal Clash':             63,
    'Double Crisis':            64,
    'Roaring Skies':            65,
    'Ancient Origins':          66,
    'BREAKthrough':             67,

    'Kalos Starter':            1006,
    'McDonald\'s 2014':         3004,
    'XY Trainer Kit':           4006,
    'XY Promos':                5006,
}

standard = [
    'XY',
    'Flashfire',
    'Furious Fists',
    'Phantom Forces',
    'Primal Clash',
    'Double Crisis',
    'Roaring Skies',
    'Ancient Origins',
    'BREAKthrough',
    'Kalos Starter',
    'McDonals\'s 2014',
    'XY Trainer Kit',
    'XY Promos',
]


normal_basic_pkmn = [
    'litleo',
    'entei',
    'honedge',
    'spinarak',
    'swirlix',
]

ex_pkmn = [
    'shaymin ex',
]

basic_pkmn = [
    normal_basic_pkmn,
    ex_pkmn,
]

stage_1_pkmn = [
    'pyroar',
    'doublade',
    'aradios',
    'slurpuff'
]

supporters = [
    'processor sycamore',
    'wally',
    'lysandre',
    'blacksmith',
    'tierno',
    'skyla',
]

items = [
    'vs seeker',
    'battle compressor',
    'fiery torch',
    'acro bike',
    'ultra ball',
    'level ball',
    'repeat ball',
    'evosoda',
    'roller skates',
    'professor\'s letter',
    'paint roller',
    'red card',
    'sacred ash',
]

tools = [
    'float stone',
    'hard charm',
    'muscle band',
    'trick coin',
]

basic_energy = [
    'electric energy',
    'psychic energy',
    'fairy energy',
    'dark energy',
    'fighting energy',
    'fire energy',
    'water energy',
    'grass energy',
    'metal energy',
]

special_energy = [
    'double colorless energy',
]


def search_card_by_name(name):
    # if name in cards:
    #     Pokemon('basic', name, 'set_name', 'set_id')
    pass


class Card():
    def __init__(self, name, set_name, set_id, definition, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = name.lower() + ' - ' + set_name.lower() + ' - ' + set_id.lower()
        self.name = name
        self.set_name = set_name
        self.set_id = set_id
        self.definition = definition


class CardAttributeException(Exception):
    pass


class CardDefinition(dict):
    def __init__(self, major_type, *args, **kwargs):
        # We filter OUT all of the attributes from args, and pass them to super()
        super().__init__(filter(lambda x: not isinstance(x, Attribute), args), **kwargs)
        self.major_type = major_type
        # This time, we single out ONLY the attributes, and add them to ourself
        self.add(*filter(lambda x: isinstance(x, Attribute), args))

    def add(self, *attrs):
        for attr in attrs:
            if attr.classifier not in self:
                self[attr.classifier] = attr
            else:
                raise CardAttributeException('Attribute \'{0}\' is already defined'.format(attr.classifier))

    def remove(self, *attrs):
        for attr in attrs:
            if attr.classifier in self:
                del self[attr.classifier]


class Attribute():
    def __init__(self, classifier, *args, **kwargs):
        self.classifier = classifier
        self.args = args
        self.kwargs = kwargs


# Common Attributes
BASIC = Attribute('basic')
STAGE_1 = Attribute('stage_1')
STAGE_2 = Attribute('stage_2')
EX = Attribute('pokemon ex')

ITEM = Attribute('item')
TOOL = Attribute('tool')
STADIUM = Attribute('stadium')
SUPPORTER = Attribute('supporter')

FIRE = Attribute('type', 'fire')
WATER = Attribute('type', 'water')
LIGHTNING = Attribute('type', 'lightning')
GRASS = Attribute('type', 'grass')
FIGHTING = Attribute('type', 'fighting')
PSYCHIC = Attribute('type', 'psychic')
METAL = Attribute('type', 'metal')
DARK = Attribute('type', 'dark')
FAIRY = Attribute('type', 'fairy')
COLORLESS = Attribute('type', 'colorless')
DRAGON = Attribute('type', 'dragon')


class CardList(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add(self, card):
        self[card.id] = self.get(card.id, 0) + 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='pk - A Python based tool for pokemon card statistics')
    parser.add_argument(dest='deck_files', metavar='DECK', nargs='+',
                        help='File location(s) for a pokemon card deck')
    parser.add_argument('-x', '--x_var', dest='x_var', action='store_true',
                        help='Stores x_var to true (default=false)')
    args = parser.parse_args()

    print(args.x_var)
    print(args.deck_files)

    for deck_file in args.deck_files:
        if not os.path.isfile(deck_file):
            print('Error: {0} was not found'.format(deck_file))
            sys.exit(1)

    # for deck_file in args.deck_files:

    defs = {}
    cards = {}

    defs['entei'] = CardDefinition('pokemon', BASIC, FIRE)
    c = Card('Entei', 'Ancient Origins', '15/98', defs['entei'])
    defs['litleo'] = CardDefinition('pokemon', BASIC, FIRE)
    c = Card('Litleo', 'Flashfire', '18/106', defs['litleo'])
    defs['pyroar'] = CardDefinition('pokemon', STAGE_1, FIRE)
    c = Card('Pyroar', 'Flashfire', '20/106', defs['pyroar'])
    defs['shaymin-ex'] = CardDefinition('pokemon', BASIC, EX, COLORLESS)
    c = Card('Shaymin EX', 'Roaring Skies', '77/108', defs['shaymin-ex'])

    defs['sycamore'] = CardDefinition('trainer', SUPPORTER)
    c = Card('Professor Sycamore', 'Phantom Forces', '101/119', defs['sycamore'])
    c = Card('Professor Sycamore', 'XY', '122/146', defs['sycamore'])
    defs['wally'] = CardDefinition('trainer', SUPPORTER)
    c = Card('Wally', 'Roaring Skies', '94/108', defs['wally'])
    c = Card('Wally', 'Roaring Skies', '107/108', defs['wally'])
    defs['lysandre'] = CardDefinition('trainer', SUPPORTER)
    c = Card('Lysandre', 'Ancient Origins', '78/98', defs['lysandre'])
    c = Card('Lysandre', 'Flashfire', '90/106', defs['lysandre'])
    c = Card('Lysandre', 'Flashfire', '104/106', defs['lysandre'])
    defs['blacksmith'] = CardDefinition('trainer', SUPPORTER)
    c = Card('Blacksmith', 'Flashfire', '88/106', defs['blacksmith'])

    cards[c.id] = c
    print(c)
    print(c.name)
    print(c.id)
    print(c.definition.keys())
    print(c.definition['type'].args)
    defs['litleo'].add(EX)
    print(c.definition.keys())
    defs['litleo'].remove(EX)
    print(c.definition.keys())

    sys.exit(0)
