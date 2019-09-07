import logging
from Bucket import Bucket
from BucketState import BucketState
from Player import Player
import time

from flask import Flask  # For REST API suppprt
from flask import request
from flask import abort
from flask import jsonify
from flask import escape
from flask import render_template
from flask import make_response
from flask_cors import CORS

# Setup player server
app = Flask(__name__)
CORS(app)
bucketplayer = None


class BucketPlayer:

    def __init__(self):
        self.bucket = Bucket()
        self.player = Player()
        self.bucket_state = BucketState.UNKNOWN

    def run_detection(self):
        new_bucket_state = self.bucket.detect()

        if self.bucket_state != new_bucket_state:
            if new_bucket_state is BucketState.ONE_IN_FROM_LEFT:
                logging.info('Detected person coming from left. Start playing video.')
                self.player.play_video(0)
            elif new_bucket_state is BucketState.ONE_IN_FROM_RIGHT:
                logging.info('Detected person coming from right. Start playing video.')
                self.player.play_video(1)
            elif new_bucket_state is BucketState.TWO_IN:
                logging.info('Detected person coming from both sides. Start playing video.')
                self.player.play_video(2)
            else:
                logging.info(
                    'Current state {} does not match any of the rules. Stopping video...'.format(new_bucket_state))
                self.player.stop_playing()

        self.bucket_state = new_bucket_state


def set_logging():
    logging.basicConfig(filename='BucketPlayer.log', level=logging.DEBUG)
    logging.basicConfig(format='%(asctime)s %(message)s')
    logging.info('Started service')


@app.route('/current/', methods=['GET'])
def get_player_state():
    bucketplayer.player.state()


if __name__ == '__main__':

    set_logging()

    bucketplayer = BucketPlayer()

    while True:
        bucketplayer.run_detection()
        time.sleep(0.1)
