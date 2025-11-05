import pathlib

import cv2 as cv
import numpy as np
from pdf2image import convert_from_path
from PIL import Image


# From copiplot.
def pdf_to_numpy_arrays(pdf_path, dpi=200):
    """
    Reads a multi-page PDF and returns a list of pages as NumPy arrays.

    Parameters:
        pdf_path (str): Path to the PDF file.
        dpi (int): Resolution for rendering PDF pages.

    Returns:
        List[np.ndarray]: List of NumPy arrays representing each page.
    """
    # Convert PDF pages to PIL images
    pages = convert_from_path(pdf_path, dpi=dpi)

    # Convert each PIL image to a NumPy array
    page_arrays = [np.array(page.convert('RGB')) for page in pages]

    return page_arrays


data_folder = (pathlib.Path('/mnt') / 'g' / 'My Drive' / 'church' /
               'music_dec_2025')
assert data_folder.exists()
input_pdf_file = data_folder / 'gesu_bambino_orig.pdf'
assert input_pdf_file.exists()

print('reading PDF file')
pages = pdf_to_numpy_arrays(str(input_pdf_file), 300)
for x in pages:
    print(x.shape)
