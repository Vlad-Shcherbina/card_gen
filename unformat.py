import re

"""
Template is a string containing '{name}' fragments.
Result is a dictionary matching 'name' with corresponding fragment
of input string.
"""
def unformat(template, s):
    special = '***SPECIAL***{0}***SPECIAL***'
    template = special.format(template)
    s = special.format(s)

    bindings = {}
    parts = re.split(r'\{(\w+)\}', template)
    pos = 0
    for i in range(0, len(parts), 2):
        new_pos = s.find(parts[i], pos)
        assert new_pos != -1
        if i == 0:
            assert new_pos == 0
        else:
            bindings[parts[i-1]] = s[pos:new_pos]
        pos = new_pos+len(parts[i])
    assert pos == len(s)
    assert template.format(**bindings) == s
    return bindings


def unformat_re(template, s):
    parts = re.split(r'\{(\w+)\}', template)
    regex = ''
    for i, part in enumerate(parts):
        if i%2 == 0:
            regex += re.escape(part)
        else:
            regex += r'(?P<{}>.*)'.format(part)
    regex += '$'
    m = re.match(regex, s, re.DOTALL) # dotall to match newlines
    return m.groupdict()


if __name__ == '__main__':
    for u in [unformat, unformat_re]:
        assert u('{x} {y}', 'hello world') == dict(x='hello', y='world')
        template = \
'''{x}
---
{y}'''
        s = \
'''hello
asdf
---
world'''
        print u(template, s)