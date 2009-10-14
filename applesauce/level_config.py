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
        
    def player(self):
        if not self.config.has_section("Player"):
            return tuple()
        return self.__get_list_from_section("Player")

    def basic_enemies(self):
        """Returns a generator of locations for basic enemies"""
        if not self.config.has_section("BasicEnemies"):
            return tuple()
        return self.__get_list_from_section("BasicEnemies")

    def officers(self):
        if not self.config.has_section("Officers"):
            return tuple()
        return self.__get_list_from_section("Officers")

    def walls(self):
        if not self.config.has_section("Walls"):
            return tuple()
        return self.__get_list_from_section("Walls")

    def doors(self):
        if not self.config.has_section("Doors"):
            return tuple()
        return self.__get_list_from_section("Doors")
        
    def bombsites(self):
        if not self.config.has_section("BombSites"):
            return tuple()
        return self.__get_list_from_section("BombSites")
        
    def end(self):
        if not self.config.has_section("End"):
            return tuple()
        return self.__get_list_from_section("End")
        
    def image(self):
        return self.config.get("LevelInfo", "image")

    def magic_scroll(self):
        if not self.config.has_option("LevelInfo", "magic_scroll"):
            return True
        return ast.literal_eval(self.config.get("LevelInfo", "magic_scroll"))

    def hud_level(self):
        if not self.config.has_option("LevelInfo", "hud"):
            return None
        return ast.literal_eval(self.config.get("LevelInfo", "hud"))

    def big(self):
        if not self.config.has_option("LevelInfo", "big"):
            return False
        return ast.literal_eval(self.config.get("LevelInfo", "big"))

    def start(self):
        if not self.config.has_option("LevelInfo", "start"):
            return (0,0)
        return ast.literal_eval(self.config.get("LevelInfo", "start"))
