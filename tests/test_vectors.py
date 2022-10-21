import unittest
import asciiglet


class VectorTests(unittest.TestCase):
    def test_element_order_initialization(self):
        for pairs in [(0.0, 0.0), (1.0, 1.0), (3.0, -1.0)]:
            vec = Vector.new(pairs[0]. pairs[1])
            self.assertTrue(vec[0] == pairs[0] and vec[1] == pairs[1])

    def test_rotate_unit_circle(self):
        vec = Vector.new(1.0, 1.0)

        for angle, answer in [
            (0.0, (1.0, 1.0)),
            (90.0, (-1.0, 1.0)),
            (180.0, (-1.0, -1.0)),
            (360.0, (1.0, 1.0)),
            (720.0, (1.0, 1.0)),
            (-90.0, (1.0, -1.0)),
        ]:
            estimate = Vector.rotate(vec, angle)
            self.assertTrue(estimate[0] == answer[0] and estimate[1] == answer[1])
