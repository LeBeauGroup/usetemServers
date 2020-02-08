# USETEMServers

USETEMServers provide xml-rpc based access to control various compontents of the electon microscope and accessories. For now, this is limited to TFS TEM scripting and TIA scripting.  Control for Velox and DM are on the way, but for now are not included.  The goal of this python package is to build a single platform that can interface with functionallity provided by a diverse set of tools.  

This server platform is agnostic to the type of interface, and therefore could be created independent of the OEMs.

[![DOI](https://zenodo.org/badge/238958312.svg)](https://zenodo.org/badge/latestdoi/238958312)




## Install

### Packages

comtypes, pyqt5, numpy, pywinauto


### Python setup

run `python setup.py install`



## To start

open an anaconda terminal and run:

	python -m usetemServers.start

Click TEM Scripting and TIA scripting (buttons should turn green)

