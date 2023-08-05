from unittest import TestCase
import unittest

from conv import convolved_1d


class TestConvolved1D(TestCase):

    def test_trivial_loop(self):
        expected = tuple(range(7))
        result = []

        for kernel_hover in convolved_1d(expected, kernel_size=1, padding=0, stride=1):
            result.append(*kernel_hover)
        result = tuple(result)

        self.assertEqual(expected, result)

    def test_seven_for_with_stride_two(self):
        expected = tuple(range(0, 7, 2))
        result = []

        for kernel_hover in convolved_1d(list(range(7)), kernel_size=1, padding=0, stride=2):
            result.append(*kernel_hover)
        result = tuple(result)

        self.assertEqual(expected, result)

    def test_seven_for_with_padding_one(self):
        expected = tuple([42] + list(range(0, 7)) + [42])
        result = []

        for kernel_hover in convolved_1d(list(range(7)), kernel_size=1, padding=1, stride=1, default_value=42):
            result.append(*kernel_hover)
        result = tuple(result)

        self.assertEqual(expected, result)

    def test_seven_kernel_of_two(self):
        expected = tuple([a, b] for a, b in zip(list(range(0, 6)), list(range(1, 7))))
        result = []

        for kernel_hover in convolved_1d(list(range(7)), kernel_size=2, padding=0, stride=1):
            result.append(kernel_hover)
        result = tuple(result)

        self.assertEqual(expected, result)

    def test_seven_kernel_of_two_and_stride_two(self):
        expected = ([0, 1], [2, 3], [4, 5], [6, None])
        result = []

        for kernel_hover in convolved_1d(list(range(7)), kernel_size=2, padding=0, stride=2):
            result.append(kernel_hover)
        result = tuple(result)

        self.assertEqual(expected, result)

    def test_seven_kernel_of_two_and_stride_two_and_padding_two(self):
        expected = ([None, None], [0, 1], [2, 3], [4, 5], [6, None], [None, None])
        result = []

        for kernel_hover in convolved_1d(list(range(7)), kernel_size=2, padding=2, stride=2):
            result.append(kernel_hover)
        result = tuple(result)

        self.assertEqual(expected, result)

    def test_seven_kernel_of_two_and_stride_two_and_padding_three(self):
        expected = ([None, None], [None, 0], [1, 2], [3, 4], [5, 6], [None, None], [None, None])
        result = []

        for kernel_hover in convolved_1d(list(range(7)), kernel_size=2, padding=3, stride=2):
            result.append(kernel_hover)
        result = tuple(result)

        self.assertEqual(expected, result)

    def test_seven_kernel_of_three_and_stride_two_and_padding_two(self):
        expected = ([None, None, 0], [0, 1, 2], [2, 3, 4], [4, 5, 6], [6, None, None])
        result = []

        for kernel_hover in convolved_1d(list(range(7)), kernel_size=3, padding=2, stride=2):
            result.append(kernel_hover)
        result = tuple(result)

        self.assertEqual(expected, result)

    def test_seven_kernel_of_two_and_stride_three_and_padding_two(self):
        expected = ([None, None], [1, 2], [4, 5], [None, None])
        result = []

        for kernel_hover in convolved_1d(list(range(7)), kernel_size=2, padding=2, stride=3):
            result.append(kernel_hover)
        result = tuple(result)

        self.assertEqual(expected, result)

    def test_seven_kernel_of_three_and_stride_three_and_padding_three(self):
        expected = ([None, None, None], [0, 1, 2], [3, 4, 5], [6, None, None], [None, None, None])
        result = []

        for kernel_hover in convolved_1d(list(range(7)), kernel_size=3, padding=3, stride=3):
            result.append(kernel_hover)
        result = tuple(result)

        self.assertEqual(expected, result)

    def test_big_kernel_loops_once(self):
        expected = tuple(range(3))
        result = []

        for kernel_hover in convolved_1d(expected, kernel_size=7, padding=0, stride=1, default_value=None,
                                         include_incomplete_pass=True):
            result.append(kernel_hover)

        self.assertEqual(len(result), 1)

    def test_big_kernel_loops_twice(self):
        expected = tuple(range(7 + 3))
        result = []

        for kernel_hover in convolved_1d(expected, kernel_size=7, padding=0, stride=7, default_value=None,
                                         include_incomplete_pass=True):
            result.append(kernel_hover)

        self.assertEqual(len(result), 2)

    def test_big_kernel_loops_never(self):
        expected = []
        result = []

        for kernel_hover in convolved_1d(expected, kernel_size=7, padding=0, stride=7, default_value=None,
                                         include_incomplete_pass=True):
            result.append(kernel_hover)

        self.assertEqual(len(result), 0)


if __name__ == '__main__':
    unittest.main()
