import nose
import os
import sys
import unittest

sys.path.insert(0, '..')
import pvc


class PVCTests(unittest.TestCase):

    def test_file_exists(self):
        t_pvc = pvc.PVC(bmG="tests/bmG.csv")
        self.assertTrue(os.path.isfile(t_pvc.files.bmG))

    def test_file_read(self):
        t_pvc = pvc.PVC(bmG="tests/bmG.csv")
        t_pvc.get_needed_data("bmG")
        print(t_pvc.data.bmG)
        self.assertTrue(1.74 in t_pvc.data.bmG.z)

    def test_calculate_average(self):
        t_pvc = pvc.PVC(bmG="tests/bmG.csv")
        t_pvc.get_needed_data("bmG")
        t_pvc.calculate_average("bmG")
        print(t_pvc.data.bmG)
        self.assertTrue(1.693 == t_pvc.data.bmG.z_ave)


if __name__ == '__main__':
    nose.runmodule()
