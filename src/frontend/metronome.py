import musicalbeeps
import threading
import time


class Metronome:
    def __init__(self, tempo: int = 60, time_signature: list = [4, 4]):
        """
        Initializes metronome data when the metronome object is created.

        :param tempo: The speed or pace of the metronome. Tempo is usually measured in BPM.
        :param time_signature: Specifies how many beats are contained in each measure.
        """
        self.tempo: int = tempo
        self.time_signature: list = time_signature
        self.delay_in_seconds: float = 60.0 / self.tempo

    def start(self, metronome_duration_in_seconds: float = None, volume: float = 1.0, metronome_note: str = "C4"):
        """
        Starts the metronome with a separate thread.

        :param metronome_duration_in_seconds: How long the metronome should be played for.
        :param volume: How loud the metronome should be.
        :param metronome_note: The note that is played at each metronome "tick".
        """
        metronome_thread = threading.Thread(
            target=self.metronome,
            args=(metronome_duration_in_seconds, volume, metronome_note)
        )
        metronome_thread.start()

    def metronome(self, metronome_duration_in_sec: float = None, volume: float = 1.0, metronome_note: str = "C4"):
        """
        This function holds the metronome algorithm/functionality. This function should be called with a separate thread
        so that it does not hinder other processes.

        :param metronome_duration_in_sec: How long the metronome should be played for.
        :param volume: How loud the metronome should be.
        :param metronome_note: The note that is played at each metronome "tick".
        """
        note_player = musicalbeeps.Player(volume, mute_output=False)

        if metronome_duration_in_sec is not None:
            end_time = time.time() + metronome_duration_in_sec
            while time.time() < end_time:
                self.play_note(note_player, metronome_note, self.delay_in_seconds / 2.0)
                time.sleep(self.delay_in_seconds / 2.0)
                return

        while True:
            self.play_note(note_player, metronome_note, self.delay_in_seconds / 2.0)
            time.sleep(self.delay_in_seconds / 2.0)

    def play_note(self, note_player, note: str, note_duration: float):
        """
        Plays the provided note with the musicalbeeps library.

        :param note_player: The note player from the musicalbeeps library.
        :param note: The note to play.
        :param note_duration: How long the note should be played for.
        """
        note_player.play_note(note, note_duration)

    def set_tempo(self, tempo: int):
        self.tempo = tempo
        self.delay_in_seconds = 60.0 / self.tempo  # we must also update the delay of every metronome "tick"

    def get_tempo(self) -> int:
        return self.tempo

    def set_time_signature(self, time_signature: list):
        self.time_signature = time_signature

    def get_time_signature(self) -> list:
        return self.time_signature
