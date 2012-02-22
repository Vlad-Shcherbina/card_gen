import re
import random
import os


# dirty shit
replacements = {}
for line in open('replacements.txt'):
    a, b = line.split()
    replacements[a] = b


class Environment(object):
    def __init__(self):
        self.random = random.Random(123)
        self.unique_codes = {}


default_env = Environment()


def process(s, env=default_env):
    def repl(m):
        m = m.group(1)

        unique = False
        u = 'unique '
        if m.startswith(u):
            m = m[len(u):]
            unique = True

        if os.path.exists(m):
            items = open(m).readlines()
            items = filter(None, items)
        else:
            items = m.split('|')

        if unique:
            items = tuple(items)
            if m not in env.unique_codes:
                env.unique_codes[m] = 0
            result = items[env.unique_codes[m]]
            env.unique_codes[m] += 1
        else:
            result = env.random.choice(items)

        return replacements.get(result, result)

    return re.sub(r'\{([^\}]+)\}', repl, s)