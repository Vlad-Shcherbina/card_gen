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


default_env = Environment()


def process(s, env=default_env):
    def repl(m):
        if os.path.exists(m.group(1)):
            items = open(m.group(1)).readlines()
            items = filter(None, items)
        else:
            items = m.group(1).split('|')
        result = env.random.choice(items)
        return replacements.get(result, result)

    return re.sub(r'\{([^\}]+)\}', repl, s)