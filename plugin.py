# -*- coding: utf-8 -*-

import math
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from maptool import W3WMapTool
from coorddialog import W3WCoordInputDialog
from apikey import *

class W3WTools:

    def __init__(self, iface):
        self.iface = iface
        self.mapTool = None

    def initGui(self):

        mapToolIcon = QIcon(os.path.join(os.path.dirname(__file__), "w3w.svg"))
        self.toolAction = QAction(mapToolIcon, "what3words map tool",
                                     self.iface.mainWindow())
        self.toolAction.triggered.connect(self.setTool)
        self.toolAction.setCheckable(True)
        self.iface.addToolBarIcon(self.toolAction)
        self.iface.addPluginToMenu("what3words", self.toolAction)

        zoomToIcon = QIcon(':/images/themes/default/mActionZoomIn.svg')
        self.zoomToAction = QAction(zoomToIcon, "Zoom to 3 word address",
                                     self.iface.mainWindow())
        self.zoomToAction.triggered.connect(self.zoomTo)
        self.iface.addPluginToMenu("what3words", self.zoomToAction)

        self.apikeyAction = QAction("Set API key",
                                     self.iface.mainWindow())
        self.apikeyAction.triggered.connect(askForApiKey)
        self.iface.addPluginToMenu("what3words", self.apikeyAction)

        self.iface.mapCanvas().mapToolSet.connect(self.unsetTool)

        self.zoomTo = W3WCoordInputDialog(self.iface.mapCanvas(), self.iface.mainWindow())
        self.iface.addDockWidget(Qt.TopDockWidgetArea, self.zoomTo)
        self.zoomTo.hide()

    def zoomTo(self):
        if apikey() is None:
            return
        self.zoomTo.setApiKey(apikey())
        self.zoomTo.show()

    def unsetTool(self, tool):
        try:
            if not isinstance(tool, W3WMapTool):
                self.toolAction.setChecked(False)
        except:
            pass
            #ignore exceptions thrown when unloading plugin, since map tool class might not exist already

    def setTool(self):
        if apikey() is None:
            return
        if self.mapTool is None:
            self.mapTool = W3WMapTool(self.iface.mapCanvas())
        self.toolAction.setChecked(True)
        self.iface.mapCanvas().setMapTool(self.mapTool)

    def unload(self):
        self.iface.mapCanvas().unsetMapTool(self.mapTool)
        self.iface.removeToolBarIcon(self.toolAction)
        self.iface.removePluginMenu("what3words", self.toolAction)
        self.iface.removePluginMenu("what3words", self.zoomToAction)
