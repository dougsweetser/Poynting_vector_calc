#!/usr/bin/env python
"""
usage: pyc.py [--bmG BMGFile] [--bmT BMTFile]
              [--emG EMGFile] [--emT EMTFile] [--root NAME]

Given 4 csv files, calculates the Poynting vector

optional arguments:
  --bmG BMGFile   background mGauss csv file name [default: bmG.csv]
  --bmT BMGFile   background mTesla csv file name [default: bmT.csv]
  --emG BMGFile   experimental mGauss csv file name [default: emG.csv]
  --emT BMGFile   experimental mTesla csv file name [default: emT.csv]
  -r NAME --root NAME   
                  If the 4 files are named NAME_bmG.csv, NAME_bmT.csv
                  NAME_emG.csv, NAME_emT.csv, set this variable once
                  Note: skip the _ in NAME.
"""

from bunch import Bunch
from docopt import docopt
import csv


class PVC:
    """
    Calculate a Poynting vector given 4 csv files.
    """

    def __init__(self, bmG="bmG.csv", bmT="bmT.csv", emG="emG.csv",
                 emT="emT.csv", root=''):

        if root:
            root += "_"

        self.labels = Bunch()
        self.files = Bunch()
        self.data = Bunch()

        self.labels.bmG = "background E field"
        self.labels.bmT = "background B field"
        self.labels.emG = "experimental E field"
        self.labels.emT = "experimental B field"

        self.files.bmG = "{r}{k}".format(r=root, k=bmG)
        self.files.bmT = "{r}{k}".format(r=root, k=bmT)
        self.files.emG = "{r}{k}".format(r=root, k=emG)
        self.files.emT = "{r}{k}".format(r=root, k=emT)

        self.key_ids = ('bmG', 'bmT', 'emG', 'emT')

        for key_id in self.key_ids:
            self.data[key_id] = Bunch()
            self.data[key_id].x = []
            self.data[key_id].y = []
            self.data[key_id].z = []

    def run(self):
        "Runs all."

        for key_id, file_name in self.files.items():
            self.get_needed_data(key_id)
            self.calculate_average(key_id)

        for key_id in self.key_ids:
            print("ave {l}: {x}, {y}, {z}".format(l=self.labels[key_id],
                x=self.data[key_id].x_ave, y=self.data[key_id].y_ave, 
                z=self.data[key_id].z_ave))

        
        self.calculate_Poynting_vector()

    def get_needed_data(self, key_id):
        """Read the files."""

        with open(self.files[key_id], 'r') as csvfile:
            data_reader = csv.reader(csvfile)

            for data in data_reader:
                self.data[key_id].x.append(float(data[1]))
                self.data[key_id].y.append(float(data[2]))
                self.data[key_id].z.append(float(data[3]))

    def calculate_average(self, key_id):
        """Simple average calculation."""

        self.data[key_id].x_ave = float(sum(self.data[key_id].x) / max(len(self.data[key_id].x), 1))
        self.data[key_id].y_ave = float(sum(self.data[key_id].y) / max(len(self.data[key_id].x), 1))
        self.data[key_id].z_ave = float(sum(self.data[key_id].z) / max(len(self.data[key_id].x), 1))

    def calculate_Poynting_vector(self):
        """Use the collected data."""

        bGx = self.data.bmG.x_ave
        bGy = self.data.bmG.y_ave
        bGz = self.data.bmG.z_ave

        bTx = self.data.bmT.x_ave
        bTy = self.data.bmT.y_ave
        bTz = self.data.bmT.z_ave

        mGx = self.data.emG.x_ave - bGx
        mGy = self.data.emG.y_ave - bGy
        mGz = self.data.emG.z_ave - bGz

        mTx = self.data.emT.x_ave - bTx
        mTy = self.data.emT.y_ave - bTy
        mTz = self.data.emT.z_ave - bTz

        bpx = (bGy * bTz) - (bGz * bTy)
        bpy = (bGz * bTx) - (bGx * bTz)
        bpz = (bGx * bTy) - (bGy * bTx)

        px = (mGy * mTz) - (mGz * mTy)
        py = (mGz * mTx) - (mGx * mTz)
        pz = (mGx * mTy) - (mGy * mTx)

        print ("Background Poynting Vector\n{0}, {1}, {2}".format(bpx, bpy, bpz))

        print ("Average Poynting Vector\n{0}, {1}, {2}".format(px, py, pz))

if __name__ == "__main__":

    ARGS = docopt(__doc__)
#
    pvc = PVC(bmG=ARGS['--bmG'], bmT=ARGS['--bmT'], emG=ARGS['--emG'],
              emT=ARGS['--emT'], root=ARGS['--root'])
    pvc.run()
