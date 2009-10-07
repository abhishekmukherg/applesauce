import ConfigParser
import operator
import ast
from itertools import imap

import pkg_resources


class ConfigFileNotFound(OSError):
    pass


class LevelConfig(object):

    def __init__(self, filename):
        """Opens a level config

        filename should be the path from the package's root directory to the
        config file, seperated by /'s. For example, config/level0.ini

        """
        self.config = ConfigParser.RawConfigParser()
        self.config.readfp(
                pkg_resources.resource_stream("applesauce", filename))

    def __get_list_from_section(self, section):
        locations = imap(operator.itemgetter(1), self.config.items(section))
        return imap(ast.literal_eval, locations)

    def basic_enemies(self):
        """Returns a generator of locations for basic enemies"""
        return self.__get_list_from_section("BasicEnemies")

    def officers(self):
        return self.__get_list_from_section("Officers")

    def image(self):
        return self.config.get("LevelInfo", "image")

