import unittest

import pygame

from applesauce.sprite import enemies


POINT_IN_SECTION = {0: (-1, -1),
                    1: (0.5, -1),
                    2: (2, -1),
                    3: (-1, 0.5),
                    4: (0.5, 0.5),
                    5: (2, 0.5),
                    6: (-1, 2),
                    7: (0.5, 2),
                    8: (2, 2),
                    }
class TestEnemy(unittest.TestCase):

    def test_obstruct_los(self):
        rect = pygame.Rect((0, 0), (1, 1))
        fn = enemies.Enemy._obstructs_los
        self.assertFalse(fn(rect, POINT_IN_SECTION[0], POINT_IN_SECTION[1]))
        self.assertFalse(fn(rect, POINT_IN_SECTION[0], POINT_IN_SECTION[2]))
        self.assertFalse(fn(rect, POINT_IN_SECTION[0], POINT_IN_SECTION[3]))
        self.assertFalse(fn(rect, POINT_IN_SECTION[0], POINT_IN_SECTION[6]))
        self.assert_(fn(rect, POINT_IN_SECTION[0], POINT_IN_SECTION[4]))
        self.assert_(fn(rect, POINT_IN_SECTION[0], POINT_IN_SECTION[5]))
        self.assert_(fn(rect, POINT_IN_SECTION[0], POINT_IN_SECTION[7]))
        self.assert_(fn(rect, POINT_IN_SECTION[0], POINT_IN_SECTION[8]))

        for i in xrange(9):
            self.assert_(fn(rect, POINT_IN_SECTION[4], POINT_IN_SECTION[i]),
                    "%s (in sec %d) should be obstructed from center" %
                        (POINT_IN_SECTION[i], i))

    def test_get_section(self):
        rect = pygame.Rect((0, 0), (1, 1))
        self.assertEqual(
                enemies.Enemy._get_section(rect, POINT_IN_SECTION[0]), 0,
                u"%s not in section %d" % (POINT_IN_SECTION[0], 0))
        self.assertEqual(
                enemies.Enemy._get_section(rect, POINT_IN_SECTION[1]), 1,
                u"%s not in section %d" % (POINT_IN_SECTION[1], 1))
        self.assertEqual(
                enemies.Enemy._get_section(rect, POINT_IN_SECTION[2]), 2,
                u"%s not in section %d" % (POINT_IN_SECTION[2], 2))
        self.assertEqual(
                enemies.Enemy._get_section(rect, POINT_IN_SECTION[3]), 3,
                u"%s not in section %d" % (POINT_IN_SECTION[3], 3))
        self.assertEqual(
                enemies.Enemy._get_section(rect, POINT_IN_SECTION[4]), 4,
                u"%s not in section %d" % (POINT_IN_SECTION[4], 4))
        self.assertEqual(
                enemies.Enemy._get_section(rect, POINT_IN_SECTION[5]), 5,
                u"%s not in section %d" % (POINT_IN_SECTION[5], 5))
        self.assertEqual(
                enemies.Enemy._get_section(rect, POINT_IN_SECTION[6]), 6,
                u"%s not in section %d" % (POINT_IN_SECTION[6], 6))
        self.assertEqual(
                enemies.Enemy._get_section(rect, POINT_IN_SECTION[7]), 7,
                u"%s not in section %d" % (POINT_IN_SECTION[7], 7))
        self.assertEqual(
                enemies.Enemy._get_section(rect, POINT_IN_SECTION[8]), 8,
                u"%s not in section %d" % (POINT_IN_SECTION[8], 8))

if __name__ == "__main__":
    unittest.main()
