import io
from unittest import TestCase, mock

import blackjack


class TestBlackjack(TestCase):

    @mock.patch('builtins.input', return_value='x')
    def test_player_bet_quit(self, mock_input):
        actual = blackjack.player_bet()
        self.assertEqual(-1, actual)

    @mock.patch('builtins.input', return_value='50')
    def test_player_bet_valid(self, mock_input):
        actual = blackjack.player_bet()
        self.assertEqual(50, actual)

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    @mock.patch('builtins.input', create=True)
    def test_player_invalid_entry(self, mock_input, mock_stdout):
        mock_input.side_effect = ['c', 'x']
        actual = blackjack.player_bet()
        self.assertEqual('c is not a valid entry\n', mock_stdout.getvalue())
        self.assertEqual(-1, actual)

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    @mock.patch('builtins.input', create=True)
    def test_player_zero_entry(self, mock_input, mock_stdout):
        mock_input.side_effect = ['0', 'x']
        actual = blackjack.player_bet()
        self.assertEqual('Bets must be greater than 0\n', mock_stdout.getvalue())
        self.assertEqual(-1, actual)

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    @mock.patch('builtins.input', create=True)
    def test_player_over_limit_entry(self, mock_input, mock_stdout):
        mock_input.side_effect = ['100000', 'x']
        actual = blackjack.player_bet()
        self.assertEqual('You do not have enough to bet that high\n', mock_stdout.getvalue())
        self.assertEqual(-1, actual)
