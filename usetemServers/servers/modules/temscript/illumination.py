from comtypes.gen import TEMScripting
from .stemDetectors import STEMDetectors
from .enums import *
from comtypes import CoCreateInstance
from comtypes.safearray import safearray_as_ndarray
import numpy as np
import logging
try:
    from comtypes.gen.IOMLib import _99A162A6_3022_4B64_88C3_A62A6BE22239_0_1_0 as IOMLib
except:
    GetModule(['{99A162A6-3022-4B64-88C3-A62A6BE22239}',1,0])
    from comtypes.gen.IOMLib import _99A162A6_3022_4B64_88C3_A62A6BE22239_0_1_0 as IOMLib

class Illumination():

    _instrument = None

    def __init__(self, instrument,parent=None):
        self._instrument = instrument
        self._illum = instrument.Illumination
        self._iom3 = instrument.iom3
        self._parent = parent

    def rotationCenter(self):


        if value is None:
            return self._illum.RotationCenter
        else:
            self._illum.RotationCenter = vector(self._instrument, value)

    def mode(self, value=None):
        if value is None:
            return self._illum.mode
        else:
            self._illum.Mode = value

    def dfMode(self, value=None):
        if value is None:
            return self._illum.DFMode
        else:
            self._illum.DFMode = value

    def isBeamBlanked(self, value=None):
        if value is None:
            return self._illum.BeamBlanked
        elif type(value) is bool:
            print(value)
            self._illum.BeamBlanked = value


    def condenserStigmator(self):
        if value is None:
            return self._illum.CondenserStigmator
        else:
            self._illum.CondenserStigmator = vector(self._instrument, value)

    def spotSizeIndex(self, value=None):
        if value is None:
            return self._illum.SpotSizeIndex
        else:
            self._illum.SpotSizeIndex = int(value)


    def intensity(self, value=None):
        if value is None:
            return self._illum.Intensity
        else:
            self._illum.Intensity = value

    def c3ImageDistanceParallelOffset(self, value=None):
        if value is None:
            return self._illum.C3ImageDistanceParallelOffset
        else:
            self._illum.C3ImageDistanceParallelOffset = value


    def isIntensityZoomEnabled(self, value=None):
        if value is None:
            return self._illum.IntensityZoomEnabled
        elif type(value) is bool:
            self._illum.IntensityZoomEnabled = value

    def isIntensityLimitEnabled(self, value=None):
        if value is None:
            return self._illum.IntensityLimitEnabled
        elif type(value) is bool:
            self._illum.IntensityLimitEnabled = value

    def beamShift(self, value=None, raw=False):
        defl = self._iom3.Column.Optics.Deflectors
        beam = defl[IOMLib.enDeflector_BeamDcDeflector].QueryInterface(IOMLib.IBeamDcDeflector)

        if raw:
            shift = beam.rawshift
        else:
            shift = beam.shift

        if value is None:
            return (shift.x, shift.y)
        else:
            shift.x = value[0]
            shift.y = value[1]
            if raw:
                beam.rawshift = shift
            else:
                beam.shift = shift


    def imageShift(self):
        if value is None:
            return self._illum.Shift
        else:
            print(self._illum.Shift)
            self._illum.Shift = vector(self._instrument, value)

    def stemRotation(self, value=None):
        if value is None:
            return self._illum.StemRotation * 180/np.pi
        else:
            self._illum.StemRotation = value * np.pi/180

    def stemMagnification(self, value=None):

        if value is None or value is '':
            return self._illum.StemMagnification
        else:
            if isinstance(value, str):
                value = float(value)
            self._illum.StemMagnification = value

    def tilt(self,value=None):
        if value is None:
            return self._illum.Tilt
        else:
            self._illum.Tilt = vector(self._instrument, value)

    def condenserMode(self, value=None):

        if value is None:
            return self._illum.CondenserMode
        else:
            self._illum.CondenserMode = value

    def illuminatedArea(self, value=None):

        if value is None:
            return self._illum.IlluminatedArea
        else:
            self._illum.IlluminatedArea = value

    def probeDefocus(self, value=None):
        """
        Probe mode only, not in STEM
        """

        if value is None:
            return self._illum.ProbeDefocus
        else:
            self._illum.ProbeDefocus = value

    def STEMDefocus(self,value=None, lens=None):
        """

        """

       # logging.info('Product Family'+str(self._parent.configInfo('ProductFamily')))


        if self._parent.configInfo('ProductFamily') == IOMLib.enProductFamily_Titan: # Titan Product Family
            if value is None:
                return self._iom3.Column.Optics.StemFocus.GetObjectiveDefocus()
            else:
                self._iom3.Column.Optics.StemFocus.SetObjectiveDefocus(value)
        elif self._parent.configInfo('ProductFamily') == IOMLib.enProductFamily_Talos:

            if value is None:
                return self._iom3.Column.Optics.StemFocus.GetObjectiveDefocus()
            else:
                self._iom3.Column.Optics.StemFocus.SetObjectiveDefocus(value)






    def convergenceAngle(self):
        """
        Not clear this is actually doing anything

        """
        return self._illum.ConvergenceAngle
