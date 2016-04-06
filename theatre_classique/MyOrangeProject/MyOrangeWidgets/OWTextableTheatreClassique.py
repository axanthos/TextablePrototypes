"""
<name>Theatre Classique</name>
<description>Import XML-TEI data from Theatre-classique website</description>
<icon>path_to_icon.svg</icon>
<priority>10</priority>
"""

__version__ = '0.0.0001'

import Orange
from OWWidget import *
import OWGUI

from _textable.widgets.LTTL.Segmentation import Segmentation
from _textable.widgets.LTTL.Input import Input
from _textable.widgets.LTTL.Segmenter import Segmenter

from _textable.widgets.TextableUtils import *   # Provides several utilities.

import urllib2
import re
import inspect
import os
import pickle


class OWTextableTheatreClassique(OWWidget):
    """Orange widget for importing XML-TEI data from the Theatre-classique
    website (http://www.theatre-classique.fr)
    """

    # Widget settings declaration...
    settingsList = [
        'autoSend',
        'label',
        'uuid',
        'selectedTitleLabels',
        'filterCriterion',
        'filterValue',
        'displayAdvancedSettings',
    ]

    def __init__(self, parent=None, signalManager=None):
        """Widget creator."""

        # Standard call to creator of base class (OWWidget).
        OWWidget.__init__(self, parent, signalManager, wantMainArea=0)

        # Channel definitions...
        self.inputs = []
        self.outputs = [('Text data', Segmentation)]

        # Settings initializations...
        self.autoSend = True
        self.label = u'xml_tei_data'
        self.filterCriterion = u'none'
        self.filterValue = None 
        self.titleLabels = list()
        self.selectedTitleLabels = list()
        self.displayAdvancedSettings = False

        # Always end Textable widget settings with the following 3 lines...
        self.uuid = None
        self.loadSettings()
        self.uuid = getWidgetUuid(self)

        # Other attributes...
        self.segmenter = Segmenter()
        self.segmentation = Input()
        self.titleSeg = None
        self.base_url =     \
          'http://www.theatre-classique.fr/pages/programmes/PageEdition.php'
        self.document_base_url =     \
          'http://www.theatre-classique.fr/pages/'

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

        # The AdvancedSettings class, also from TextableUtils, facilitates
        # the management of basic vs. advanced interface. An object from this 
        # class (here assigned to self.advancedSettings) contains two lists 
        # (basicWidgets and advanceWidgets), to which the corresponding
        # widgetBoxes must be added.
        self.advancedSettings = AdvancedSettings(
            widget=self.controlArea,
            master=self,
            callback=self.sendButton.settingsChanged,
        )

        # User interface...

        # Advanced settings checkbox (basic/advanced interface will appear 
        # immediately after it...
        self.advancedSettings.draw()

        # Filter box (advanced settings only)
        filterBox = OWGUI.widgetBox(
            widget=self.controlArea,
            box=u'Filter',
            orientation='vertical',
        )
        filterCriterionCombo = OWGUI.comboBox(
            widget=filterBox,
            master=self,
            value='filterCriterion',
            items=[u'author', u'year', u'genre'],
            sendSelectedValue=True,
            orientation='horizontal',
            label=u'Criterion:',
            labelWidth=180,
            callback=self.sendButton.settingsChanged,
            tooltip=(
                u"Tool\n"
                u"tips."
            ),
        )
        filterCriterionCombo.setMinimumWidth(120)
        OWGUI.separator(widget=filterBox, height=3)
        self.FilterValueCombo = OWGUI.comboBox(
            widget=filterBox,
            master=self,
            value='filterValue',
            orientation='horizontal',
            label=u'Value:',
            labelWidth=180,
            callback=self.sendButton.settingsChanged,
            tooltip=(
                u"Tool\n"
                u"tips."
            ),
        )
        OWGUI.separator(widget=filterBox, height=3)
        
        # The following lines add filterBox (and a vertical separator) to the
        # advanced interface...
        self.advancedSettings.advancedWidgets.append(filterBox)
        self.advancedSettings.advancedWidgetsAppendSeparator()

        # Title box
        titleBox = OWGUI.widgetBox(
            widget=self.controlArea,
            box=u'Titles',
            orientation='vertical',
        )
        self.titleListbox = OWGUI.listBox(
            widget=titleBox,
            master=self,
            value='selectedTitleLabels',    # setting (list)
            labels='titleLabels',           # setting (list)
            callback=self.sendButton.settingsChanged,
            tooltip=u"The list of titles whose content will be imported",
        )
        self.titleListbox.setMinimumHeight(150)
        OWGUI.separator(widget=titleBox, height=3)
        OWGUI.button(
            widget=titleBox,
            master=self,
            label=u'Refresh',
            callback=self.refreshTitleSeg,
            tooltip=u"Connect to Theatre-classique website and refresh list.",
        )
        OWGUI.separator(widget=titleBox, height=3)

        OWGUI.separator(widget=self.controlArea, height=3)

        # From TextableUtils: a minimal Options box (only segmentation label).
        basicOptionsBox = BasicOptionsBox(self.controlArea, self)
 
        OWGUI.separator(widget=self.controlArea, height=3)

        # Now Info box and Send button must be drawn...
        self.infoBox.draw()
        self.sendButton.draw()
        
        # This initialization step needs to be done after infoBox has been 
        # drawn (because getTitleSeg may need to display an error message).
        self.getTitleSeg()

        # Send data if autoSend.
        self.sendButton.sendIf()

    def sendData(self):
        """Compute result of widget processing and send to output"""

        # Skip if title list is empty:
        if self.titleLabels == list():
            return
        
        # Check that something has been selected...
        if len(self.selectedTitleLabels) == 0:
            self.infoBox.noDataSent(u': no title selected.')
            self.send('Text data', None, self)
            return

        # Check that label is not empty...
        if not self.label:
            self.infoBox.noDataSent(warning=u'No label was provided.')
            self.send('Text data', None, self)
            return

        # Attempt to connect to Theatre-classique...
        try:
            response = urllib2.urlopen(
                self.document_base_url
                + self.titleSeg[self.selectedTitleLabels[0]].annotations['url']
            )
            xml_content = unicode(response.read(), 'utf8')

        # If unable to connect (somehow)...
        except:

            # Set Info box and widget to 'error' state.
            self.infoBox.noDataSent(
                error=u"Couldn't access theatre-classique website."
            )

            # Reset output channel.
            self.send('Text data', None, self)
            return
            
        # Store downloaded XML in segmentation attribute.
        self.segmentation.update(text=xml_content, label=self.label)

        # Set status to OK...
        message = u'1 segment (%i character@p).' % len(xml_content)
        message = pluralize(message, len(xml_content))
        self.infoBox.dataSent(message)

        # Send token...
        self.send('Text data', self.segmentation, self)
        self.sendButton.resetSettingsChangedFlag()        
        
    def updateGUI(self):
        """Update GUI state"""
        if self.displayAdvancedSettings:
            self.advancedSettings.setVisible(True)
        else:
            self.advancedSettings.setVisible(False)
            
        if len(self.titleLabels) > 0:
            self.selectedTitleLabels = self.selectedTitleLabels
            
    def getTitleSeg(self):
        """Get title segmentation, either saved locally or online"""
        
        # Try to open saved file in this module's directory...
        path = os.path.dirname(
            os.path.abspath(inspect.getfile(inspect.currentframe()))
        )
        try:
            file = open(os.path.join(path, "cached_title_list"),'r')
            self.titleSeg = pickle.load(file)
            file.close()
        # Else try to load list from Theatre-classique and build new seg...
        except IOError:
            self.titleSeg = self.getTitleListFromTheatreClassique()

        # Update title list and filter comboboxes (only at init and on manual
        # refresh, therefore separate from self.updateGUI).
        self.updateLists()
                    
    def refreshTitleSeg(self):
        """Refresh title segmentation from website"""
        self.titleSeg = self.getTitleListFromTheatreClassique()
        # Update title list and filter comboboxes (only at init and on manual
        # refresh, therefore separate from self.updateGUI).
        self.updateLists()
        
    def getTitleListFromTheatreClassique(self):
        """Fetch titles from the Theatre-classique website"""

        self.infoBox.customMessage(
            u'Fetching data from Theatre-classique website, please wait'
        )
        
        # Attempt to connect to Theatre-classique...
        try:
            response = urllib2.urlopen(self.base_url)
            base_html = unicode(response.read(), 'iso-8859-1')
            self.infoBox.customMessage(
                u'Done fetching data from Theatre-classique website.'
            )

        # If unable to connect (somehow)...
        except:

            # Set Info box and widget to 'warning' state.
            self.infoBox.noDataSent(
                warning=u"Couldn't access theatre-classique website."
            )

            # Empty title list box.
            self.titleLabels = list()

            # Reset output channel.
            self.send('Text data', None, self)
            return None
            
        # Otherwise store HTML content in LTTL Input object.
        base_html_seg = Input(base_html)

        # Extract table containing titles from HTML.
        table_seg = self.segmenter.import_xml(
            segmentation=base_html_seg,
            element='table',
            conditions={'id': re.compile(r'^table_AA$')},
            remove_markup=False,
        )

        # Extract table lines.
        line_seg = self.segmenter.import_xml(
            segmentation=table_seg,
            element='tr',
            remove_markup=False,
        )

        # Compile the regex that will be used to parse each line.
        field_regex = re.compile(
            r"^\s*<td>\s*<a.+?>(.+?)</a>\s*</td>\s*"
            r"<td>(.+?)</td>\s*"
            r"<td.+?>\s*<a.+?>\s*(\d+?)\s*</a>\s*</td>\s*"
            r"<td.+?>\s*(.+?)\s*</td>\s*"
            r"<td.+?>\s*<a\s+.+?t=\.{2}/(.+?)'>\s*HTML"
        )

        # Parse each line and store the resulting segmentation in an attribute.
        titleSeg = self.segmenter.tokenize(
            segmentation=line_seg,
            regexes=[
                (field_regex, 'Tokenize', {'author': '&1'}),
                (field_regex, 'Tokenize', {'title': '&2'}),
                (field_regex, 'Tokenize', {'year': '&3'}),
                (field_regex, 'Tokenize', {'genre': '&4'}),
                (field_regex, 'Tokenize', {'url': '&5'}),
            ],
            import_annotations=False,
        )

        # Sort this segmentation alphabetically based on titles...
        titleSeg.segments.sort(key=lambda s: s.annotations['title'])
        
        # Try to save list in this module's directory for future reference...
        path = os.path.dirname(
            os.path.abspath(inspect.getfile(inspect.currentframe()))
        )
        try:
            file = open(os.path.join(path, "cached_title_list"), 'wb')
            pickle.dump(titleSeg, file) 
            file.close()         
        except IOError:
            pass

        # Remove warning (if any)...
        self.error(0)
        self.warning(0)
        
        return titleSeg

    def updateLists(self):
        """Update lists in the interface"""
        
        # If titleSeg has not been loaded for some reason, skip.
        if self.titleSeg is None:
            return
            
        # Populate titleLabels list with the titles...
        self.titleLabels = sorted(
            [s.annotations['title'] for s in self.titleSeg]
        )
        
        # Add author when title is duplicated...
        titleLabels = self.titleLabels[:]
        for idx in xrange(len(titleLabels)):
            titleLabel = titleLabels[idx]
            if self.titleLabels.count(titleLabel) > 1:
                author = self.titleSeg[idx].annotations['author']
                titleLabels[idx] = titleLabel + " (%s)" % author
        self.titleLabels = titleLabels
        
        self.updateGUI()

    def onDeleteWidget(self):
        """Make sure to delete the stored segmentation data when the widget
        is deleted (overriden method)
        """
        self.segmentation.clear()

    # The following two methods need to be copied (without any change) in
    # every Textable widget...

    def getSettings(self, *args, **kwargs):
        """Read settings, taking into account version number (overriden)"""
        settings = OWWidget.getSettings(self, *args, **kwargs)
        settings["settingsDataVersion"] = __version__.split('.')[:2]
        return settings

    def setSettings(self, settings):
        """Write settings, taking into account version number (overriden)"""
        if settings.get("settingsDataVersion", None) \
                == __version__.split('.')[:2]:
            settings = settings.copy()
            del settings["settingsDataVersion"]
            OWWidget.setSettings(self, settings)


if __name__ == '__main__':
    myApplication = QApplication(sys.argv)
    myWidget = OWTextableTheatreClassique()
    myWidget.show()
    myApplication.exec_()
