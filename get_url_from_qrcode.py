#!/usr/bin/env python
import fitz
import cv2
from PIL import Image
from pyzbar.pyzbar import decode
import sys
import os

def get_images_from_pdf(filename):
    """Retrieves images from pdf file.

    Args:
        filename: string

    Returns:
        :obj:`list` of :obj:`Pixmap`.
    """
    doc = fitz.open(filename)
    imgs = []
    for i in range(len(doc)):
        for img in doc.get_page_images(i):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.n < 5:       # this is GRAY or RGB
                imgs.append(pix)
            else:               # CMYK: convert to RGB first
                pix1 = fitz.Pixmap(fitz.csRGB, pix)
                imgs.append(pix1)
    return imgs


def read_qrcode(imgs):
    """Get url from qrcode.

    Args:
        imgs: 'list' (Pixmap)

    Returns:
        :obj:`string` (string) if image contain qrcode
        else None.
    """
    for pix in imgs:
        if pix.samples == None or pix.colorspace.name != "DeviceRGB":
            continue
        try:
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        except:
            continue
        qrcode = decode(img)
        if qrcode == []:
            continue
        else:
            return str(qrcode[0].data.decode())
    return ""


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 1:
        print("")
    else:
        filename = args[0]
        if not os.path.exists(filename):
            print("")
        else:
            if filename.split(".")[-1] in ["png", "jpg"]:
                image = fitz.Pixmap(filename)
                url = read_qrcode([image])
                print(url)
            else:
                images = get_images_from_pdf(filename=filename)
                url = read_qrcode(images)
                print(url)
