# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from parallel_corpus_web.models import ParallelPage
import codecs
import os

# Test set file, should be in the root of the project (i.e. same dir as manage.py)
INPUT_FILE = "test_set.csv"

# Location of actual *.{en,kz} files
INPUT_DIR = "/home/aseke/research/SMT/STRANDAligner/articles/"


def read_file(fpath):
    f = codecs.open(fpath, "r", "utf-8")
    data = f.read()    
    f.close()
    return data

def load():    
    f = open(INPUT_FILE, "r")
    for i, line in enumerate(f.readlines()):
        if i == 0:
            # Skip headers
            continue
        fname = line.split(",")[0].strip('"')
        prefix = ""
        if "â" in fname:            
            fname = fname.replace("â", "\udce2")
            

        fname_en = "%sen" % fname
        fname_kz = "%skz" % fname
        
        fname_en = os.path.join(INPUT_DIR, fname_en)
        fname_kz = os.path.join(INPUT_DIR, fname_kz)
        en = read_file(fname_en)
        kz = read_file(fname_kz)

        parallel_page = ParallelPage(en_text=en,
                                    kz_text=kz,
                                    is_test=True,
                                    file_name=fname.replace("\udce2", "â"))
        parallel_page.save()
        print("Loaded test data from %d-th file" % (i + 1))
    f.close()            
    print("Finished loading test data.")

class Command(BaseCommand):
    def handle(self, *args, **options):
        load()




