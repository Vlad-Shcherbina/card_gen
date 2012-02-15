'Usage: %prog [options] order1.txt [order2.txt...]'

from optparse import OptionParser
import os

import metalang
from unformat import unformat


html_template = '''
<!--<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">-->
<html>
<head>
<link rel="stylesheet" type="text/css" href="../styles/{style}.css">
</head>

<body>
{body}

<script language="javascript" src="../checkOverflow.js"></script>
</body>
'''

front_page_template = '''
<div class="front">
{0}
</div>
'''

back_page_template = '''
<div class="back">
{0}
</div>
'''


def process_order_file(order_file):
    order_name, _ = os.path.splitext(order_file)
    print order_name
    order_file = open(order_file)
    per_page, cat = next(order_file).split()
    per_page = int(per_page)

    template = open('templates/{0}.txt'.format(cat)).read().strip()
    front_template = open('templates/{0}_front.html'.format(cat)).read()
    back_template = open('templates/{0}_back.html'.format(cat)).read()

    cards = []

    for item in order_file:
        card, count = item.split()
        count = int(count)
        if options.once:
            count = 1
        print ' ', card, count

        card_text = open(card).read().strip()
        card_slots = unformat(template, card_text)

        for i in range(count):
            instantiated_card_slots = \
                dict((k, metalang.process(v)) for k, v in card_slots.items())
            cards.append((
                front_template.format(**instantiated_card_slots),
                back_template.format(**instantiated_card_slots)
                ))

    result_front = ''
    result_back = ''
    for i in range(0, len(cards), per_page):
        front_page = ''
        back_page = ''
        for front, back in cards[i:i+per_page]:
            front_page += front
            back_page += back
        result_front += front_page_template.format(front_page)
        result_back += back_page_template.format(back_page)

    result_front = html_template.format(style=cat, body=result_front)
    result_back = html_template.format(style=cat, body=result_back)

    with open('results/{0}_front.html'.format(order_name), 'w') as fout:
        fout.write(result_front)
    with open('results/{0}_back.html'.format(order_name), 'w') as fout:
        fout.write(result_back)


def main():
    global options
    parser = OptionParser(usage=__doc__)
    parser.add_option(
        '-o', '--once', 
        action='store_true', default=False,
        help='Generate only one instance of each card')

    options, args = parser.parse_args()
    
    if len(args) < 1:
        parser.error('Order file is not specified')

    if not os.path.exists('results'):
        os.makedirs('results')

    map(process_order_file, args)


if __name__ == '__main__':
    main()