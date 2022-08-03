"""Humre
By Al Sweigart al@inventwithpython.com

A human-readable regular expression module for Python."""


# TODO - Add atomic grouping ((?>...)) and possessive quantifiers (*+, ++, ?+, {m,n}+) new in python 3.11
# TODO - Add a warning if they are called from older versions of Python.

import re
from typing import ParamSpecArgs

__version__ = '0.1.0'

digit = r'\d'
word = r'\w'
whitespace = r'\s'
nondecimal = r'\D'
nonword = r'\W'
nonwhitespace = r'\S'

boundary = r'\b'
IGNORE_DIRECTIVE = '(?i)'


# Constants copied from the re module:
# Changed in version 3.6: Flag constants are now instances of RegexFlag, which is a subclass of enum.IntFlag.
A = re.A
ASCII = re.ASCII
DEBUG = re.DEBUG
I = re.I
IGNORECASE = re.IGNORECASE
L = re.L
LOCALE = re.LOCALE
M = re.M
MULTILINE = re.MULTILINE
S = re.S
DOTALL = re.DOTALL
X = re.X
VERBOSE = re.VERBOSE

# Custom character classes
# NOTE: ord('À') == 192, ord('ÿ') == 255
letter = '[A-zÀ-ÿ]'
nonletter = '[^A-zÀ-ÿ]'
uppercase = '[A-ZÀ-Ÿ]'
nonuppercase = '[^A-ZÀ-Ÿ]'
lowercase = '[a-zà-ÿ]'
nonlowercase = '[^a-zà-ÿ]'
alphanumeric = '[A-zÀ-ÿ0-9]'
nonalphanumeric = '[^A-zÀ-ÿ0-9]'
number = r'(?:+|-)?(?:\d{1:3}(?:,\d{3})*)|(?:\d)+(?:\.\d+)'  # 1,200.3456789
euro_number = r'(?:+|-)?(?:\d{1:3}(?:\.\d{3})*)|(?:\d)+(?:,\d+)'
hexadecimal = '[0-9A-f]'
nonhexadecimal = '[^0-9A-f]'

# TODO - I'm still not sure about these names:
anything = '.*?'
everything = '.*'
greedy_something = '.+'
something = '.+?'
anychar = '.'


# labels for escaped regex metacharacters: . ^ $ * + ? { } [ ] \ | ( )
# This full list copied from https://docs.python.org/3/howto/regex.html
period = r'\.'
caret = r'\^'
dollar_sign = r'\$'
asterisk = r'\*'
plus_sign = r'\+'
question_mark = r'\?'
open_brace = r'\{'
close_brace = r'\}'
open_bracket = r'\['
close_bracket = r'\]'
backslash = r'\\'
pipe = r'\|'
open_paren = open_parenthesis = r'\('
close_paren = close_parenthesis = r'\)'

newline = r'\n'  # TODO - double check this: do I want r'\n' or '\n' here?
tab = r'\t'
quote = r"\'"
double_quote = r'\"'


def esc(*listOfRegexStrs):  # type: (str) -> str
    r"""A wrapper for re.escape(). Escape special characters in the strings
    in listOfRegexStrs.

    >>> from humre import *
    >>> esc('!#$%&')
    '!\\#\\$%\\&'

    >>> import re
    >>> re.escape('!#$%&') == esc('!#$%&')
    True
    """
    return re.escape(''.join(listOfRegexStrs))


def compile(*listOfRegexStrs, flags=0):  # TODO fix type hint
    """A wrapper for re.compile(). This passes the strings in listOfRegexStrs
    as a single concatenated string to re.compile(). All other arguments to
    re.compile() must be passed to the flags keyword argument.

    >>> from humre import *
    >>> patternObj = compile('[a-z]+', flags=IGNORECASE)
    >>> patternObj.search('Hello')
    <re.Match object; span=(0, 5), match='Hello'>
    """
    return re.compile(''.join(listOfRegexStrs), flags=flags)


def group(*listOfRegexStrs):  # type: (str) -> str
    """Returns a string in the regex sytax for a regex group surrounded by
    parentheses of the regex strings in listOfRegexStrs.

    >>> from humre import *
    >>> group('cat')
    '(cat)'
    >>> group('cat', 'dog', 'moose')
    '(catdogmoose)'
    >>> group('catdogmoose')
    '(catdogmoose)'
    >>> group('cat', group('dog'), group('moose'))
    '(cat(dog)(moose))'
    """
    return '(' + ''.join(listOfRegexStrs) + ')'


