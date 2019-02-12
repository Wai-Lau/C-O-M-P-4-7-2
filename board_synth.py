from colorama import Fore, Back, Style
from copy import deepcopy
from re import findall
# coordinates are board[column][row]
# bottom left block is (A,0)

class BoardSynth:
    def copy(self, board):
        return deepcopy(board)

    def apply(self, board, *cards):
        # this could be something to take out if we don't need rollbacks
        board_original = self.copy(board)
        for c in cards:
            try:
                ds = self.dest(c)
                if ds and self.legal(board, ds):
                    for s in ds:
                        board[s[0]][s[1]] = s[2]
                else:
                    print("Illegal move: " + ' '.join(c))
                    board = board_original
                    return False
            except Exception as e:
                board = board_original
                print("Illegal move: " + ' '.join(c))
                print(e)
                return False
        return True

    def coord_to_dest(self, board, coords):
        col1, row1 = self.to_n(coords[0]), int(coords[1]) - 1
        col2, row2 = self.to_n(coords[2]), int(coords[3]) - 1
        sym1, sym2 = board[col1][row1], board[col2][row2]
        return ((col1, row1, sym1),(col2, row2, sym2))

    def apply_remove(self, board, ds):
        board_original = self.copy(board)
        try:
            if ds and self.legal_remove(board, ds):
                for s in ds:
                    board[s[0]][s[1]] = ''
            else:
                print('That card choice is invalid and cannot be recycled')
                board = board_original
                return False
        except Exception as e:
            board = board_original
            print('That card choice is not valid and cannot be recycled')
            return False
        return True

    def recycle(self, board, to_remove, to_apply, last_move):
        remove_ds = self.coord_to_dest(board, to_remove)
        last_ds = self.dest(last_move)
        if remove_ds == last_ds:
            print("Cannot recycle recently played move: " + ' '.join(to_remove))
            return False
        apply_ds = self.dest(to_apply)
        if remove_ds == apply_ds:
            print("Cannot place card in the same place!: " + ' '.join(to_remove))
            return False
        if self.apply_remove(board, remove_ds):
            return self.apply(board, to_apply)
        return False

    #TODO - Check whether the removed state is valid
    def legal_remove(self, board, dest):
        return self.legal_card(dest)

    def legal(self, board, dest):
        for i, d in enumerate(dest):
            e, r = d[0], d[1]
            if r < 0 or len(board[0]) <= r:
                return False
            if e < 0 or len(board) <= e:
                return False
            if board[e][r]:
                return False
            # because we are only checking directly below,
            # there is the constraint that
            # we need to keep the order of the cards played
            # if second piece is above first
            # then we only need to check the first piece
            if i == 0 or r == dest[0][1]:
                if r is not 0:
                    if not board[e][r - 1]:
                        return False
        return True

    def to_n(self, char):
        return ord(char.upper()) - 65 

    def dest(self, card):
        if card[0] == '0':
            orientation = int(card[1])
            e = int(self.to_n(card[2]))
            r = int(card[3])-1
        else:
            orientation = int(card[0])
            e = int(self.to_n(card[1]))
            r = int(card[2])-1
            
        # if len(card) == 3:
        #     r = int(card[2])-1
        # if len(card) == 4:
        #     r = int(card[3])-1
        # elif len(card) == 5:
        #     r = int(card[3] + card[4])-1

        if orientation == 1:
            return ((e, r, 'R▶'), (e + 1, r, 'W◁'))
        if orientation == 2:
            return ((e, r, 'W△'), (e, r + 1, 'R▼'))
        if orientation == 3:
            return ((e, r, 'W▷'), (e + 1, r, 'R◀'))
        if orientation == 4:
            return ((e, r, 'R▲'), (e, r + 1, 'W▽'))
        if orientation == 5:
            return ((e, r, 'R▷'), (e + 1, r, 'W◀'))
        if orientation == 6:
            return ((e, r, 'W▲'), (e, r + 1, 'R▽'))
        if orientation == 7:
            return ((e, r, 'W▶'), (e + 1, r, 'R◁'))
        if orientation == 8:
            return ((e, r, 'R△'), (e, r + 1, 'W▼'))

    def render(self, board):
        t_board = zip(*board)
        self.print_instructions()

        for r, row in reversed(list(enumerate(t_board))):
            print(Back.BLACK + Fore.WHITE + str(r + 1) + (2 - int((r + 1) / 10)) * ' ' +
                  "".join([self.to_symbol(e) for e in row]))
        print(Back.BLACK + Fore.WHITE + '   ABCDEFGH' + Style.RESET_ALL)

    def print_instructions(self):
        print("\n " +            "".join(map(lambda x: self.to_symbol(x), [""  ,""  ,""  ,'R▼',""  ,""  ,""  ,""  ,'W▽',""  ,""  ,""  ,"" ,'R▽',""  ,""  ,""  ,""  ,'W▼'])))
        print(Back.BLACK + " " + "".join(map(lambda x: self.to_symbol(x), ['R▶','W◁',""  ,'W△',""  ,'W▷','R◀',""  ,'R▲',""  ,'R▷','W◀',"" ,'W▲',""  ,'W▶','R◁',""  ,'R△'])))
        print(Style.RESET_ALL + "\n 1  2 3  4 5  6 7  8")
        print()

    def to_symbol(self, string):
        if not string:
            return Back.BLACK + Fore.WHITE + '·'
        filled_in = ""
        if string[0].upper() == 'R' and string[1] in ['▷','△','▽','◁']:
            filled_in = self.fill_in(string[1])

        bg = fg = None

        if string[0].upper() == 'W':
            bg = Back.WHITE
        else:
            bg = Back.RED

        if not filled_in:
            fg = Fore.BLACK + string[1]
        else:
            fg = Fore.WHITE + filled_in

        return bg + fg

    def fill_in(self, sym):
        return {'▷':'▶','△':'▲','▽':'▼','◁':'◀'}[sym]

    def new(width = 8, height = 12):
        width, height = 8, 12
        return [['' for _ in range(height)] for _ in range(width)]

    def symbol_pair(self, sym):
        return {
            'R▶': 'W◁',
            'W△': 'R▼',
            'W▷': 'R◀',
            'R▲': 'W▽',
            'R▷': 'W◀',
            'W▲': 'R▽',
            'W▶': 'R◁',
            'R△': 'W▼'
        }[sym]


    def legal_card(self, card):
        col1, row1, sym1 = card[0][0], card[0][1], card[0][2]
        col2, row2, sym2 = card[1][0], card[1][1], card[1][2]
        if sym1[1] == '▶' or sym1[1] == '▷':
            return self.symbol_pair(sym1) == sym2 \
                and col1 == col2 - 1 and row1 == row2
        elif sym1[1] == '△' or sym1[1] == '▲':
            return self.symbol_pair(sym1) == sym2 \
                and col1 == col2 and row1 == row2 - 1
        return False

