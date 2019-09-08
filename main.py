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
from multiprocessing import Process
import socket
import webbrowser

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


class Server(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            host, port, debug = self.queue.get()
            try:
                app.run(host=host, port=port, debug=debug)
            finally:
                self.queue.task_done()


def set_logging():
    # logging.basicConfig(filename='BucketPlayer.log', level=print)
    # logging.basicConfig(format='%(asctime)s %(message)s')
    # logging.info('Started service. Logging level {}'.format(config['logging_level']))
    pass


def read_config():
    global config

    with open("config.yml", 'r') as yml_file:
        config = yaml.load(yml_file, Loader=yaml.FullLoader)


def run_detection():
    global bucketplayer

    while True:
        bucketplayer.run_detection()
        time.sleep(0.1)


def run_server(host='0.0.0.0', port=5000, debug=False, threading=True):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print('Starting server on http://{}:{}'.format(s.getsockname()[0],port))
    app.run(host=host, port=port, debug=debug, threaded=threading)


def run_browser():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    url = 'http://{}:5000'.format(s.getsockname()[0])
    webbrowser.open_new_tab(url)


def run_in_parallel(*fns):
    proc = []
    for fn in fns:
        p = Process(target=fn)
        p.start()
        proc.append(p)
    for p in proc:
        p.join()


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/current/', methods=['GET'])
def get_player_state():
    global bucketplayer
    print('Frontend fetches current state...')
    state = bucketplayer.player.state()
    return jsonify({'state': state}), 201


if __name__ == '__main__':
    read_config()
    set_logging()

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

    run_in_parallel(run_detection, run_server, run_browser)