def positive_lookahead(*listOfRegexStrs):  # type: (str) -> str
    """Returns a string in the regex syntax for a positive lookahead
    assertion of the regex strings in listOfRegexStrs. A lookahead matches
    text but does not consume it in the original parsed text.

    In the following example, 'kitty' is matched but only if 'cat' follows
    'kitty'. Note that the match only includes 'kitty' and not 'kittycat'.

    >>> from humre import *
    >>> 'kitty' + positive_lookahead('cat')
    'kitty(?=cat)'
    >>> compile('kitty' + positive_lookahead('cat')).search('kitty') == None
    True
    >>> compile('kitty' + positive_lookahead('cat')).search('kittycat')
    <re.Match object; span=(0, 5), match='kitty'>
    """
    return '(?=' + ''.join(listOfRegexStrs) + ')'


def negative_lookahead(*listOfRegexStrs):  # type: (str) -> str
    """Returns a string in the regex syntax for a negative lookahead
    assertion of the regex strings in listOfRegexStrs. A lookahead matches
    text but does not consume it in the original parsed text.

    In the following example, 'kitty' is matched but only if the 'cat'
    does not follow 'kitty'. Note that the match only includes 'kitty' and
    not 'kittycat'.

    >>> from humre import *
    >>> 'kitty' + negative_lookahead('cat')
    'kitty(?!cat)'
    >>> compile('kitty' + negative_lookahead('cat')).search('kitty')
    <re.Match object; span=(0, 5), match='kitty'>
    >>> compile('kitty' + negative_lookahead('cat')).search('kittycat') == None
    True
    """
    return '(?!' + ''.join(listOfRegexStrs) + ')'


def positive_lookbehind(*listOfRegexStrs):  # type: (str) -> str
    """Returns a string in the regex syntax for a positive lookbehind
    assertion of the regex strings in listOfRegexStrs. A lookbehind
    matches text but does not consume it
    in the original parsed text.

    In the following example, 'cat' is matched but only if 'kitty' is before
    'cat'. Note that the match only includes 'cat' and not 'kittycat'.

    >>> from humre import *
    >>> positive_lookbehind('kitty') + 'cat'
    '(?<=kitty)cat'
    >>> compile(positive_lookbehind('kitty') + 'cat').search('kittycat')
    <re.Match object; span=(5, 8), match='cat'>
    >>> compile(positive_lookbehind('kitty') + 'cat').search('cat') == None
    True
    """
    return '(?<=' + ''.join(listOfRegexStrs) + ')'


def negative_lookbehind(*listOfRegexStrs):  # type: (str) -> str
    """Returns a string in a negative lookbehind assertion of the regex
    strings in listOfRegexStrs. A lookbehind matches text but does not
    consume it in the original parsed text.

    In the following example, 'cat' is matched but only if 'kitty' is not
    before 'cat'. Note that the match only includes 'cat' and not 'kittycat'.

    >>> from humre import *
    >>> negative_lookbehind('kitty') + 'cat'
    '(?<!kitty)cat'
    >>> compile(negative_lookbehind('kitty') + 'cat').search('kittycat') == None
    True
    >>> compile(negative_lookbehind('kitty') + 'cat').search('black cat')
    <re.Match object; span=(6, 9), match='cat'>
    """
    return '(?<!' + ''.join(listOfRegexStrs) + ')'


def named_group(name, *listOfRegexStrs):  # type: (str, str) -> str
    r"""Returns a string in the regex syntax for a named group of the regex
    strings in listOfRegexStrs.

    Named groups can be referred to by their name rather than their
    group number.

    >>> from humre import *
    >>> named_group('group_name', 'pattern_to_look_for')
    '(?P<group_name>pattern_to_look_for)'
    >>> named_group('pobox', 'PO BOX \d{3:5}')
    '(?P<pobox>PO BOX \\d{3:5})'
    """
    if re.match(r'\w+', name) is None or re.match(r'^\d', name):
        raise ValueError('name must contain only letters, numbers, and underscore and not start with a number')
    return '(?P<' + str(name) + '>' + ''.join(listOfRegexStrs) + ')'


