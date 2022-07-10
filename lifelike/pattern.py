import numpy as np
import requests
import re


class Pattern:
    def __init__(self, name):
        self.name = name

        self.x = None
        self.y = None
        self.rule = None
        self.rle = None

        self._retrieve_data()

        self.U = None

        self._rldecode()

    def _retrieve_data(self):
        response = requests.get(f'https://www.conwaylife.com/patterns/{self.name}.rle')

        rlencoded = re.sub(
            r'(?m)^#.*\n?',
            '',
            response.content.decode('utf-8')
        )

        matches = re.match(
            r'(?s)x = (.*), y = (.*), rule = (.*?)\r\n(.*!)',
            rlencoded
        )

        x, y, rule, rle = matches.groups()
        self.x = int(x)
        self.y = int(y)
        self.rule = rule
        self.rle = rle.replace('\r\n', '')

    def _rldecode(self):
        U = np.zeros((self.y, self.x))

        row = 0
        column = 0
        number = ''
        for c in self.rle:
            if c == 'o':
                if number != '':
                    for _ in range(int(number)):
                        U[row, column] = 1
                        column += 1
                else:
                    U[row, column] = 1
                    column += 1
                number = ''
            elif c == 'b':
                column += 1 if number == '' else int(number)
                number = ''
            elif c.isnumeric():
                number += c
            elif c == '$' or c == '!':
                row += 1 if number == '' else int(number)
                column = 0
                number = ''

        self.U = U

    def __repr__(self):
        out = ''
        for row in self.U:
            for elem in row:
                out += '@' if elem==1 else ' '
            out += '\n'

        return out
