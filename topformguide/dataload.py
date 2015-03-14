from topformguide.dataload import dataloader
# import topformguide
#from django.conf import settings
import sys
#import os
"""
A main method for triggering data loading from file
"""
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "topformguide.settings")
#settings.configure(default_settings=topformguide.settings)

loader = dataloader.DataLoader(True)
loader.loadCarsFromFile('/files/dev/projects/topformguide/data/failed.json')