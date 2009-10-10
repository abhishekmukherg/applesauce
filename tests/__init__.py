import unittest
import tests.sprite.enemies

suite = unittest.TestSuite()

suite.addTest(tests.sprite.enemies.TestEnemy('test_obstruct_los'))
suite.addTest(tests.sprite.enemies.TestEnemy('test_get_section'))
