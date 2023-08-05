#! /usr/bin/env python
# -*- coding: utf-8 -*-


from loguru import logger

# import funkcí z jiného adresáře
# import sys
import os.path as op
import pytest

# import copy

import unittest

# sample_data_path = os.path.dirname(os.path.abspath(__file__))
# sample_data_path
# sys.path.append(os.path.join(path_to_script, "../extern/pyseg_base/src/"))
# sys.path.append(os.path.join(path_to_script, "../extern/py3DSeedEditor/"))
# sys.path.append(os.path.join(path_to_script, "../src/"))

from PyQt5.QtWidgets import QFileDialog, QApplication, QMainWindow
import sys

import numpy as np

try:
    import dicom as pydicom

    pydicom.debug(False)
except:
    import pydicom

    pydicom.config.debug(False)

from distutils.version import LooseVersion

#
import io3d
import io3d.dcmreaddata as dcmr
import io3d.fsbrowser

sample_data_path = "~/data/medical/orig/sample_data/"
sample_data_path = op.expanduser(sample_data_path)


class FileSystemBrowserTest(unittest.TestCase):

    # @unittest.skip('waiting for implementation')
    @unittest.skipIf(
        LooseVersion(pydicom.__version__) < LooseVersion("1.0.0"),
        "Data from pydicom >= 1.0.0 required",
    )
    def test_fsbrowser_path_info(self):
        import pydicom.data

        # filepath = pydicom.data.get_testdata_files('DICOMDIR')[0]
        filepath = op.join(
            pydicom.data.DATA_ROOT, "test_files/dicomdirtests/98892001/CT2N"
        )
        fsb = io3d.fsbrowser.FileSystemBrowser(filepath)
        dirlist = fsb.get_path_info(filepath)
        # weak test - TODO..
        self.assertTrue("name: CT2N" in dirlist[0])
        self.assertTrue("type: .dir" in dirlist[1])
        self.assertTrue("Preview of files in dir: CT2N" in dirlist[2])
        self.assertTrue("test_files/dicomdirtests/98892001/CT2N" in dirlist[6])

    #  comment next line if you want to run the test
    # @unittest.skip('waiting for implementation')
    @unittest.skipIf(
        LooseVersion(pydicom.__version__) < LooseVersion("1.0.0"),
        "Data from pydicom >= 1.0.0 required",
    )
    def test_fsbrowser_dir_list(self):

        import pydicom.data

        # TODO make test stronger
        # filepath = pydicom.data.get_testdata_files('DICOMDIR')[0]
        filepath = op.join(
            pydicom.data.DATA_ROOT, "test_files/dicomdirtests/98892001/CT2N"
        )
        # filepath = io3d.datasets.join_path("3Dircadb1.1/PATIENT_DICOM")
        # filepath = io3d.datasets.join_path("jatra_5mm")
        fsb = io3d.fsbrowser.FileSystemBrowser(filepath)
        dirlist = fsb.get_dir_list()
        self.assertTrue("path" in dirlist[0])
        self.assertTrue("name" in dirlist[0])

    # @unittest.skip("technology test")
    # @pytest.mark.skip("technology test")
    @pytest.mark.interactive
    def test_devel_qt_dialog_fsbrowser(self):
        import sys
        from PyQt5.QtWidgets import (
            QApplication,
            QWidget,
            QLineEdit,
            QPushButton,
            QLabel,
        )
        from PyQt5.QtGui import QImage, QPixmap
        import matplotlib.pyplot as plt

        # Create an PyQT4 application object.
        a = QApplication(sys.argv)

        # The QWidget widget is the base class of all user interface objects in PyQt4.
        w = QWidget()

        # Set window size.
        w.resize(320, 240)

        # Set window title
        w.setWindowTitle("Hello World!")

        qfd = QFileDialog(None)
        qfd.setOption(QFileDialog.DontUseNativeDialog)

        lineedit = QLineEdit(qfd)
        # Create a button in the window
        button = QPushButton("Click me", qfd)

        # Image
        image = io3d.datasets.generate_face([1, 100, 100]).squeeze()

        cmap = np.uint8(np.round(255 * plt.get_cmap("magma")(np.arange(256))))
        image /= image.max()
        image = np.minimum(image, 1.0)
        image = np.round(255 * image).astype("uint8")
        Y, X = image.shape
        self._bgra = np.zeros((Y, X, 4), dtype=np.uint8, order="C")
        self._bgra[..., 0] = cmap[:, 2][image]
        self._bgra[..., 1] = cmap[:, 1][image]
        self._bgra[..., 2] = cmap[:, 0][image]
        qimage = QImage(self._bgra.data, X, Y, QImage.Format_RGB32)

        pixmap = QPixmap.fromImage(qimage)

        label = QLabel(w)
        # pixmap = QPixmap(os.getcwd() + 'https://pythonspot-9329.kxcdn.com/logo.png')
        label.setPixmap(pixmap)
        w.resize(pixmap.width(), pixmap.height())
        # success = img.loadFromData(image_data)
        # painter = QPainter(img)
        layout = qfd.layout()

        layout.addWidget(lineedit)
        layout.addWidget(button, 2, 5)
        layout.addWidget(label, 1, 5)

        def process_selected_file(filename):
            print("print_all")
            print(filename)
            lineedit.setText(filename)

        qfd.currentChanged.connect(process_selected_file)

        if qfd.exec_():
            print(qfd.selectedFiles())
        else:
            print("Cancel")

        # a.exec_()

    def test_remove(self):
        fn = "try_to_remove.txt"
        io3d.remove_if_exists(fn)
        with open(fn, "w") as f:
            f.write("ahoj")

        io3d.remove_if_exists(fn)

        self.assertFalse(op.exists(fn))


if __name__ == "__main__":
    unittest.main()
