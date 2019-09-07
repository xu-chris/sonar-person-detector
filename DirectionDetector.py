from Sensor import Sensor
from DirectionState import DirectionState
import logging


def evaluate_direction(old_detection, new_detection):
    """
    Evaluates two given detection results and returns the Direction enum as state result.
    :param old_detection: The old detection
    :param new_detection: The new detection
    :return: Direction enum object that holds the direction
    """

    # Left to right
    if (
            old_detection == [False, False] and
            new_detection == [True, False]
    ) or (
            old_detection == [True, False] and
            new_detection == [True, True]
    ) or (
            old_detection == [True, True] and
            new_detection == [False, True]
    ) or (
            old_detection == [False, True] and
            new_detection == [False, False]
    ):
        return DirectionState.RIGHT

    elif (
            old_detection == [False, False] and
            new_detection == [False, True]
    ) or (
            old_detection == [False, True] and
            new_detection == [True, True]
    ) or (
            old_detection == [True, True] and
            new_detection == [True, False]
    ) or (
            old_detection == [True, False] and
            new_detection == [False, False]
    ):
        return DirectionState.LEFT

    elif old_detection == [False, False] and old_detection == new_detection:
        return DirectionState.NONE

    else:
        return DirectionState.UNKNOWN


class DirectionDetector:

    def __init__(self):
        self.current_detection = None
        self.sensor_left = Sensor(trigger_channel=22, echo_channel=27)
        self.sensor_right = Sensor(trigger_channel=5, echo_channel=6)
        logging.debug('DirectionDetector initialized')

        self.setup()

    def setup(self):
        """
        Triggers first the calibration and runs an initial detection
        """

        # Calibrate sensors
        logging.debug('Calibrate left sensor...')
        self.sensor_left.calibrate(for_seconds=10, threshold_reduction=0.1)
        logging.debug('Calibrate right sensor...')
        self.sensor_right.calibrate(for_seconds=10, threshold_reduction=0.1)

        # Get current result
        self.current_detection = (self.sensor_left.detect(), self.sensor_right.detect())
        logging.debug('Current detection result: {}'.format(self.current_detection))

    def detect(self):
        """
        Runs the detection on both sensors and evaluates the result.
        :return: The direction result
        """

        # Get result of detectors first
        new_detection = (self.sensor_left.detect(), self.sensor_right.detect())
        logging.debug('Detection run result: {}'.format(new_detection))

        # Compare with simple state comparison
        result = evaluate_direction(self.current_detection, new_detection)

        # Close detection
        self.current_detection = new_detection
        return result
