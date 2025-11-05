import pathlib

import cv2 as cv

data_folder = (pathlib.Path('/mnt') / 'g' / 'My Drive' / 'church' /
               'music_dec_2025')
assert data_folder.exists()
input_pdf_file = data_folder / 'gesu_bambino_orig.pdf'
assert input_pdf_file.exists()
