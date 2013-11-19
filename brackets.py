import unittest
import math


OPENING_CHARS = '[<({'
CLOSING_CHARS = ']>)}'
CHARS_CLOSE_OPEN_PAIRING = {
    ']': '[',
    '>': '<',
    ')': '(',
    '}': '{',
}
WILDCARD_CHARS = ' |'


def is_balanced(expression):
    '''
    Verifies if the expression (containing only brackets) is balanced.

    - The expression may contain only brackets and/or wildcard characters.
    - By definition, all opening brackets must have a closing pair.
    - A wildcard is a special kind of bracket, where it may be opening or closing an expression depending on the context.
    - It's allowed to have an unclosed wildcard if it's in the middle of the expression.
    '''

    stack = list()

    # if expression length is odd, then we have a
    # char in the middle. hopefully it's a wildcard
    if len(expression) % 2 is not 0:
        middle_index = int(math.floor(len(expression)/2))
        if expression[middle_index] in WILDCARD_CHARS:
            # now the expression has an even length
            expression = expression[:middle_index] + expression[middle_index+1:]
        else:
            return False

    for char in expression:
        if char not in OPENING_CHARS and char not in CLOSING_CHARS and char not in WILDCARD_CHARS:
            return False
        elif char in WILDCARD_CHARS:
            if stack and char is stack[-1]:
                stack.pop()
            else:
                stack.append(char)
        elif char in OPENING_CHARS:
            stack.append(char)
        elif CHARS_CLOSE_OPEN_PAIRING[char] is not stack.pop():
            return False

    return False if stack else True


'''
Unit Tests
'''


class MatchingBracketsTest(unittest.TestCase):
    
    def test_empty_expression_is_valid(self):
        self.assertTrue(is_balanced(''))

    def test_expresison_is_invalid_if_char_not_allowed(self):
        self.assertFalse(is_balanced('aa'))

    def test_square_and_angle_and_parenthesis_and_curly_brackers_must_be_valid(self):
        self.assertTrue(is_balanced('[]'))
        self.assertTrue(is_balanced('<>'))
        self.assertTrue(is_balanced('()'))
        self.assertTrue(is_balanced('{}'))

    def test_nested_brackets_must_be_valid(self):
        self.assertTrue(is_balanced('{<([])>}'))

    def test_sibling_brackets_must_be_valid(self):
        self.assertTrue(is_balanced('{<([])>}[(<{}>)]'))

    def test_sibling_brackets_must_be_valid_when_wraped(self):
        self.assertTrue(is_balanced('{<{<([])>}[(<{}>)]>}'))

    def test_wildcard_character_must_be_accepted(self):
        self.assertTrue(is_balanced('||'))
        self.assertTrue(is_balanced('<||>'))
        self.assertTrue(is_balanced('<  >'))
        self.assertTrue(is_balanced(' |  {}  | '))

    def test_wildcard_character_must_be_valid_if_in_the_middle(self):
        self.assertTrue(is_balanced('|'))
        self.assertTrue(is_balanced('{ }'))

    def test_expression_must_be_invalid_when_there_is_no_closing_brackets(self):
        self.assertFalse(is_balanced('<({['))

    def test_expression_must_be_invalid_when_there_is_unmatching_wildcards(self):
        self.assertFalse(is_balanced('|<||>'))


if __name__ == '__main__':
    unittest.main()
