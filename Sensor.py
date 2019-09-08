import RPi.GPIO as GPIO
from datetime import datetime
import time
import logging


class Sensor:

    def __init__(self, trigger_channel=22, echo_channel=27):
        self.activation_threshold = None
        self.trigger_channel = trigger_channel
        self.echo_channel = echo_channel

    def measure(self):
        """
        Starts measuring the distance by using the time of flight traveled
        :return: distance of current measurement
        """

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        print('Setting up sensor. Trigger: {}, echo: {}'.format(self.trigger_channel, self.echo_channel))
        print('Function of the chosen pins: {}, {}'.format(GPIO.gpio_function(self.trigger_channel),
                                                           GPIO.gpio_function(self.echo_channel)))
        GPIO.setup(self.trigger_channel, GPIO.OUT)
        GPIO.setup(self.echo_channel, GPIO.IN)

        start_time = time.time()
        stop_time = time.time()
        # set Trigger to HIGH
        GPIO.output(self.trigger_channel, GPIO.HIGH)
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.trigger_channel, GPIO.LOW)

        # save start_time
        while GPIO.input(self.echo_channel) == 0:
            start_time = time.time()

        # save time of arrival
        while GPIO.input(self.echo_channel) == 1:
            stop_time = time.time()

        # time difference between start and arrival
        time_elapsed = stop_time - start_time
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because time sent and received is the doubled time
        distance = (time_elapsed * 34300) / 2
        # print('Measured distance: {}'.format(distance))
        GPIO.cleanup([self.trigger_channel, self.echo_channel])
        return distance

    def obstacle_detected(self, distance):
        """
        Checks with the given distance if there is something in front of the sensor (e.g. a person)
        :param distance: the measured distance of the sensor
        :return: True if obstacle is detected, otherwise False
        """
        if distance < self.activation_threshold:
            return True
        else:
            return False

    def detect(self):
        """
        Convenience function to call measurement and obstacle_detected functions one after the other.
        :return: True if obstacle is detected, otherwise False
        """
        distance = self.measure()
        return self.obstacle_detected(distance)

    def calibrate(self, for_seconds=10, threshold_reduction=0.1):
        """
        Calibrates the sensor by setting the lowest trigger value recorded in 5 seconds - 10% as a threshold.
        """

        # Set the activation threshold really high
        self.activation_threshold = 10000

        start_time = datetime.now()
        current_time = datetime.now()
        print('Calibration starts at {}, used pins: trigger: {}, echo: {}'.format(start_time, self.trigger_channel, self.echo_channel))

        while (current_time - start_time).seconds < for_seconds:

            # Measure
            measurement = self.measure()

            # If Xth percentage of the measurement is lower than current activation threshold, save new threshold
            if measurement <= 0:
                print('Sensor on pins {}, {} seems to be broken. invalid measurement result: {}'.format(self.trigger_channel, self.echo_channel, measurement))
            elif measurement < 100:
                print('Measurement is smaller than 100. Is something in it\'s way? Pins: {}, {} ;  Measurement: {}'.format(self.trigger_channel, self.echo_channel, measurement))
            elif measurement * (1 - threshold_reduction) < self.activation_threshold:
                self.activation_threshold = measurement * (1 - threshold_reduction)
                print('Saved new activation threshold: {}'.format(self.activation_threshold))
            else:
                print('No new measurements. Skipping...')
            current_time = datetime.now()

        print('Finished calibration at {}, used pins: trigger: {}, echo: {}'.format(current_time, self.trigger_channel,
                                                                                  self.echo_channel))

        return True
