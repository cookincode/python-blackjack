class Card:

    def __init__(self, rank: str, suit: str, down=True) -> None:
        self.rank = rank
        self.suit = suit
        self._down = down

    def __repr__(self):
        return f"<Card {{'rank'={self.rank}, 'suit'={self.suit}, 'down'={self._down}}}"

    def __str__(self):
        if self._down:
            return '##'

        return f'{self.rank}{self.suit[0].upper()}'

    def up(self):
        self._down = False
        return self

    def down(self):
        self._down = True
        return self

    def turn(self):
        self._down = not self._down
        return self


class Deck:
    ranks = list('A') + [str(n) for n in range(2, 11)] + list('JQK')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit)
                       for rank in self.ranks
                       for suit in self.suits]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def __setitem__(self, position, card):
        self._cards[position] = card

    def __iter__(self):
        return self

    def __next__(self):
        if len(self._cards) == 0:
            raise StopIteration

        return self._cards.pop(0)

    def add_cards(self, cards):
        if type(cards) == Card:
            self._cards.append(cards)

        if type(cards) == list:
            self._cards.extend(cards)
