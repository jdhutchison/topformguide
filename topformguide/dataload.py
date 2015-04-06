from topformguide.dataload import dataloader
import sys
"""
A main method for triggering data loading from file
"""
loader = dataloader.DataLoader(True)
if datafile is not None:
    loader.loadCarsFromFile(datafile)
else:
    print('A datafile must be specified to run this file.\n')