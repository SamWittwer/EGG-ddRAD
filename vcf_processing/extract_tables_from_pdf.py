import os
import tabula
import numpy as np
import pandas as pd

for filename in os.listdir('../'):

    with open('outpdf.txt', 'a') as o:
        if filename.endswith(".pdf"):
            a = tabula.read_pdf('../' + filename)
            o.write(a.to_csv(sep=' ', index=False, header=False))
        else:
            continue

