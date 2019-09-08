import logging
from Bucket import Bucket
from BucketState import BucketState
from Player import Player
import time
import yaml
from threading import Thread

from flask import Flask  # For REST API suppprt
from flask import jsonify
from flask import render_template
from flask_cors import CORS

# Setup player server
app = Flask(__name__, template_folder='static')
CORS(app)
config = None
bucketplayer = None


class BucketPlayer:

    def __init__(self, devices):
        self.bucket = Bucket(devices)
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


def read_config():
    global config

    with open("config.yml", 'r') as yml_file:
        config = yaml.load(yml_file, Loader=yaml.FullLoader)


def run_detection():
    global bucketplayer

    devices = [
        [
            config['left_device']['left_sensor']['trigger_channel'],
            config['left_device']['left_sensor']['echo_channel']
        ],
        [
            config['left_device']['right_sensor']['trigger_channel'],
            config['left_device']['right_sensor']['echo_channel']
        ],
        [
            config['right_device']['left_sensor']['trigger_channel'],
            config['right_device']['left_sensor']['echo_channel']
        ],
        [
            config['right_device']['right_sensor']['trigger_channel'],
            config['right_device']['right_sensor']['echo_channel']
        ]
    ]

    bucketplayer = BucketPlayer(devices)

    while True:
        bucketplayer.run_detection()
        time.sleep(0.1)


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/current/', methods=['GET'])
def get_player_state():
    print('Frontend fetches current state...')
    state = bucketplayer.player.state()
    return jsonify({'state': state}), 201


if __name__ == '__main__':

    read_config()

    set_logging()

    server = Thread(target=app.run(host='0.0.0.0', port=5000, debug=True)).start()
    detector = Thread(run_detection()).start()
