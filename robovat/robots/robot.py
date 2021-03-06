"""The basic class of robots."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import abc
import os

from robovat.utils.string_utils import camelcase_to_snakecase
from robovat.utils.yaml_config import YamlConfig


class Robot(object):
    """Base class for robots."""
    __metaclass__ = abc.ABCMeta

    def __init__(self, config=None, root_dir=None):
        """Initialize.

        config: The configuartion as a dictionary.
        """
        self.config = config or self.default_config
        if isinstance(self.config, str):
            self.config = YamlConfig(self.config, root_dir=root_dir).as_easydict()

    @abc.abstractmethod
    def reboot(self):
        """Reboot the robot.
        """
        pass

    @abc.abstractmethod
    def reset(self):
        """Reset the robot.
        """
        pass

    @property
    def pose(self):
        raise NotImplementedError

    @property
    def position(self):
        return self.pose.position

    @property
    def orientation(self):
        return self.pose.orientation

    @property
    def euler(self):
        return self.orientation.euler

    @property
    def quaternion(self):
        return self.orientation.quaternion

    @property
    def matrix3(self):
        return self.orientation.matrix3

    @property
    def default_config(self):
        """Load the default configuration file."""
        robot_name = camelcase_to_snakecase(type(self).__name__)
        config_path = os.path.join('configs', 'robots',
                                   '%s.yaml' % (robot_name))
        assert os.path.exists(config_path), (
            'Default configuration file %s does not exist' % (config_path))
        return YamlConfig(config_path).as_easydict()
