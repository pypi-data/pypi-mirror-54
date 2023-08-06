# Basic imports
import io
import numpy as np
import pandas as pd
from urllib.request import urlopen
from PIL import Image

# 3-rd party imports
from PyQt5.QtCore import QFile, QIODevice
import rasterio

# self import
from .lib import *

def loadImg(path):
    """
    ----------
    Parameters
    ----------
    path : str
           path to the image file 

    -------
    Returns
    -------
    npImg : 3-d ndarray encoded in UINT8

    """

    # rasObj = rasterio.open(path)
    # nCh = rasObj.count
    # obj = initProgress(nCh, "loading channel 1")
    # if nCh < 3:
    #     npImg = np.zeros((rasObj.height, rasObj.width, 3), dtype="uint8")
    #     for i in range(3):
    #         npImg[:, :, i] = rasObj.read(1)
    #         updateProgress(obj, 1, "loading channel %d" %
    #                        (i+2 if i != (nCh-1) else i+1))
    # else:
    #     npImg = np.zeros((rasObj.height, rasObj.width, nCh), dtype="uint8")
    #     for i in range(nCh):
    #         npImg[:, :, i] = rasObj.read(i + 1)
    #         updateProgress(obj, "loading channel %d" % (i+2) if i != (nCh-1) else "Done")

    # return npImg

    rasObj = rasterio.open(path)
    nCh = rasObj.count
    prog = initProgress(nCh, name="Loading channel 1")
    if nCh < 3:
        npImg = np.zeros((rasObj.height, rasObj.width, 3), dtype="uint8")
        for i in range(3):
            npImg[:, :, i] = rasObj.read(1)
            if i != nCh-1:
                updateProgress(prog, name="Loading channel %d" % (i+2))
            else:
                updateProgress(prog, name="Done")
    else:
        npImg = np.zeros((rasObj.height, rasObj.width, nCh), dtype="uint8")
        for i in range(nCh):
            npImg[:, :, i] = rasObj.read(i + 1)
            if i != nCh-1:
                updateProgress(prog, name="Loading channel %d" % (i+2))
            else:
                updateProgress(prog, name="Done")

    return npImg

def loadImgWeb(URL):
    """
    ----------
    Parameters
    ----------
    URL : str
          URL to the UINT8-encoded image file 

    -------
    Returns
    -------
    npImg : 3-d ndarray encoded in UINT8

    """

    with urlopen(URL)as url:
        file = io.BytesIO(url.read())
        npImg = np.array(Image.open(file), dtype="uint8")

    return npImg


def loadMap(path):
    """
    ----------
    Parameters
    ----------
    path : str
           path to the csv file 

    -------
    Returns
    -------
    pdMap : Pandas dataframe or None if path is empty

    """

    try:
        pdMap = pd.read_csv(path, header=None)
    except Exception as e:
        pdMap = None

    return pdMap


def saveQImg(qimg, path):
    """
    ----------
    Parameters
    ----------
    qimg : qimage
            
    path : str
           path to the destination
    -------
    Returns
    -------
    None

    """
    
    qfile = QFile(path + ".jpg")
    qfile.open(QIODevice.WriteOnly)
    qimg.save(qfile, "JPG")
    qfile.close()