# TODO - is there a better name than this? noncapture()?
def noncapturing_group(*listOfRegexStrs):
    r"""Returns a string in the regex syntax for a noncapturing group of the
    regex strings in listOfRegexStrs.

    Noncapturing groups are not included in the groups field of a Pattern
    object. They are useful for when you want to group parts of a regex
    string together without affecting the numbered groups.

    >>> from humre import *
    >>> noncapturing_group('pattern_to_look_for')
    '(?:pattern_to_look_for)'
    """
    return '(?:' + ''.join(listOfRegexStrs) + ')'


def optional(*listOfRegexStrs):  # type: (str) -> str
    r"""Returns a string in the regex syntax for an optional part of the
    pattern of the regex strings in listOfRegexStrs.

    >>> from humre import *
    >>> optional('a')
    'a?'
    >>> optional(group('spam'))
    '(spam)?'
    """
    regexStr = ''.join(listOfRegexStrs)
    if regexStr == '':
        raise ValueError('listOfRegexStrs must have at least one nonblank value')
    return regexStr + '?'


def either(*listOfRegexStrs):
    # TODO - it's going to be really easy to get this wrong when people pass multiple comma-separated arguments when they intended to pass fewer string arguments in. How do we avoid this problem?
    r"""Returns a string in the regex syntax for the alternation or "or"
    operator of the regex strings in listOfRegexStrs. This matches one of
    the strings in listOfRegexStrs.

    >>> from humre import *
    >>> either(group('cat'), group('dog'), group('moose'))
    '(cat)|(dog)|(moose)'
    """
    listOfRegexStrs = [s for s in listOfRegexStrs if s != '']
    if len(listOfRegexStrs) == 0:
        raise ValueError('listOfRegexStrs must have at least one nonblank value')
    return '|'.join(listOfRegexStrs)


def exactly(quantity, *listOfRegexStrs):  # type: (int, str) -> str
    r"""Returns a string in the regex syntax for matching an exact number
    of occurrences of the regex strings in listOfRegexStrs.

    >>> from humre import *
    >>> exactly(3, 'a')
    'a{3}'
    >>> compile(exactly(3, 'a')).search('aaaaah!')
    <re.Match object; span=(0, 3), match='aaa'>
    """
    if not isinstance(quantity, int):
        raise TypeError('quantity must be a positive int')
    if quantity < 0:
        raise ValueError('quantity must be a positive int')
    regexStr = ''.join(listOfRegexStrs)
    if regexStr == '':
        raise ValueError('listOfRegexStrs must have at least one nonblank value')
    return regexStr + '{' + str(quantity) + '}'


def between(minimum, maximum, *listOfRegexStrs):  # type: (int, int, str) -> str
    r"""Returns a string in the regex syntax for matching an between the
    minimum and maximum number of occurrences of the regex strings in
    listOfRegexStrs.

    >>> from humre import *
    >>> between(3, 5, 'a')
    'a{3,5}'
    >>> compile(between(3, 5, 'a')).search('aah!') == None
    True
    >>> compile(between(3, 5, 'a')).search('aaaah!')
    <re.Match object; span=(0, 4), match='aaaa'>
    >>> compile(between(3, 5, group('ha'))).search('hahahaha!')
    <re.Match object; span=(0, 8), match='hahahaha'>
    """
    if not isinstance(minimum, int):
        raise TypeError('minimum must be a positive int')
    if minimum < 0:
        raise ValueError('minimum must be a positive int')
    if not isinstance(maximum, int):
        raise TypeError('maximum must be a positive int')
    if maximum < 0:
        raise ValueError('maximum must be a positive int')
    if minimum > maximum:
        raise ValueError('minimum greater than maximum')
    regexStr = ''.join(listOfRegexStrs)
    if regexStr == '':
        raise ValueError('listOfRegexStrs must have at least one nonblank value')
    return regexStr + '{' + str(minimum) + ',' + str(maximum) + '}'


def at_least(minimum, *listOfRegexStrs):  # type: (int, str) -> str
    r"""Returns a string in the regex syntax for matching a minimum number
    of occurrences of the regex strings in listOfRegexStrs.

    >>> from humre import *
    >>> at_least(3, 'A')
    'A{3,}'
    >>> compile(at_least(3, 'A')).search('Rated AAAAA+')
    <re.Match object; span=(6, 11), match='AAAAA'>
    """
    if not isinstance(minimum, int):
        raise TypeError('minimum must be a positive int')
    if minimum < 0:
        raise ValueError('minimum must be a positive int')
    regexStr = ''.join(listOfRegexStrs)
    if regexStr == '':
        raise ValueError('listOfRegexStrs must have at least one nonblank value')
    return regexStr + '{' + str(minimum) + ',}'


