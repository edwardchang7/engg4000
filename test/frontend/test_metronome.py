import time
import unittest

from src.frontend.metronome import Metronome
from unittest.mock import patch


class TestMetronome(unittest.TestCase):
    @patch("musicalbeeps.Player")
    @patch("time.time")
    def test_metronome_with_duration(self, mock_time_time, mock_musicalbeeps_player):
        testing_duration = 999
        metronome = Metronome()
        metronome.start(testing_duration)

        self.assertTrue(mock_musicalbeeps_player.called)
        self.assertTrue(mock_time_time.called)
        return

    # UNCOMMENT THIS TEST TO RUN IT LOCALLY/MANUALLY
    #
    # @patch("musicalbeeps.Player")
    # @patch("time.time")
    # def test_metronome_without_duration(self, mock_time_time, mock_musicalbeeps_player):
    #     metronome = Metronome()
    #     metronome.start()
    #
    #     self.assertTrue(mock_musicalbeeps_player.called)
    #     time.sleep(3)
    #     self.assertFalse(mock_time_time.called)
    #     return
