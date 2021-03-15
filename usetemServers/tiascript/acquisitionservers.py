import logging
from .enums import *
from .application import *



logging.basicConfig(level=logging.INFO)

class AcquisitionServer():

    def __init__(self,app,classType):
        self.app = app
        self.server = getattr(app, classType)

    def biasCorrection(self):
        pass

    def gainCorrection(self):
        pass

    def seriesSize(self, size=None):

        if size is None:
            return self.server.SeriesSize
        else:
            self.server.SeriesSize = size
            logging.info(f'Series size set as {size}')

class ImageServer(AcquisitionServer):

    def __init__(self,app):
            self.app = app
            self.server = app.ScanningServer()

    def beamPosition(self, pos=None):
        if pos is None:
            pos2d = self.server.BeamPosition
            return (pos2d.X, pos2d.Y)
        else:
            self.server.BeamPosition = self.app.Position2D(pos[0], pos[1])
            logging.debug(f'Beam Position moved to {pos}')

    def acquireMode(self, mode=None):

        if mode is None:
            return AcquireModes(self.server.AcquireMode).name
        else:
            self.server.AcquireMode = mode
            logging.info(f'Acquire mode is now {AcquireModes(mode).name}')

    def createMagnification(self, mag, imageRange, modeString):

        mMode = MicroscopeModes[modeString].value
        self.server.CreateMagnification(mag, esvision.Range2D(imageRange),mMode)

    def deleteMagnification(self, name, modeString):
        mMode = MicroscopeModes[modeString].value
        self.server.DeleteMagnification(name, mMode)


    def driftRateX(self, value=None):

        if value is None:
            return self.server.DriftRateX
        else:
            self.server.DriftRateX = value
            logging.debug(f'DwellTime set as {value}')

    def driftRateY(self, value=None):

        if value is None:
            return self.server.DriftRateY
        else:
            self.server.DriftRateY = value
            logging.debug(f'DwellTime set as {value}')


    def MagnificationName(self, mag, microscopeModeString):
        return self.server.MagnificationName(mag, MicroscopeModes[microscopeModeString].value)

    def MagnificationNames(self, microscopeModeString):

        names = self.server.MagnificationNames(MicroscopeModes[microscopeModeString].value)

        namesList = list()
        for name in names:
            namesList.append(name)

        return namesList

    def ReferencePosition(self, position=None):

        if position is None:
            return self.server.ReferencePosition
        else:
            ref = esvision.Position2D(position)
            self.server.ReferencePosition = ref
            logging.debug(f'Reference Position moved to {position}')

    def SetBiasImage(self, imageData):
        pass

    def SetDriftRate(self, driftX, driftY):
        self.server.SetDriftRate(driftX, driftY)
        logging.debug(f'Drift rate set to ({driftX}, {driftY})')

    def SetGainImage(self, imageData):
        pass

class ScanningServer(ImageServer):

    def __init__(self,app):
            self.app = app
            self.server = app.ScanningServer()

    def scanMode(self, mode=None):

        if mode is None:
            return ScanModes(self.server.ScanMode).name
        else:
            self.server.ScanMode = mode
            logging.info(f'Acquire mode is now {ScanModes(mode).name}')

    def getTotalScanRange(self):

        range = self.server.GetTotalScanRange

        return (range.StartX, range.StartY, range.EndX, range.EndY)

    def forceExternalScan(self, value=None):

        if value is None:
            return self.server.ForceExternalScan

        else:
            self.server.ForceExternalScan = value

    def frameWidth(self, value=None):

        if value is None:
            return self.server.FrameWidth
        else:
            self.server.FrameWidth = value
            logging.debug(f'Frame Width set as {value}')

    def dwellTime(self, value=None):

        if value is None:
            return self.server.DwellTime
        else:
            self.server.DwellTime = value
            logging.debug(f'DwellTime set as {value}')

    def frameHeight(self, value=None):

        if value is None:
            return self.server.FrameHeight
        else:
            self.server.FrameHeight = value
            logging.debug(f'Frame Height set as {value}')

    def scanRange(self, value=None):

        print('testing')
        if value is None:
            range = self.server.scanRange

            return (range.StartX, range.StartY, range.EndX, range.EndY)
        else:
            self.server.scanRange = self.app.Range2D(value[0], value[1], value[2],value[3])

    def scanResolution(self, value=None):

        if value is None:
            return self.server.ScanResolution

        else:
            self.server.ScanResolution = value


class ParallelImageServer(AcquisitionServer):

    def __init__(self,app):
            self.app = app
            self.server = app.CCDServer()

    def camera(self, value=None):
        '''
        :param value: camera name to set
        :return: camera name if value is none
        '''
        if value is None:
            return self.server.Camera

        else:
            self.server.Camera = value


    def cameraInserted(self, value=None):
        '''
        :param value: set insertion state of camera
        :return: camera insertion state
        '''
        if value is None:
            return self.server.CameraInserted

        else:
            self.server.CameraInserted = value

    def cameraNames(self):


        names = self.server.CameraNames()

        namesList = list()
        for name in names:
            namesList.append(name)

        return namesList

    def totalReadoutRange(self):

        range = self.server.GetTotalReadoutRange()

        return (range.StartX, range.StartY, range.EndX, range.EndY)

    def totalPixelReadoutRange(self):

        range = self.server.GetTotalPixelReadoutRange()

        return (range.StartX, range.StartY, range.EndX, range.EndY)

    def integrationTimeRange(self):

        range = self.server.GetIntegrationTimeRange()
        return (range.Start, range.End)

    def hasBiasImage(self):

        return self.server.HasBiasImage()

    def hasGainImage(self):

        return self.server.HasGainImage()

    def integrationTime(self, value=None):
        '''
        :param value: set integration time for acquistion
        :return: current integration time for acquisition
        '''
        if value is None:
            return self.server.IntegrationTime

        else:
            self.server.IntegrationTime = value

    def isCameraRetractable(self):
        return self.server.isCameraRetractable()


    def pixelReadoutRange(self, value=None):
        '''
        :param value: set pixelReadoutRange for acquistion
        :return: current pixelReadoutRange for acquisition
        '''
        if value is None:

            range =self.server.pixelReadoutRange
            return (range.StartX, range.StartY, range.EndX, range.EndY)

        else:

            newRange = self.app.Range2D(value[0],value[1],value[2],value[3])
            self.server.pixelReadoutRange = newRange


    def readoutRange(self, value=None):
        '''
        :param value: set readoutRange for acquistion
        :return: current readoutRange  for acquisition
        '''
        if value is None:
            range =self.server.readoutRange
            return (range.StartX, range.StartY, range.EndX, range.EndY)

        else:
            newRange = self.app.Range2D(value[0],value[1],value[2],value[3])
            self.server.readoutRange = newRange


class CcdServer(ParallelImageServer):

 #   def __init__(self,app):
  #      super(CcdServer, self).__init__()


    def binning(self, value=None):
        if value is None:
            return self.server.binning

        else:
            self.server.readoutRange = value

    def binningValues(self):
        binValues = self.server.binningValues()

        bins = list()
        for bin in binValues:
            bins.append(bin)

        return bins

    def readoutRate(self,value=None):
        if value is None:
            return self.server.ReadoutRate

        else:
            self.server.ReadoutRate = value

    def readoutRates(self):
        readoutRates = self.server.readoutRates()

        rates = list()
        for rate in readoutRates:
            rates.append(rate)

        return rates

    def setGainImage(self, image, binning):
        '''
        implementation needed
        :param image: data array
        :param binning: int
        :return:
        '''
        pass


class EmpadServer(ScanningServer):
    a =2