def at_most(maximum, *listOfRegexStrs):  # type: (int, str) -> str
    r"""Returns a string in the regex syntax for matching a maximum number
    of occurrences of the regex strings in listOfRegexStrs.

    >>> from humre import *
    >>> at_most(3, 'A')
    'A{,3}'
    >>> compile('A{,3}').search('AAAAA+')
    <re.Match object; span=(0, 3), match='AAA'>
    """
    if not isinstance(maximum, int):
        raise TypeError('maximum must be a positive int')
    if maximum < 0:
        raise ValueError('maximum must be a positive int')
    regexStr = ''.join(listOfRegexStrs)
    if regexStr == '':
        raise ValueError('listOfRegexStrs must have at least one nonblank value')
    return regexStr + '{,' + str(maximum) + '}'


def zero_or_more(*listOfRegexStrs):  # type: (str) -> str
    r"""Returns a string in the regex syntax for matching zero or more
    occurrences of the regex strings in listOfRegexStrs. This does a
    greedy match, which tries to make the largest match possible.

    >>> from humre import *
    >>> compile(zero_or_more('A')).search('AAAAA')
    <re.Match object; span=(0, 5), match='AAAAA'>
    >>> compile(zero_or_more('A')).search('Blah blah blah')
    <re.Match object; span=(0, 0), match=''>
    """
    regexStr = ''.join(listOfRegexStrs)
    if regexStr == '':
        raise ValueError('listOfRegexStrs must have at least one nonblank value')
    return ''.join(listOfRegexStrs) + '*'


def zero_or_more_lazy(*listOfRegexStrs):  # type: (str) -> str
    r"""Returns a string in the regex syntax for matching zero or more
    occurrences of the regex strings in listOfRegexStrs. This does a
    lazy match, which tries to make the smallest match possible.

    >>> from humre import *

    """
    regexStr = ''.join(listOfRegexStrs)
    if regexStr == '':
        raise ValueError('listOfRegexStrs must have at least one nonblank value')
    return regexStr + '*?'


def one_or_more(*listOfRegexStrs):  # type: (str) -> str
    regexStr = ''.join(listOfRegexStrs)
    if regexStr == '':
        raise ValueError('listOfRegexStrs must have at least one nonblank value')
    return regexStr + '+'


def one_or_more_lazy(*listOfRegexStrs):  # type: (str) -> str
    r"""Returns a string in the regex syntax for matching one or more
    occurrences of the regex strings in listOfRegexStrs. This does a
    lazy match, which tries to make the smallest match possible.

    >>> from humre import *

    """
    regexStr = ''.join(listOfRegexStrs)
    if regexStr == '':
        raise ValueError('listOfRegexStrs must have at least one nonblank value')
    return regexStr + '+?'


def starts_with(*listOfRegexStrs):  # type: (str) -> str
    return '^' + ''.join(listOfRegexStrs)


def ends_with(*listOfRegexStrs):  # type: (str) -> str
    return ''.join(listOfRegexStrs) + '$'


def starts_and_ends_with(*listOfRegexStrs):  # type: (str) -> str
    return '^' + ''.join(listOfRegexStrs) + '$'


def chars(*listOfRegexStrs):  # type: (str) -> str
    regexStr = ''.join(listOfRegexStrs)
    if regexStr == '':
        raise ValueError('listOfRegexStrs must have at least one nonblank value')
    return '[' + regexStr + ']'


def nonchars(*listOfRegexStrs):  # type: (str) -> str
    regexStr = ''.join(listOfRegexStrs)
    if regexStr == '':
        raise ValueError('listOfRegexStrs must have at least one nonblank value')
    return '[^' + regexStr + ']'


# TODO - should I have these group_*() functions? It does help cut down on the parentheses hell.
def optional_group(*listOfRegexStrs):  # type: (str) -> str
    return '(' + ''.join(listOfRegexStrs) + ')?'


def group_either(*listOfRegexStrs):
    listOfRegexStrs = [s for s in listOfRegexStrs if s != '']
    return '(' + '|'.join(listOfRegexStrs) + ')'


