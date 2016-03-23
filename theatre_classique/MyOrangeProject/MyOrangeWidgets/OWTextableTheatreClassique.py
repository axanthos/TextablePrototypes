"""
<name>Theatre Classique</name>
<description>Import XML-TEI data from Theatre-classique website</description>
<icon>path_to_icon.svg</icon>
<priority>10</priority> 
"""

__version__ = '0.0.1'

import Orange
from OWWidget import *
import OWGUI

from _textable.widgets.LTTL.Segmentation import Segmentation
from _textable.widgets.LTTL.Input import Input
from _textable.widgets.LTTL.Segmenter import Segmenter

from _textable.widgets.TextableUtils import *   # Provides several utilities.


class OWTextableTheatreClassique(OWWidget):
    """Orange widget for importing XML-TEI data from the Theatre-classique 
    website (http://www.theatre-classique.fr)
    """
    
    # Widget settings declaration...
    settingsList = [
        'selectedTitleLabels',
        'titleLabels'
        'autoSend',
        'label',
        'uuid',
    ]   
    
    def __init__(self, parent=None, signalManager=None):
        """Widget creator."""
        
        # Standard call to creator of base class (OWWidget).
        OWWidget.__init__(self, parent, signalManager, wantMainArea=0)

        # Channel definitions...
        self.inputs = []     
        self.outputs = [('Segmentation', Segmentation)]

        # Settings initializations...
        self.titleLabels = list()  
        self.selectedTitleLabels = list()  
        self.autoSend = True  
        self.label = u'xml_tei_data'
        
        # Always end Textable widget settings with the following 3 lines...
        self.uuid = None
        self.loadSettings()
        self.uuid = getWidgetUuid(self)
        
        # Other attributes...
        self.segmenter = Segmenter()
        self.segmentation = None
        
        # Next two instructions are helpers from TextableUtils. Corresponding
        # interface elements are declared here and actually drawn below (at
        # their position in the UI)...
        self.infoBox = InfoBox(widget=self.controlArea)  
        self.sendButton = SendButton(
            widget=self.controlArea,
            master=self,
            callback=self.sendData,
            infoBoxAttribute='infoBox',
            sendIfPreCallback=self.updateGUI,
        )
        
        # User interface...
        
        # Title box
        titleBox = OWGUI.widgetBox(
            widget=self.controlArea,
            box=u'Titles',
            orientation='vertical',
        )
        self.TitleListbox = OWGUI.listBox(
            widget=titleBox,
            master=self,
            value='selectedTitleLabels',    # setting (list)
            labels='titleLabels',           # setting (list)
            callback=self.updateGUI,
            tooltip=u"The list of titles whose content will be imported.\n",
        )       
        OWGUI.separator(widget=titleBox, height=3)
        
        # From TextableUtils: a minimal Options box (only segmentation label).
        basicOptionsBox = BasicOptionsBox(self.controlArea, self)

        # Now Info box and Send button must be drawn...
        self.infoBox.draw()
        self.sendButton.draw()

        # Send data if autoSend.
        self.sendButton.sendIf()

    def sendData(self):
        """Compute result of widget processing and send to output"""
        pass

    def updateGUI(self):
        """Update GUI state"""
        pass
        
    
    # The following two methods need to be copied (without any change) in 
    # every Textable widget...
    
    def getSettings(self, *args, **kwargs):
        settings = OWWidget.getSettings(self, *args, **kwargs)
        settings["settingsDataVersion"] = __version__.split('.')[:2]
        return settings

    def setSettings(self, settings):
        if settings.get("settingsDataVersion", None) \
                == __version__.split('.')[:2]:
            settings = settings.copy()
            del settings["settingsDataVersion"]
            OWWidget.setSettings(self, settings)

        
if __name__=='__main__':
    myApplication = QApplication(sys.argv)
    myWidget = OWTextableTheatreClassique()
    myWidget.show()
    #myWidget.processInputData(1)
    myApplication.exec_()
    