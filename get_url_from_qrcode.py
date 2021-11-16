import fitz
import cv2
from PIL import Image
from pyzbar.pyzbar import decode


def get_images_from_pdf(filename):
    """Retrieves images from pdf file.

    Args:
        filenma: string

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
        :obj:`string` (string).
    """
    for pix in imgs:
        if pix.width == pix.height == 300:
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            qrcode = decode(img)[0]
            return str(qrcode.data.decode())


if __name__ == "__main__":
    filename = "resources\\sdv.pdf"
    images = get_images_from_pdf(filename=filename)
    url = read_qrcode(images)
    print(url)
