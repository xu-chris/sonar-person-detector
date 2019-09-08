from DirectionState import DirectionState
from DirectionDetector import DirectionDetector
from BucketState import BucketState
import time


def evaluate_directions(old_directions, new_directions):
    # Person enters the bucket from left
    if (
            old_directions == [DirectionState.NONE, DirectionState.NONE] and
            new_directions == [DirectionState.RIGHT, DirectionState.NONE]
    ) or (
            old_directions == [DirectionState.RIGHT, DirectionState.NONE] and
            new_directions == [DirectionState.NONE, DirectionState.NONE]
    ):
        return BucketState.ONE_IN_FROM_LEFT

    elif (
            old_directions == [DirectionState.NONE, DirectionState.NONE] and
            new_directions == [DirectionState.LEFT, DirectionState.NONE]
    ) or (
            old_directions == [DirectionState.LEFT, DirectionState.NONE] and
            new_directions == [DirectionState.NONE, DirectionState.NONE]
    ):
        return BucketState.ONE_OUT_TO_LEFT

    elif (
            old_directions == [DirectionState.NONE, DirectionState.NONE] and
            new_directions == [DirectionState.NONE, DirectionState.LEFT]
    ) or (
            old_directions == [DirectionState.NONE, DirectionState.LEFT] and
            new_directions == [DirectionState.NONE, DirectionState.NONE]
    ):
        return BucketState.ONE_IN_FROM_RIGHT

    elif (
            old_directions == [DirectionState.NONE, DirectionState.NONE] and
            new_directions == [DirectionState.NONE, DirectionState.RIGHT]
    ) or (
            old_directions == [DirectionState.NONE, DirectionState.RIGHT] and
            new_directions == [DirectionState.NONE, DirectionState.NONE]
    ):
        return BucketState.ONE_OUT_TO_RIGHT

    elif (
            old_directions == [DirectionState.RIGHT, DirectionState.NONE] and
            new_directions == [DirectionState.NONE, DirectionState.LEFT]
    ) or (
            old_directions == [DirectionState.RIGHT, DirectionState.LEFT] and
            new_directions == [DirectionState.NONE, DirectionState.NONE]
    ) or (
            old_directions == [DirectionState.NONE, DirectionState.LEFT] and
            new_directions == [DirectionState.RIGHT, DirectionState.NONE]
    ):
        return BucketState.TWO_IN
    else:
        return BucketState.UNKNOWN


class Bucket:

    def __init__(self, devices):
        self.left_direction_detector = DirectionDetector(devices[0], devices[1])
        self.right_direction_detector = DirectionDetector(devices[2], devices[3])
        self.current_directions = None

    def setup(self):
        """
        Sets up the bucket
        """

        # Save current direction pair for now
        self.current_directions = (self.left_direction_detector.detect(), self.right_direction_detector.detect())

    def detect(self):
        """
        Detects the state of the bucket.
        :return: The result of the detection
        """

        # Gather new detection of directions
        new_directions = (self.left_direction_detector.detect(), self.right_direction_detector.detect())
        logging.info('Detected direction pair: {}. Detection result before was: {}'.format(new_directions,
                                                                                           self.current_directions))

        # Check if directions are different from before
        while self.current_directions == new_directions:
            time.sleep(0.1)
            new_directions = (self.left_direction_detector.detect(), self.right_direction_detector.detect())

        # Run evaluation
        result = evaluate_directions(self.current_directions, new_directions)

        # Close down
        self.current_directions = new_directions
        return result
