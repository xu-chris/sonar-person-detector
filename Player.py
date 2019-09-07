import os
import time


class Player:

    def __init__(self):
        self.state = 'stop'

    def play_video(self, id_video):
        self.state = id_video

    def stop_playing(self):
        self.state = 'stop'

    def get_state(self):
        return self.state
