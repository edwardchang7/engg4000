import unittest

from src.backend.mxl_to_abc import batch_convert


class TestConverter(unittest.TestCase):
  
  def test_batch_convert():
    # check for converted_compositions directory if its there delete it
    print("ohya");
    # batch convert

    # check for converted_compositions directory





    # def test_metronome_with_duration(self, mock_time_time, mock_musicalbeeps_player):
    #     testing_duration = 999
    #     metronome = Metronome()
    #     metronome.start(testing_duration)

    #     self.assertTrue(mock_musicalbeeps_player.called)
    #     self.assertTrue(mock_time_time.called)
    #     return

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