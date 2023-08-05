# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ImageViewTemplate.ui'
#
# Created: Sun Sep 18 19:17:41 2016
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(726, 588)
        self.gridLayout_3 = QtWidgets.QGridLayout(Form)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.splitter = QtWidgets.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.graphicsView = GraphicsView(self.layoutWidget)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 0, 0, 2, 1)
        self.histogram = HistogramLUTWidget(self.layoutWidget)
        self.histogram.setObjectName("histogram")
        self.gridLayout.addWidget(self.histogram, 0, 1, 1, 2)
        self.roiBtn = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.roiBtn.sizePolicy().hasHeightForWidth())
        self.roiBtn.setSizePolicy(sizePolicy)
        self.roiBtn.setCheckable(True)
        self.roiBtn.setObjectName("roiBtn")
        self.gridLayout.addWidget(self.roiBtn, 1, 1, 1, 1)
        self.menuBtn = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.menuBtn.sizePolicy().hasHeightForWidth())
        self.menuBtn.setSizePolicy(sizePolicy)
        self.menuBtn.setObjectName("menuBtn")
        self.gridLayout.addWidget(self.menuBtn, 1, 2, 1, 1)
        self.roiPlot = PlotWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.roiPlot.sizePolicy().hasHeightForWidth())
        self.roiPlot.setSizePolicy(sizePolicy)
        self.roiPlot.setMinimumSize(QtCore.QSize(0, 40))
        self.roiPlot.setObjectName("roiPlot")
        self.gridLayout_3.addWidget(self.splitter, 0, 0, 1, 1)
        self.normGroup = QtWidgets.QGroupBox(Form)
        self.normGroup.setObjectName("normGroup")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.normGroup)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.normSubtractRadio = QtWidgets.QRadioButton(self.normGroup)
        self.normSubtractRadio.setObjectName("normSubtractRadio")
        self.gridLayout_2.addWidget(self.normSubtractRadio, 0, 2, 1, 1)
        self.normDivideRadio = QtWidgets.QRadioButton(self.normGroup)
        self.normDivideRadio.setChecked(False)
        self.normDivideRadio.setObjectName("normDivideRadio")
        self.gridLayout_2.addWidget(self.normDivideRadio, 0, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.normGroup)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.normGroup)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.normGroup)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 2, 0, 1, 1)
        self.normROICheck = QtWidgets.QCheckBox(self.normGroup)
        self.normROICheck.setObjectName("normROICheck")
        self.gridLayout_2.addWidget(self.normROICheck, 1, 1, 1, 1)
        self.normXBlurSpin = QtWidgets.QDoubleSpinBox(self.normGroup)
        self.normXBlurSpin.setObjectName("normXBlurSpin")
        self.gridLayout_2.addWidget(self.normXBlurSpin, 2, 2, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.normGroup)
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 2, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.normGroup)
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 2, 3, 1, 1)
        self.normYBlurSpin = QtWidgets.QDoubleSpinBox(self.normGroup)
        self.normYBlurSpin.setObjectName("normYBlurSpin")
        self.gridLayout_2.addWidget(self.normYBlurSpin, 2, 4, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.normGroup)
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 2, 5, 1, 1)
        self.normOffRadio = QtWidgets.QRadioButton(self.normGroup)
        self.normOffRadio.setChecked(True)
        self.normOffRadio.setObjectName("normOffRadio")
        self.gridLayout_2.addWidget(self.normOffRadio, 0, 3, 1, 1)
        self.normTimeRangeCheck = QtWidgets.QCheckBox(self.normGroup)
        self.normTimeRangeCheck.setObjectName("normTimeRangeCheck")
        self.gridLayout_2.addWidget(self.normTimeRangeCheck, 1, 3, 1, 1)
        self.normFrameCheck = QtWidgets.QCheckBox(self.normGroup)
        self.normFrameCheck.setObjectName("normFrameCheck")
        self.gridLayout_2.addWidget(self.normFrameCheck, 1, 2, 1, 1)
        self.normTBlurSpin = QtWidgets.QDoubleSpinBox(self.normGroup)
        self.normTBlurSpin.setObjectName("normTBlurSpin")
        self.gridLayout_2.addWidget(self.normTBlurSpin, 2, 6, 1, 1)
        self.gridLayout_3.addWidget(self.normGroup, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.roiBtn.setText(QtWidgets.QApplication.translate("Form", "ROI", None, -1))
        self.menuBtn.setText(QtWidgets.QApplication.translate("Form", "Menu", None, -1))
        self.normGroup.setTitle(QtWidgets.QApplication.translate("Form", "Normalization", None, -1))
        self.normSubtractRadio.setText(QtWidgets.QApplication.translate("Form", "Subtract", None, -1))
        self.normDivideRadio.setText(QtWidgets.QApplication.translate("Form", "Divide", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("Form", "Operation:", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("Form", "Mean:", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("Form", "Blur:", None, -1))
        self.normROICheck.setText(QtWidgets.QApplication.translate("Form", "ROI", None, -1))
        self.label_8.setText(QtWidgets.QApplication.translate("Form", "X", None, -1))
        self.label_9.setText(QtWidgets.QApplication.translate("Form", "Y", None, -1))
        self.label_10.setText(QtWidgets.QApplication.translate("Form", "T", None, -1))
        self.normOffRadio.setText(QtWidgets.QApplication.translate("Form", "Off", None, -1))
        self.normTimeRangeCheck.setText(QtWidgets.QApplication.translate("Form", "Time range", None, -1))
        self.normFrameCheck.setText(QtWidgets.QApplication.translate("Form", "Frame", None, -1))

from ..widgets.HistogramLUTWidget import HistogramLUTWidget
from ..widgets.PlotWidget import PlotWidget
from ..widgets.GraphicsView import GraphicsView
