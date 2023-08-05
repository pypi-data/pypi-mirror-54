# Copyright (C) 2017  DESY, Christoph Rosemann, Notkestr. 85, D-22607 Hamburg
#
# lavue is an image viewing program for photon science imaging detectors.
# Its usual application is as a live viewer using hidra as data source.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation in  version 2
# of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA  02110-1301, USA.
#
# Authors:
#     Christoph Rosemann <christoph.rosemann@desy.de>
#     Jan Kotanski <jan.kotanski@desy.de>
#

""" level widget """

from .qtuic import uic
import pyqtgraph as _pg
from pyqtgraph import QtCore, QtGui
from .histogramWidget import HistogramHLUTWidget
from . import messageBox
from . import gradientDialog
# from .histogramWidget import HistogramHLUTItem
import math
import os

_formclass, _baseclass = uic.loadUiType(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 "ui", "LevelsGroupBox.ui"))


class LevelsGroupBox(QtGui.QGroupBox):

    """
    Set minimum and maximum displayed values and its color.
    """

    #: (:class:`pyqtgraph.QtCore.pyqtSignal`) minimum level changed signal
    minLevelChanged = QtCore.pyqtSignal(float)
    #: (:class:`pyqtgraph.QtCore.pyqtSignal`) maximum level changed signal
    maxLevelChanged = QtCore.pyqtSignal(float)
    #: (:class:`pyqtgraph.QtCore.pyqtSignal`) automatic levels changed signal
    autoLevelsChanged = QtCore.pyqtSignal(int)  # bool does not work...
    #: (:class:`pyqtgraph.QtCore.pyqtSignal`) levels changed signal
    levelsChanged = QtCore.pyqtSignal()
    #: (:class:`pyqtgraph.QtCore.pyqtSignal`) color channel changed signal
    channelChanged = QtCore.pyqtSignal()
    #: (:class:`pyqtgraph.QtCore.pyqtSignal`) rgb color channel changed signal
    rgbChanged = QtCore.pyqtSignal(bool)
    #: (:class:`pyqtgraph.QtCore.pyqtSignal`) store settings requested
    storeSettingsRequested = QtCore.pyqtSignal()

    def __init__(self, parent=None, settings=None, expertmode=False):
        """ constructor

        :param parent: parent object
        :type parent: :class:`pyqtgraph.QtCore.QObject`
        :param settings: lavue configuration settings
        :type settings: :class:`lavuelib.settings.Settings`
        :param expertmode: expert mode flag
        :type expertmode: :obj:`bool`
        """
        QtGui.QGroupBox.__init__(self, parent)

        #: (:class:`Ui_LevelsGroupBox') ui_groupbox object from qtdesigner
        self.__ui = _formclass()
        self.__ui.setupUi(self)

        #: (:obj: `bool`) colors to be shown
        self.__colors = True
        #: (:obj: `bool`) auto levels enabled
        self.__auto = True
        #: (:obj: `bool`) histogram shown
        self.__histo = True
        #: (:obj: `bool`) levels shown
        self.__levels = True
        #: (:obj: `bool`) rgb flag
        self.__rgb = False
        #: (:obj: `str`) scale label
        self.__scaling = ""
        #: (:obj: `int`) red channel
        self.__rindex = 0
        #: (:obj: `int`) green channel
        self.__gindex = 1
        #: (:obj: `int`) blue channel
        self.__bindex = 2
        #: (:obj: `int`) current color channel
        self.__colorchannel = 0
        #: (:obj: `int`) number of color channels
        self.__numberofchannels = 0
        #: (:class:`lavuelib.settings.Settings`) settings
        self.__settings = settings
        #: (:obj:`bool`) expert mode
        self.__expertmode = expertmode

        #: (:obj:`dict`) channellabels
        self.__channellabels = {}
        #: (:obj:`dict` < :obj:`str`, :obj:`dict` < :obj:`str`,`any`> >
        #                custom gradients
        self.__customgradients = self.__settings.customGradients()
        for name, gradient in self.__customgradients.items():
            _pg.graphicsItems.GradientEditorItem.Gradients[name] = gradient
            self._addGradientItem(name)

        #: (:obj: `float`) minimum intensity level value
        self.__minval = 0.1
        #: (:obj: `float`) maximum intensity level value
        self.__maxval = 1.

        self.__ui.minDoubleSpinBox.setMinimum(-10e20)
        self.__ui.minDoubleSpinBox.setMaximum(10e20)
        self.__ui.maxDoubleSpinBox.setMinimum(-10e20)
        self.__ui.maxDoubleSpinBox.setMaximum(10e20)

        #: (:class: `lavuelib.histogramWidget.HistogramHLUTWidget`)
        #:      intensity histogram widget
        self.__histogram = HistogramHLUTWidget(
            bins='auto', step='auto',
            expertmode=expertmode)
        self.__ui.histogramLayout.addWidget(self.__histogram)

        self.__ui.gradientComboBox.currentIndexChanged.connect(
            self._updateGradient)
        self.setNumberOfChannels(-1)
        self.__ui.channelComboBox.currentIndexChanged.connect(self.setChannel)
        self.__ui.binsComboBox.currentIndexChanged.connect(self.setBins)
        self.__ui.rComboBox.currentIndexChanged.connect(
            self._onRChannelChanged)
        self.__ui.gComboBox.currentIndexChanged.connect(
            self._onGChannelChanged)
        self.__ui.bComboBox.currentIndexChanged.connect(
            self._onBChannelChanged)
        # self.__ui.binsComboBox.hide()
        # self.__ui.binsLabel.hide()

        self.__hideControls()
        self.__ui.autoLevelsCheckBox.stateChanged.connect(
            self._onAutoLevelsChanged)
        self.__ui.stepLineEdit.textChanged.connect(
            self._onStepChanged)
        self.__ui.autofactorLineEdit.textChanged.connect(
            self._onAutoFactorChanged)
        self.__connectHistogram()
        self.updateLevels(self.__minval, self.__maxval)
        self.__connectMinMax()

    def __connectHistogram(self):
        """ create histogram object and connect its signals
        """
        self.__histogram.item.sigLevelsChanged.connect(self._onLevelsChanged)
        self.__histogram.sigNameChanged.connect(self._changeGradient)
        self.__histogram.saveGradientRequested.connect(self._saveGradient)
        self.__histogram.removeGradientRequested.connect(self._removeGradient)

    def __disconnectHistogram(self):
        """ remove histogram object and disconnect its signals
        """
        self.__histogram.item.sigLevelsChanged.disconnect(
            self._onLevelsChanged)
        self.__histogram.sigNameChanged.disconnect(
            self._changeGradient)
        self.__histogram.saveGradientRequested.disconnect(
            self._saveGradient)
        self.__histogram.removeGradientRequested.disconnect(
            self._removeGradient)

    def updateCustomGradients(self, gradients):
        self.__customgradients = dict(gradients)
        for name, gradient in self.__customgradients.items():
            _pg.graphicsItems.GradientEditorItem.Gradients[name] = gradient
            self._addGradientItem(name)
        self.__histogram.resetGradient()
        self._updateGradient()

    def __connectMinMax(self):
        """ connects mix/max spinboxes
        """
        self.__ui.minDoubleSpinBox.valueChanged.connect(self._onMinMaxChanged)
        self.__ui.maxDoubleSpinBox.valueChanged.connect(self._onMinMaxChanged)

    def __disconnectMinMax(self):
        """ disconnects mix/max spinboxes
        """
        self.__ui.minDoubleSpinBox.valueChanged.disconnect(
            self._onMinMaxChanged)
        self.__ui.maxDoubleSpinBox.valueChanged.disconnect(
            self._onMinMaxChanged)

    @QtCore.pyqtSlot(float)
    def _onMinMaxChanged(self, _):
        """ sets region of the histograms
        """
        if not self.__auto:
            try:
                self.__disconnectMinMax()
                self._checkAndEmit()
                if self.__histo:
                    lowlim = self.__ui.minDoubleSpinBox.value()
                    uplim = self.__ui.maxDoubleSpinBox.value()
                    self.__histogram.region.setRegion([lowlim, uplim])
            finally:
                self.__connectMinMax()

    def changeView(self, showhistogram=None, showlevels=None,
                   showadd=None):
        """ shows or hides the histogram widget

        :param showhistogram: if histogram should be shown
        :type showhistogram: :obj:`bool`
        :param showlevels: if levels should be shown
        :type showlevels: :obj:`bool`
        :param showadd: if additional histogram should be shown
        :type showadd: :obj:`bool`
        """

        if showhistogram is True and self.__histo is False:
            self.__connectHistogram()
            self.__histogram.show()
            self.__histogram.fillHistogram(True)
        elif showhistogram is False and self.__histo is True:
            self.__histogram.hide()
            self.__histogram.fillHistogram(False)
            self.__disconnectHistogram()
        if showadd is True:
            self.__ui.binsComboBox.show()
            self.__ui.binsLabel.show()
            self.__ui.stepLineEdit.show()
            self.__ui.stepLabel.show()
        elif showadd is False:
            self.__ui.binsComboBox.hide()
            self.__ui.binsLabel.hide()
            self.__ui.stepLineEdit.hide()
            self.__ui.stepLabel.hide()
        if showlevels is True and self.__levels is False:
            if self.__colors:
                self.__ui.channelLabel.show()
                self.__ui.channelComboBox.show()
            else:
                self.__ui.channelLabel.hide()
                self.__ui.channelComboBox.hide()
            self.__ui.gradientLabel.show()
            self.__ui.gradientComboBox.show()
            self.__ui.scalingLabel.show()
            self.__ui.rLabel.hide()
            self.__ui.gLabel.hide()
            self.__ui.bLabel.hide()
            self.__ui.rComboBox.hide()
            self.__ui.gComboBox.hide()
            self.__ui.bComboBox.hide()
            self.__ui.autoLevelsCheckBox.show()
            self.__ui.maxDoubleSpinBox.show()
            self.__ui.maxLabel.show()
            self.__ui.minDoubleSpinBox.show()
            self.__ui.minLabel.show()
            self.__ui.scalingLabel.show()
        elif showlevels is False and self.__levels is True:
            self.__ui.channelLabel.hide()
            self.__ui.channelComboBox.hide()
            self.__ui.gradientLabel.hide()
            self.__ui.gradientComboBox.hide()
            self.__ui.rLabel.show()
            self.__ui.gLabel.show()
            self.__ui.bLabel.show()
            self.__ui.rComboBox.show()
            self.__ui.gComboBox.show()
            self.__ui.bComboBox.show()

            self.__ui.scalingLabel.hide()
            self.__ui.autoLevelsCheckBox.hide()
            self.__ui.maxDoubleSpinBox.hide()
            self.__ui.maxLabel.hide()
            self.__ui.minDoubleSpinBox.hide()
            self.__ui.minLabel.hide()
            self.__ui.scalingLabel.hide()

        if showhistogram is not None:
            self.__histo = showhistogram
        if showlevels is not None:
            self.__levels = showlevels

        if not self.__histo and not self.__levels:
            self.hide()
        else:
            self.show()

    def isAutoLevel(self):
        """ returns if automatics levels are enabled

        :returns: if automatics levels are enabled
        :rtype: :obj:`bool`
        """
        return self.__auto

    @QtCore.pyqtSlot(int)
    def setAutoLevels(self, auto):
        """enables or disables automatic levels

        :param auto: if automatics levels to be set
        :type auto: :obj:`bool` or :obj:`int`
        """
        self.__ui.autoLevelsCheckBox.setChecked(
            2 if auto else 0)
        self._onAutoLevelsChanged(auto)

    @QtCore.pyqtSlot(str)
    def _onStepChanged(self, step):
        """sets step for  automatic levels

        :param step: if automatics levels to be set
        :type step: :obj:`str`
        """
        try:
            fstep = float(step)
            if fstep <= 0:
                fstep = None
                self.__ui.stepLineEdit.setText("")
            self.__histogram.setStep(fstep)
        except Exception:
            self.__histogram.setStep(None)
            self.__ui.stepLineEdit.setText("")
        self.levelsChanged.emit()

    @QtCore.pyqtSlot(str)
    def _onAutoFactorChanged(self, factor):
        """sets factor for  automatic levels

        :param factor: if automatics levels to be set
        :type factor: :obj:`str`
        """
        try:
            ffactor = float(factor)
            if ffactor < 0:
                ffactor = 0
                self.__ui.autofactorLineEdit.setText("0")
            elif ffactor > 100:
                ffactor = 100
                self.__ui.autofactorLineEdit.setText("100")
            self.__histogram.setAutoFactor(ffactor)
            self.autoLevelsChanged.emit(1)
        except Exception:
            self.__histogram.setAutoFactor(None)
            self.autoLevelsChanged.emit(2 if self.__auto else 0)
        self.levelsChanged.emit()

    @QtCore.pyqtSlot(int)
    def _onAutoLevelsChanged(self, auto):
        """enables or disables automatic levels

        :param auto: if automatics levels to be set
        :type auto: :obj:`bool` or :obj:`int`
        """
        if auto:
            self.__auto = True
            self.__hideControls()
            factor = str(self.__ui.autofactorLineEdit.text())
            try:
                ffactor = float(factor)
                if ffactor < 0:
                    ffactor = 0
                    self.__ui.autofactorLineEdit.setText("0")
                elif ffactor > 100:
                    ffactor = 100
                    self.__ui.autofactorLineEdit.setText("100")
                self.__histogram.setAutoFactor(ffactor)
            except Exception:
                self.__histogram.setAutoFactor(None)
                self.autoLevelsChanged.emit(2)
        else:
            self.__histogram.setAutoFactor(None)
            self.__auto = False
            self.__showControls()
            self.autoLevelsChanged.emit(0)
            self._checkAndEmit()
        self.levelsChanged.emit()

    @QtCore.pyqtSlot(object)
    def _onLevelsChanged(self, histogram):
        """ set min/max level spinboxes according to histogram

        :param histogram: intensity histogram object
        :type histogram: :class: `lavuelib.histogramWidget.HistogramHLUTWidget`

        """
        levels = histogram.region.getRegion()
        lowlim = self.__ui.minDoubleSpinBox.value()
        uplim = self.__ui.maxDoubleSpinBox.value()
        if levels[0] != lowlim or levels[1] != uplim:
            self.__ui.minDoubleSpinBox.setValue(levels[0])
            self.__ui.maxDoubleSpinBox.setValue(levels[1])
            if not self.__auto:
                self._checkAndEmit()

    @QtCore.pyqtSlot()
    def _checkAndEmit(self):
        """ checks if the minimum value is actually smaller than the maximum
        """
        self.__minval = self.__ui.minDoubleSpinBox.value()
        self.__maxval = self.__ui.maxDoubleSpinBox.value()
        if self.__maxval - self.__minval <= 0:
            if self.__minval >= 1.:
                self.__minval = self.__maxval - 1.
            else:
                self.__maxval = self.__minval + 1

        self.__ui.minDoubleSpinBox.setValue(self.__minval)
        self.__ui.maxDoubleSpinBox.setValue(self.__maxval)

        self.minLevelChanged.emit(self.__minval)
        self.maxLevelChanged.emit(self.__maxval)
        self.levelsChanged.emit()

    def updateLevels(self, lowlim, uplim):
        """ set min/max level spinboxes and histogram from the parameters

        :param lowlim: minimum intensity value
        :type lowlim: :obj:`float`
        :param uplim:  maximum intensity value
        :type uplim: :obj:`float`
        """
        self.__ui.minDoubleSpinBox.setValue(lowlim)
        self.__ui.maxDoubleSpinBox.setValue(uplim)
        if self.__histo and self.__auto:
            levels = self.__histogram.region.getRegion()
            if levels[0] != lowlim or levels[1] != uplim:
                self.__histogram.region.setRegion([lowlim, uplim])

    def updateAutoLevels(self, lowlim, uplim):
        """ set min/max level spinboxes and histogram from the parameters

        :param lowlim: minimum intensity value
        :type lowlim: :obj:`float`
        :param uplim:  maximum intensity value
        :type uplim: :obj:`float`
        """
        try:
            factor = str(self.__ui.autofactorLineEdit.text())
            float(factor)
            llim, ulim = self.__histogram.getFactorRegion()
            if llim is not None and ulim is not None:
                self.updateLevels(llim, ulim)
                self.minLevelChanged.emit(llim)
                self.maxLevelChanged.emit(ulim)
            else:
                self.updateLevels(lowlim, uplim)
        except Exception:
            self.updateLevels(lowlim, uplim)

    def __hideControls(self):
        """ disables spinboxes
        """
        self.__ui.minDoubleSpinBox.setEnabled(False)
        self.__ui.maxDoubleSpinBox.setEnabled(False)
        self.__ui.autofactorLineEdit.setEnabled(True)
        self.__ui.autofactorLabel.setEnabled(True)

    def __showControls(self):
        """ enables spinboxes
        """
        self.__ui.minDoubleSpinBox.setEnabled(True)
        self.__ui.maxDoubleSpinBox.setEnabled(True)
        self.__ui.autofactorLineEdit.setEnabled(False)
        self.__ui.autofactorLabel.setEnabled(False)

    @QtCore.pyqtSlot(str)
    def setScalingLabel(self, scalingtype):
        """ sets scaling label

        :param scalingtype: scaling type, i.e. log, linear, sqrt
        :type scalingtype: :obj:`str`
        """
        lowlim = float(self.__ui.minDoubleSpinBox.value())
        uplim = float(self.__ui.maxDoubleSpinBox.value())
        if scalingtype == "log":
            if scalingtype != self.__scaling:
                self.__ui.scalingLabel.setText("log scale!")
                if not self.__auto:
                    if self.__scaling == "linear":
                        lowlim = math.log10(
                            lowlim or 10e-3) if lowlim > 0 else -2
                        uplim = math.log10(
                            uplim or 10e-3) if uplim > 0 else -2
                    elif self.__scaling == "sqrt":
                        lowlim = math.log10(
                            lowlim * lowlim or 10e-3) if lowlim > 0 else -2
                        uplim = math.log10(
                            uplim * uplim or 10e-3) if uplim > 0 else -2
        elif scalingtype == "linear":
            if scalingtype != self.__scaling:
                self.__ui.scalingLabel.setText("linear scale!")
                if not self.__auto:
                    if self.__scaling == "log":
                        lowlim = math.pow(10, lowlim)
                        uplim = math.pow(10, uplim)
                    elif self.__scaling == "sqrt":
                        lowlim = lowlim * lowlim
                        uplim = uplim * uplim
        elif scalingtype == "sqrt":
            if scalingtype != self.__scaling:
                self.__ui.scalingLabel.setText("sqrt scale!")
                if not self.__auto:
                    if self.__scaling == "linear":
                        lowlim = math.sqrt(max(lowlim, 0))
                        uplim = math.sqrt(max(uplim, 0))
                    elif self.__scaling == "log":
                        lowlim = math.sqrt(max(math.pow(10, lowlim), 0))
                        uplim = math.sqrt(max(math.pow(10, uplim), 0))
        if scalingtype != self.__scaling:
            self.__scaling = scalingtype
        if not self.__auto:
            if self.__histo:
                self.__histogram.region.setRegion([lowlim, uplim])
            else:
                self.__ui.minDoubleSpinBox.setValue(lowlim)
                self.__ui.maxDoubleSpinBox.setValue(uplim)

    @QtCore.pyqtSlot(int)
    def setChannel(self, channel):
        """ sets color channel

        :param channel: color channel
        :type channel: :obj:`int`
        """
        if self.__colorchannel != channel:
            if channel >= 0 and channel <= self.__numberofchannels + 2:
                if channel == self.__numberofchannels + 2 \
                   and self.__colorchannel != channel:
                    self.__colorchannel = channel
                    self.__histogram.setRGB(True)
                    self.showGradient(False)
                    self.rgbChanged.emit(True)
                elif (self.__colorchannel == self.__numberofchannels + 2
                      and self.__colorchannel != channel):
                    self.__colorchannel = channel
                    self.__histogram.setRGB(False)
                    self.showGradient(True)
                    self.rgbChanged.emit(False)
                else:
                    self.__colorchannel = channel
                    self.__histogram.setRGB(False)
                    self.channelChanged.emit()

    def showGradient(self, status=True):
        """ resets color channel

        :param status: show gradient flag
        :type status: :obj:`bool`
        """
        if status:
            self.__ui.gradientComboBox.show()
            self.__ui.gradientLabel.show()
            self.__histogram.gradient.show()
            self.__ui.rLabel.hide()
            self.__ui.gLabel.hide()
            self.__ui.bLabel.hide()
            self.__ui.rComboBox.hide()
            self.__ui.gComboBox.hide()
            self.__ui.bComboBox.hide()
            self._updateGradient()
        else:
            self.__ui.gradientComboBox.hide()
            self.__ui.gradientLabel.hide()
            self.__histogram.gradient.hide()
            self.__ui.rLabel.show()
            self.__ui.gLabel.show()
            self.__ui.bLabel.show()
            self.__ui.rComboBox.show()
            self.__ui.gComboBox.show()
            self.__ui.bComboBox.show()

    @QtCore.pyqtSlot(int)
    def _onRChannelChanged(self, index):
        """ set red channel
        """
        if index < self.__numberofchannels:
            self.__rindex = index
        else:
            self.__rindex = -1
        self.channelChanged.emit()

    @QtCore.pyqtSlot(int)
    def _onGChannelChanged(self, index):
        """ set green channel
        """
        if index < self.__numberofchannels:
            self.__gindex = index
        else:
            self.__gindex = -1
        self.channelChanged.emit()

    @QtCore.pyqtSlot(int)
    def _onBChannelChanged(self, index):
        """ set blue channel
        """
        if index < self.__numberofchannels:
            self.__bindex = index
        else:
            self.__bindex = -1
        self.channelChanged.emit()

    def updateChannelLabels(self, chlabels):
        """ update red channel

        :param chlabels: dictionary with channel labels
        :type chlabels: :obj:`dict` <:obj:`int` :obj:`str`>
        """
        if isinstance(chlabels, dict):
            for ky, vl in chlabels.items():
                if not vl:
                    if ky in self.__channellabels.keys():
                        self.__channellabels.pop(ky)
                else:
                    try:
                        self.__channellabels[int(ky)] = vl
                        self.setChannelItemText(ky, vl)
                    except Exception as e:
                        print(str(e))

    def setChannelItemText(self, iid, text):
        """ sets channel item text

        :param iid: label id
        :type iid: :obj:`int`
        :param iid: label text
        :type iid: :obj:`str`
        """
        self.__ui.channelComboBox.setItemText(
            iid + 1, text)
        self.__ui.channelComboBox.setItemData(
            iid + 1, text, QtCore.Qt.ToolTipRole)

    def updateRChannel(self):
        """ update red channel
        """
        current = self.__ui.rComboBox.currentIndex()
        if self.__rindex != self.__numberofchannels:
            if self.__rindex != current:
                self.__ui.rComboBox.setCurrentIndex(self.__rindex)
        elif self.__rindex != -1:
            self.__ui.rComboBox.setCurrentIndex(self.__numberofchannels)

    def updateGChannel(self):
        """ update green channel
        """
        current = self.__ui.gComboBox.currentIndex()
        if self.__gindex != self.__numberofchannels:
            if self.__gindex != current:
                self.__ui.gComboBox.setCurrentIndex(self.__gindex)
        elif self.__gindex != -1:
            self.__ui.gComboBox.setCurrentIndex(self.__numberofchannels)

    def updateBChannel(self):
        """ update blue channel
        """
        current = self.__ui.bComboBox.currentIndex()
        if self.__bindex != self.__numberofchannels:
            if self.__bindex != current:
                self.__ui.bComboBox.setCurrentIndex(self.__bindex)
        elif self.__bindex != -1:
            self.__ui.bComboBox.setCurrentIndex(self.__numberofchannels)

    def rgbchannels(self):
        return (self.__rindex, self.__gindex, self.__bindex)

    @QtCore.pyqtSlot(int)
    def setBins(self, index):
        """ sets bins edges algorithm for histogram

        :param index: bins edges algorithm index for histogram
        :type index: :obj:`int`
        """
        self.__histogram.setBins(
            self.__ui.binsComboBox.itemText(index))
        self.levelsChanged.emit()

    def colorChannel(self):
        """ provides color channel

        :returns: color channel
        :rtype: :obj:`int`
        """
        return self.__colorchannel

    def setNumberOfChannels(self, number):
        """ sets maximum number of color channel

        :param number:  number of color channel
        :type number: :obj:`int`
        """
        if number != self.__numberofchannels:
            self.__numberofchannels = int(max(number, 0))
            if self.__numberofchannels > 0:
                for i in reversed(
                        range(0, self.__ui.channelComboBox.count())):
                    self.__ui.channelComboBox.removeItem(i)
                self.__ui.channelComboBox.addItem("sum")
                # self.__ui.channelComboBox.setSizeAdjustPolicy(
                # QtGui.QComboBox.AdjustToMinimumContentsLength)
                self.__ui.channelLabel.show()
                self.__ui.channelComboBox.show()
                self.__ui.channelComboBox.setSizeAdjustPolicy(
                    QtGui.QComboBox.AdjustToContents)

                self.__ui.channelComboBox.addItems(
                    ["channel %s" % (ch)
                     for ch in range(self.__numberofchannels)])

                for ky, vl in self.__channellabels.items():
                    if vl and ky < self.__numberofchannels:
                        self.setChannelItemText(ky, vl)
                self.__ui.channelComboBox.addItem("mean")
                self.__ui.channelComboBox.addItem("RGB")
                self.__colors = True
                for i in reversed(
                        range(0, self.__ui.rComboBox.count())):
                    self.__ui.rComboBox.removeItem(i)
                for i in reversed(
                        range(0, self.__ui.gComboBox.count())):
                    self.__ui.gComboBox.removeItem(i)
                for i in reversed(
                        range(0, self.__ui.bComboBox.count())):
                    self.__ui.bComboBox.removeItem(i)

                self.__ui.rComboBox.addItems(
                    ["%s" % (ch)
                     for ch in range(self.__numberofchannels)])
                self.__ui.bComboBox.addItems(
                    ["%s" % (ch)
                     for ch in range(self.__numberofchannels)])
                self.__ui.gComboBox.addItems(
                    ["%s" % (ch)
                     for ch in range(self.__numberofchannels)])
                self.__ui.rComboBox.addItem("None")
                self.__ui.bComboBox.addItem("None")
                self.__ui.gComboBox.addItem("None")
                self.__rindex = 0
                if self.__numberofchannels > 1:
                    self.__gindex = 1
                else:
                    self.__gindex = -1
                if self.__numberofchannels > 2:
                    self.__bindex = 2
                else:
                    self.__bindex = -1
                self.updateRChannel()
                self.updateGChannel()
                self.updateBChannel()
            else:
                self.__ui.channelLabel.hide()
                self.__ui.channelComboBox.hide()
                self.__colors = False

    def gradient(self):
        """ provides the current color gradient

        :returns:  gradient name
        :rtype: :obj:`str`
        """
        return str(self.__ui.gradientComboBox.currentText())

    @QtCore.pyqtSlot()
    def _saveGradient(self):
        """ saves the current gradient
        """
        graddlg = gradientDialog.GradientDialog()
        graddlg.protectednames = list(
            set(_pg.graphicsItems.GradientEditorItem.Gradients.keys()) -
            set(self.__customgradients.keys())
        )
        graddlg.createGUI()
        if graddlg.exec_():
            if graddlg.name:
                name = graddlg.name
                gradient = self.__histogram.gradient.getCurrentGradient()
                self.__customgradients[name] = gradient
                _pg.graphicsItems.GradientEditorItem.Gradients[name] = gradient
                self._addGradientItem(name)
                self.__histogram.resetGradient()
                self.setGradient(name)
                self._updateGradient()
                self.__settings.setCustomGradients(self.__customgradients)
                self.storeSettingsRequested.emit()

    @QtCore.pyqtSlot()
    def _removeGradient(self):
        """ removes the current gradient
        """
        name = str(self.gradient())

        if name in self.__customgradients:
            if QtGui.QMessageBox.question(
                    self, "Removing Label",
                    'Would you like  to remove "%s"" ?' %
                    (name),
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                    QtGui.QMessageBox.Yes) == QtGui.QMessageBox.No:
                return False
            self.__customgradients.pop(name)
            _pg.graphicsItems.GradientEditorItem.Gradients.pop(name)
            self._removeGradientItem(name)
            self.__histogram.resetGradient()
            self.__settings.setCustomGradients(self.__customgradients)
            self.storeSettingsRequested.emit()
        else:
            messageBox.MessageBox.warning(
                self, "Gradient: '%s' cannot be removed" % str(name),
                None, None)

    def _addGradientItem(self, name):
        """ sets gradient

        :param name  gradient name
        :type name: :obj:`str`
        """
        cid = self.__ui.gradientComboBox.findText(name)
        if cid < 0:
            self.__ui.gradientComboBox.addItem(name)

    def _removeGradientItem(self, name):
        """ removes gradient

        :param name  gradient name
        :type name: :obj:`str`
        """
        cid = self.__ui.gradientComboBox.findText(name)
        if cid > -1:
            self.__ui.gradientComboBox.removeItem(cid)
            self._updateGradient(0)
        else:
            print("Error %s" % name)

    def setGradient(self, name):
        """ sets gradient

        :param name  gradient name
        :type name: :obj:`str`
        """
        self._changeGradient(name)

    @QtCore.pyqtSlot(int)
    def _updateGradient(self, index=-1):
        """ updates gradient in the intensity histogram

        :param index: gradient index
        :type index: :obj:`int`
        """
        if index == -1:
            name = self.__ui.gradientComboBox.currentText()
            index = self.__ui.gradientComboBox.findText(name)
        self.__histogram.setGradientByName(
            self.__ui.gradientComboBox.itemText(index))

    @QtCore.pyqtSlot(str)
    def _changeGradient(self, name):
        """ updates the gradient combobox

        :param name: gradient name
        :type name: :obj:`str`
        """
        text = self.__ui.gradientComboBox.currentText()
        if text != name:
            cid = self.__ui.gradientComboBox.findText(name)
            if cid > -1:
                self.__ui.gradientComboBox.setCurrentIndex(cid)
            else:
                print("Error %s" % name)

    def updateHistoImage(self, autoLevel=None):
        """ executes imageChanged of histogram with the givel autoLevel

        :param autoLevel: if automatics levels to be set
        :type autoLevel: :obj:`bool`
        """
        auto = autoLevel if autoLevel is not None else self.__auto
        self.__histogram.imageChanged(autoLevel=auto)

    def setImageItem(self, image):
        """ sets histogram image

        :param image: histogram image
        :type image: :class:`pyqtgraph.graphicsItems.ImageItem.ImageItem`
        """
        self.__histogram.setImageItem(image)

    def levels(self):
        """ provides levels from configuration string

        :returns:  configuration string: lowlim,uplim
        :rtype: :obj:`str`
        """
        lowlim = self.__ui.minDoubleSpinBox.value()
        uplim = self.__ui.maxDoubleSpinBox.value()
        return "%s,%s" % (lowlim, uplim)

    def setLevels(self, cnflevels):
        """ set levels from configuration string

        :param cnflevels:  configuration string: lowlim,uplim
        :type cnflevels: :obj:`str`
        """
        self.__ui.autoLevelsCheckBox.setChecked(False)
        self._onAutoLevelsChanged(0)
        llst = cnflevels.split(",")
        lmin = None
        lmax = None
        try:
            smin = llst[0]
            if smin.startswith("m"):
                smin = "-" + smin[1:]
            lmin = float(smin)
        except Exception:
            pass
        try:
            smax = llst[1]
            if smax.startswith("m"):
                smax = "-" + smax[1:]
            lmax = float(smax)
        except Exception:
            pass
        self.updateLevels(lmin, lmax)

    def autoFactor(self):
        """ provides factor for automatic levels

        :returns: factor for automatic levels
        :rtype: :obj:`str`
        """
        return str(self.__ui.autofactorLineEdit.text())

    def setAutoFactor(self, factor):
        """ sets factor for automatic levels

        :param factor: factor for automatic levels
        :type factor: :obj:`str`
        """
        self.__ui.autofactorLineEdit.setText(factor)
        if factor:
            self.setAutoLevels(2)
        self._onAutoFactorChanged(factor)
