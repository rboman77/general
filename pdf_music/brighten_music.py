import pathlib
from typing import List

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


# From copilot
def numpy_images_to_pdf(image_arrays, output_path):
    """
    Converts a list of NumPy image arrays to a multi-page PDF.

    Parameters:
        image_arrays (List[np.ndarray]): List of image arrays.
        output_path (str): Path to save the output PDF.
    """
    # Convert NumPy arrays to PIL Images
    pil_images = [
        Image.fromarray(arr.astype('uint8')).convert('RGB')
        for arr in image_arrays
    ]

    # Save as multi-page PDF
    if pil_images:
        pil_images[0].save(output_path,
                           save_all=True,
                           append_images=pil_images[1:])
    else:
        raise ValueError("No images provided.")


data_folder = (pathlib.Path('/mnt') / 'g' / 'My Drive' / 'church' /
               'music_dec_2025')
assert data_folder.exists()
input_pdf_file = data_folder / 'gesu_bambino_orig.pdf'
output_pdf_file = data_folder / 'gesu_bambino_whitened.pdf'
assert input_pdf_file.exists()

print('reading PDF file')
pages = pdf_to_numpy_arrays(str(input_pdf_file), 300)
proc_pages = []
bright_value = 150
for x in pages:
    hsv = cv.cvtColor(x, cv.COLOR_BGR2HSV)
    hsv[:, :, 1] = 0
    mod_x = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
    gray_image = cv.cvtColor(mod_x, cv.COLOR_BGRA2GRAY)
    lookup_table = np.zeros((256, ), np.uint8)
    for i in range(256):
        if i < bright_value:
            frac = float(i) / float(bright_value) * 256.
            lookup_table[i] = min(255, int(frac))
        else:
            lookup_table[i] = 255
    print(lookup_table)
    bright_image = cv.LUT(gray_image, lookup_table)
    proc_pages.append(bright_image)

print('Writing PDF file')
numpy_images_to_pdf(proc_pages, str(output_pdf_file))
print('done')
