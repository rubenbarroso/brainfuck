# (c) Ruben Barroso Dec 2011 - ruben.bm@gmail.com

# Take control of your boredom - Program your own Brainfuck interpreter!
import sys

class Brainfuck:
    """
    Brainfuck Spec
    --------------
    30k cells (bytes initialized to 0)
    Data pointer to a specific cell
    Only eight operators:
      < move data pointer one cell left
      > move data pointer one cell right
      + increment the cell at the current data pointer
      - decrement the cell at the current data pointer
      . output the cell at the current data pointer as a character
      , input the next character to the cell at the current data pointer
      [ if the cell at the current data pointer is zero, move the instruction pointer to the matching ]
      ] move the instruction pointer to the matching [

    Ignore characters other than +-.,[]<>
    Advance instruction pointer after each instruction
    A program halts by running off its end
    """

    def __init__(self):
        self.cells = [0] * 30000
        self.data_pointer = 0

    def _tokenize(self, str, level=0):
        tokens = []
        while len(str) > 0:
            token = str.pop(0)
            if token == '[':
                tokens.append(self._tokenize(str, level + 1))
            elif token == ']':
                return tokens
            else:
                tokens.append(token)
        if level is not 0:
            raise SyntaxError('Malformed expression')
        return tokens

    def eval(self, src):
        """ Iterative evaluator """
        self._eval(self._tokenize(list(src)))

    def _eval(self, program):
        # the program counter
        pc = 0

        while pc < len(program):
            # current operation
            op = program[pc]

            if op == '+':
                self.cells[self.data_pointer] += 1
            elif op == '-':
                self.cells[self.data_pointer] -= 1
            elif op == '>':
                self.data_pointer += 1
            elif op == '<':
                self.data_pointer -= 1
            elif op == '.':
                print chr(self.cells[self.data_pointer]),
            elif op == ',':
                self.cells[self.data_pointer] = ord(sys.stdin.read(1))
            elif isinstance(op, list):
                if self.cells[self.data_pointer]:
                    self._eval(op)
                    # retry the loop again
                    pc -= 1
            else:
                raise SyntaxError("Unrecognized operator '" + op + "' at position ", pc)

            # always advance, as specified
            pc += 1
