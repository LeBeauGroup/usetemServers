
from comtypes.client import CreateObject, Constants
try:
    from comtypes.gen import TEMScripting
except:
    CreateObject("TEMScripting.Instrument")
    from comtypes.gen import TEMScripting

try:
    from comtypes.gen.IOMLib import _99A162A6_3022_4B64_88C3_A62A6BE22239_0_1_0 as IOMLib
except:
    CreateObject('{99A162A6-3022-4B64-88C3-A62A6BE22239}')
    from comtypes.gen.IOMLib import _99A162A6_3022_4B64_88C3_A62A6BE22239_0_1_0 as IOMLib


from comtypes.client import GetModule

from .acquisition import Acquisition
from .autoloader import AutoLoader
from .illumination import Illumination
from .temperatureControl import TemperatureControl
from .vacuum import Vacuum
from .camera import Camera
from .projection import Projection
from .gun import Gun
from .stage import Stage
import logging


class Instrument():


    def __init__(self):

        try:
            instrument = CreateObject("TEMScripting.Instrument")
            self.instrument = instrument

        except Exception as e:
            logging.info('Could not create instrument')
            logging.info(e)

        try:
            iom2Connection = CreateObject('Fei.Tem.Instrument2Connection.1')
            iom2Connection.connect()

            self.instrument.iom2 = iom2Connection.Instrument
        except Exception as e:
            logging.info('Could not create iom2 instrument')
            logging.info(e)

        try:
            iom3Connection = CreateObject('Fei.Tem.Instrument3Connection.1')
            iom3Connection.connect()

            self.instrument.iom3:IOMLib.Instrument3 = iom3Connection.Instrument
        except Exception as e:
            logging.info('Could not create iom3 instrument')
            logging.info(e)


        self.acquisition = Acquisition(instrument)
        self.autoloader = AutoLoader(instrument)
        self.camera = Camera(instrument)
        self.gun = Gun(instrument)
        self.illumination = Illumination(instrument,parent=self)
        self.projection = Projection(instrument)
        self.stage = Stage(instrument)
        self.temperatureControl = TemperatureControl(instrument)
        self.vacuum = Vacuum(instrument)
        self.buttons = instrument.UserButtons

        buildVersion = self.configInfo('BuildVersion')

        logging.info(f'Build Version: {buildVersion}')

    def isSTEMAvailable(self):
        return self.instrument.InstrumentModeControl.StemAvailable

    def mode(self, modeValue=None):

        if modeValue is None:
            logging.info('returning instrument mode')
            return self.instrument.InstrumentModeControl.InstrumentMode

        else:
            self.instrument.InstrumentModeControl.InstrumentMode = modeValue

    def configInfo(self, infoName):


        infoRequest = f'self.instrument.iom3.Configuration.{infoName}'

        try:
            info = eval(infoRequest)
            return info

        except Exception as e:
            logging.info(f'Could not retrieve {infoName}, {e}')