def group_exactly(quantity, *listOfRegexStrs):  # type: (int, str) -> str
    if not isinstance(quantity, int):
        raise TypeError('quantity must be a positive int')
    if quantity < 0:
        raise ValueError('quantity must be a positive int')

    return '(' + ''.join(listOfRegexStrs) + '){' + str(quantity) + '}'


def group_between(minimum, maximum, *listOfRegexStrs):  # type: (int, int, str) -> str
    if not isinstance(minimum, int):
        raise TypeError('minimum must be a positive int')
    if minimum < 0:
        raise ValueError('minimum must be a positive int')
    if not isinstance(maximum, int):
        raise TypeError('maximum must be a positive int')
    if maximum < 0:
        raise ValueError('maximum must be a positive int')
    if minimum > maximum:
        raise ValueError('minimum greater than maximum')

    return '(' + ''.join(listOfRegexStrs) + '){' + str(minimum) + ',' + str(maximum) + '}'


def group_at_least(minimum, *listOfRegexStrs):  # type: (int, str) -> str
    if not isinstance(minimum, int):
        raise TypeError('minimum must be a positive int')
    if minimum < 0:
        raise ValueError('minimum must be a positive int')

    return '(' + ''.join(listOfRegexStrs) + '){' + str(minimum) + ',}'


def group_at_most(maximum, *listOfRegexStrs):  # type: (int, str) -> str
    if not isinstance(maximum, int):
        raise TypeError('maximum must be a positive int')
    if maximum < 0:
        raise ValueError('maximum must be a positive int')

    return '(' + ''.join(listOfRegexStrs) + '){,' + str(maximum) + '}'


def zero_or_more_group(*listOfRegexStrs):  # type: (str) -> str
    return '(' + ''.join(listOfRegexStrs) + ')*'


def one_or_more_group(*listOfRegexStrs):  # type: (str) -> str
    return '(' + ''.join(listOfRegexStrs) + ')+'


def group_chars(*listOfRegexStrs):  # type: (str) -> str
    regexStr = ''.join(listOfRegexStrs)
    if regexStr == '':
        raise ValueError('listOfRegexStrs must have at least one nonblank value')
    return '([' + regexStr + '])'


def group_nonchars(*listOfRegexStrs):  # type: (str) -> str
    regexStr = ''.join(listOfRegexStrs)
    if regexStr == '':
        raise ValueError('listOfRegexStrs must have at least one nonblank value')
    return '([^' + regexStr + '])'


if __name__ == "__main__":
    import doctest

    doctest.testmod()

'''
# Testing string concatenation vs join() string method:

def group1(*listOfRegexStrs):  # type: (str) -> str
    return '(' + ''.join(listOfRegexStrs) + ')'
def group2(*listOfRegexStrs):  # type: (str) -> str
    return ''.join(['(', ''.join(listOfRegexStrs), ')'])
def group3(*listOfRegexStrs):  # type: (str) -> str
    return ''.join(['(', *listOfRegexStrs, ')'])
def group4(*listOfRegexStrs):  # type: (str) -> str
    return ''.join(('(', *listOfRegexStrs, ')'))
import timeit
print(timeit.timeit("group1('cat', 'dog')", globals=globals(), number=100000000))
print(timeit.timeit("group2('cat', 'dog')", globals=globals(), number=100000000))
print(timeit.timeit("group3('cat', 'dog')", globals=globals(), number=100000000))
print(timeit.timeit("group4('cat', 'dog')", globals=globals(), number=100000000))
print(timeit.timeit("group1('cat', 'dog', 'cat', 'dog', 'cat', 'dog', 'cat', 'dog', 'cat', 'dog')", globals=globals(), number=100000000))
print(timeit.timeit("group2('cat', 'dog', 'cat', 'dog', 'cat', 'dog', 'cat', 'dog', 'cat', 'dog')", globals=globals(), number=100000000))
print(timeit.timeit("group3('cat', 'dog', 'cat', 'dog', 'cat', 'dog', 'cat', 'dog', 'cat', 'dog')", globals=globals(), number=100000000))
print(timeit.timeit("group4('cat', 'dog', 'cat', 'dog', 'cat', 'dog', 'cat', 'dog', 'cat', 'dog')", globals=globals(), number=100000000))
# Times:
#32.36761399998795
#36.67457259999355
#34.13985800003866
#39.810779399995226
#49.031997100042645
#50.96271799999522
#53.6757457999629
#60.84193440002855
'''
