# This file is part of applesauce.
#
# applesauce is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# applesauce is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with applesace.  If not, see <http://www.gnu.org/licenses/>.
import collections
CAPTION = "Applesauce"


SCREEN_SIZE = collections.namedtuple('Size', 'width height')(800, 600)

ENEMY_MAX_V_1 = 2
ENEMY_MAX_V_2 = 3

OFFICER_MAX_V_1 = 3.75
OFFICER_MAX_V_2 = 4.75


TIME_IN_RANDOM_DIR = 100
TIME_IN_RANDOM_DIR_VARIATION = 100

TIME_UNTIL_LOST = 100
TIME_UNTIL_OFFICER_LOST = TIME_UNTIL_LOST

OFFICER_VIEW_DISTANCE = 300
OFFICER_ALERT_DISTANCE = 100

BOOMBOX_RADIUS = 150

TURKEY_SPEED_MODIFIER = 0.50
TURKEY_SPLASH_SIZE = 50

HUD_FONT_SIZE = 32

FLYER_RADIUS = 500

DOOR_FRAME_TIME = 10
DOOR_FRAME_COUNT = 6
