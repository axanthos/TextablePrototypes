"""
Class OWWebSearch
Copyright 2016 University of Lausanne
-----------------------------------------------------------------------------
This file is part of the Orange-Textable-Prototypes package v0.1.

Orange-Textable-Prototypes v0.1 is free software: you can redistribute it 
and/or modify it under the terms of the GNU General Public License as published 
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Orange-Textable-Prototypes v0.1 is distributed in the hope that it will be 
useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Orange-Textable-Prototypes v0.1. If not, see 
<http://www.gnu.org/licenses/>.
"""

__version__ = u'0.1.2'
__author__ = "Bassim Matar, Gregory Thonney, Cyril Nghiem, Jean Galleno, Taar Rusconi"
__maintainer__ = "Aris Xanthos"
__email__ = "aris.xanthos@unil.ch"

"""
<name>Web Search</name>
<description>Get corpus from Wikipedia, Twitter and Bing</description>
<icon>icons/icon_WebSearch_transpa.png</icon>
<priority>11</priority> 
"""

__version__ = '0.0.3'

import Orange
from OWWidget import *
import OWGUI
from pattern.web import (
    Twitter, 
    Wikipedia, 
    Bing, 
    SEARCH,
    HTTP401Authentication, 
    HTTP400BadRequest,
    SearchEngineLimitError
)
from LTTL.Segmentation import Segmentation
from LTTL.Input import Input
import LTTL.Segmenter as Segmenter
from _textable.widgets.TextableUtils import *

class OWWebSearch(OWWidget):
    """Orange widget to get corpus from pattern web"""
    
    # Widget settings declaration...
    settingsList = [
        'segment_label',
        'nb_tweet',
        'include_RT',
        'word_to_search',
        'autoSend',
        'operation',

        'useTwitterLicenseKey',
        'twitterLicenseKeys',
        'twitterLicenseKeysConsumerKey',
        'twitterLicenseKeysConsumerSecret',
        'twitterLicenseKeysAccessToken',
        'twitterLicenseKeysAccessTokenSecret',

        'service',
        'wiki_section',
        'wiki_type_of_text',
        'nb_bing_entry',
        'language'
    ]  
    
    def __init__(self, parent=None, signalManager=None):
        """Widget creator."""
        
        OWWidget.__init__(            
            self,
            parent,
            signalManager,
            wantMainArea=0,
            wantStateInfoWidget=0,
        )
      
        # DEFINE OUTPUT
        
        self.outputs = [('Text data', Segmentation)]

       

        # Settings and other attribute initializations...

        self.segment_label = u'search_results'
        self.nb_tweet = 50
        self.include_RT = False
        self.word_to_search = ''
        self.autoSend = False

        self.useTwitterLicenseKey = False
        self.twitterLicenseKeys = False
        self.twitterLicenseKeysConsumerKey = ''
        self.twitterLicenseKeysConsumerSecret = ''
        self.twitterLicenseKeysAccessToken = ''
        self.twitterLicenseKeysAccessTokenSecret = ''

        self.service = u'Twitter'
        self.wiki_section = False
        self.wiki_type_of_text = u'Plain text'
        self.nb_bing_entry = 50
        self.language = 'English'
        self.createdInputs = list()

        self.dico_lang = {
            'English': 'en',
            'French': 'fr',
            'German': 'de',
            'Spanish': 'es',
            'Italian': 'it',
            'Dutch': 'nl'
        }

        

        # BASIC SETTING

        self.uuid = None
        self.loadSettings()
        self.uuid = getWidgetUuid(self)
        self.inputData = None

        self.infoBox = InfoBox(widget=self.controlArea)
        self.sendButton = SendButton(
            widget=self.controlArea,
            master=self,
            callback=self.sendData,
            infoBoxAttribute='infoBox'
        )

     
        # CONFIG BOXES
 
        optionsBox = OWGUI.widgetBox(self.controlArea, 'Options')
        OWGUI.separator(widget=self.controlArea, height=3)
        self.twitterBox = OWGUI.widgetBox(self.controlArea, 'Twitter')      
        self.wikipediaBox = OWGUI.widgetBox(self.controlArea, 'Wikipedia')
        self.bingBox = OWGUI.widgetBox(self.controlArea, 'Bing')
        OWGUI.separator(widget=self.controlArea, height=3)

        self.serviceBoxes = [self.twitterBox, self.wikipediaBox, self.bingBox]



        # OPTION BOX

        OWGUI.comboBox(
            widget              = optionsBox,
            master              = self,
            value               = 'service',
            items               = [u'Twitter', u'Wikipedia', u'Bing'],
            sendSelectedValue   = True,
            orientation         = 'horizontal',
            label               = u'Service:',
            labelWidth          = 160,
            callback            = self.set_service_box_visibility,
            tooltip             = (
                    u"Select a service."
            ),
        )

        OWGUI.separator(widget=optionsBox, height=3)

        OWGUI.comboBox(
            widget              = optionsBox,
            master              = self,
            value               = 'language',
            items               = ['English', 'French', 'German', 'Spanish', 'Italian', 'Dutch'],
            sendSelectedValue   = True,
            orientation         = 'horizontal',
            label               = u'Language:',
            labelWidth          = 160,
            callback            = self.sendButton.settingsChanged,
            tooltip             = (
                    u"Select language."
            ),
        )
        
        OWGUI.separator(widget=optionsBox, height=3)
        
        OWGUI.lineEdit(
            widget              = optionsBox,
            master              = self,
            value               = 'word_to_search',
            orientation         = 'horizontal',
            label               = u'Query:',
            callback            = self.sendButton.settingsChanged,
            labelWidth          = 160,
        )

        OWGUI.separator(widget=optionsBox, height=3)



        # TWITTER BOX

        OWGUI.spin(
            widget=self.twitterBox,          
            master=self, 
            value='nb_tweet',
            label='Number of tweets:',
            labelWidth=160,
            tooltip='Select a number of tweet.',
            callback= self.sendButton.settingsChanged,
            min= 1, 
            max= 3000, 
            step=1,
        )

        OWGUI.separator(widget=self.twitterBox, height=3)

        OWGUI.checkBox(
            widget              = self.twitterBox,
            master              = self,
            value               = 'include_RT',
            label               = u'Include retweets',
            labelWidth          = 160,
            callback            = self.sendButton.settingsChanged,
            tooltip             = (
                    u"Include re-tweets or not."
            ),
        )

        OWGUI.separator(widget=self.twitterBox, height=3)

        # TWITTER LICENSE KEY BOX

        OWGUI.checkBox(
            widget              = self.twitterBox,
            master              = self,
            value               = 'useTwitterLicenseKey',
            label               = u'Use license key',
            labelWidth          = 160,
            callback            = self.changeTwitterLicenseKeyBox,
            tooltip             = (
                    u"Use private license key or not."
            ),
        )

        self.twitterLicenseBox = OWGUI.indentedBox(self.twitterBox, sep=20)

        OWGUI.separator(widget=self.twitterLicenseBox, height=3)

        OWGUI.lineEdit(
            widget=self.twitterLicenseBox,
            master=self,
            value='twitterLicenseKeysConsumerKey',
            label=u'Consumer key: ',
            orientation='horizontal',
            callback=self.sendButton.settingsChanged,
            labelWidth=140,
            tooltip=(
                    u"Your twitter Consumer key."
            ),
        )

        OWGUI.separator(widget=self.twitterLicenseBox, height=3)

        OWGUI.lineEdit(
            widget=self.twitterLicenseBox,
            master=self,
            value='twitterLicenseKeysConsumerSecret',
            label=u'Consumer secret: ',
            orientation='horizontal',
            callback=self.sendButton.settingsChanged,
            labelWidth=140,
            tooltip=(
                    u"Your private twitter license key."
            ),
        )

        OWGUI.separator(widget=self.twitterLicenseBox, height=3)

        OWGUI.lineEdit(
            widget=self.twitterLicenseBox,
            master=self,
            value='twitterLicenseKeysAccessToken',
            label=u'Access token: ',
            orientation='horizontal',
            callback=self.sendButton.settingsChanged,
            labelWidth=140,
            tooltip=(
                    u"Your private twitter Access token."
            ),
        )

        OWGUI.separator(widget=self.twitterLicenseBox, height=3)

        OWGUI.lineEdit(
            widget=self.twitterLicenseBox,
            master=self,
            value='twitterLicenseKeysAccessTokenSecret',
            label=u'Access token secret: ',
            orientation='horizontal',
            callback=self.sendButton.settingsChanged,
            labelWidth=140,
            tooltip=(
                    u"Your private twitter access token secret."
            ),
        )
        OWGUI.separator(widget=self.twitterLicenseBox, height=3)




        # WIKIPEDIA BOX

        OWGUI.checkBox(
            widget              = self.wikipediaBox,
            master              = self,
            value               = 'wiki_section',
            label               = u'Segment into sections',
            labelWidth          = 160,
            callback            = self.sendButton.settingsChanged,
            tooltip             = (
                    u"Segment into Wikipedia sections:"
            ),
        )

        OWGUI.separator(widget=self.wikipediaBox, height=3)

        OWGUI.comboBox(
            widget              = self.wikipediaBox,
            master              = self,
            value               = 'wiki_type_of_text',
            items               = [u'Plain text', u'HTML'],
            sendSelectedValue   = True,
            orientation         = 'horizontal',
            label               = u'Output format:',
            labelWidth          = 160,
            callback            = self.sendButton.settingsChanged,
            tooltip             = (
                    u"Select type of text."
            ),
        )

        OWGUI.separator(widget=self.wikipediaBox, height=3)


        # BING BOX

        OWGUI.spin(
            widget=self.bingBox,          
            master=self, 
            value='nb_bing_entry',
            label='Number of results:',
            labelWidth=160,
            tooltip='Select a number of results.',
            callback= self.sendButton.settingsChanged,
            min= 1, 
            max= 1000, 
            step=1,
        )

        OWGUI.separator(widget=self.bingBox, height=3)

        # CONFIG WIDGET
        
        OWGUI.rubber(self.controlArea)
        self.sendButton.draw()
        self.infoBox.draw()
        self.set_service_box_visibility()
        self.changeTwitterLicenseKeyBox()
        self.sendButton.sendIf()
        self.adjustSizeWithTimer()        


    # GET DATA FROM PATTERN WEB

    def get_tweets(self, search, nb, include_RT, useKey, keys):

        if not useKey:
            keys = None

        twitter = Twitter(
            language=self.dico_lang[self.language],
            license=keys
        )

        tweets = list()
        if not include_RT:
            for tweet in twitter.search(search, start=1, count=nb*3):
                if not tweet.text.startswith('RT'):
                    tweet_input = Input(tweet.text)
                    annotations = {
                        'source': 'Twitter',
                        'author': tweet.author,
                        'date': tweet.date,
                        'url': tweet.url,
                        'search': search,
                    }
                    segment = tweet_input[0]
                    segment.annotations.update(annotations)
                    tweet_input[0] = segment
                    tweets.append(tweet_input)
                if len(tweets) == nb:
                    break
        else:        
            for tweet in twitter.search(search, start=1, count=nb):
                tweet_input = Input(tweet.text)
                annotations = {
                    'source': 'Twitter',
                    'author': tweet.author,
                    'date': tweet.date,
                    'url': tweet.url,
                    'search': search,
                }
                segment = tweet_input[0]
                segment.annotations.update(annotations)
                tweet_input[0] = segment
                tweets.append(tweet_input)
        return tweets
    

    def get_wiki_article(self, search, separate_in_section=False, type_of_text=u'Plain text'):
        segments = list()
        article = Wikipedia(language=self.dico_lang[self.language]).search(search, cached=False)
        if article:
            if separate_in_section:
                for section in article.sections:
                    if type_of_text == u'Plain text':
                        wiki_article = Input(section.string)
                    else:
                        wiki_article = Input(section.html)

                    annotations = {
                        'source': 'Wikipedia',
                        'section title': section.title,
                        'section level': section.level,
                        'search': search,
                    }
                    segment = wiki_article[0]
                    segment.annotations.update(annotations)
                    wiki_article[0] = segment
                    segments.append(wiki_article)
            else:
                if type_of_text == u'Plain text':
                    wiki_article = Input(article.string)
                else:
                    wiki_article = Input(article.html)
                annotations = {
                        'source': 'Wikipedia',
                        'search': search,
                    }
                segment = wiki_article[0]
                segment.annotations.update(annotations)
                wiki_article[0] = segment
                segments.append(wiki_article)
        return segments


    def get_bing_entries(self, search, nb):
        bing = Bing(language=self.dico_lang[self.language])
        entries = list()
        for result in bing.search(search, start=1, count=nb, cached=False):
            entry_input = Input(result.text)
            annotations = {
                'source': 'Bing',
                'title': result.title,
                'url': result.url,
                'search': search,
            }
            segment = entry_input[0]
            segment.annotations.update(annotations)
            entry_input[0] = segment
            entries.append(entry_input)
        return entries




    # SEND DATA

    def sendData(self):
        """Compute result of widget processing and send to output"""

        # Clear created Inputs
        self.clearCreatedInputs()
        
        if self.service == u'Twitter':
            try:
                self.createdInputs = self.get_tweets(
                    self.word_to_search,
                    self.nb_tweet,
                    self.include_RT,
                    self.useTwitterLicenseKey,
                    (
                        self.twitterLicenseKeysConsumerKey,
                        self.twitterLicenseKeysConsumerSecret,
                        (
                            self.twitterLicenseKeysAccessToken,
                            self.twitterLicenseKeysAccessTokenSecret
                        )
                    )
                )
            except (HTTP401Authentication, HTTP400BadRequest):
                self.infoBox.setText(
                    u'Please enter valid Twitter api keys.',
                    u'error',
                )
                self.send(u'Text data', None, self)
                return False
            except SearchEngineLimitError:
                self.infoBox.setText(
                    u'Twitter search limit has been exceeded.',
                    u'error',
                )
                self.send(u'Text data', None, self)
                return False


        elif self.service == u'Wikipedia':
            self.createdInputs = self.get_wiki_article(
                self.word_to_search,
                self.wiki_section,
                self.wiki_type_of_text
            )

        elif self.service == u'Bing':
            self.createdInputs = self.get_bing_entries(
                self.word_to_search,
                self.nb_bing_entry
            )

        

        if len(self.createdInputs) == 0:
            self.infoBox.setText(
                u'Please try to change query or settings.',
                u'warning',
            )
            self.send(u'Text data', None, self)
            return False

        # Initialize progress bar
        progressBar = OWGUI.ProgressBar(
            self, 
            iterations=50
        )

        output_segmentation = Segmenter.concatenate(
            self.createdInputs, 
            self.captionTitle, 
            import_labels_as=None
        )

        message = u'%i segment@p sent to output ' % len(output_segmentation)
        message = pluralize(message, len(output_segmentation))
        numChars = 0
        for segment in output_segmentation:
            segmentLength = len(Segmentation.get_data(segment.str_index))
            numChars += segmentLength
        message += u'(%i character@p).' % numChars
        message = pluralize(message, numChars)
        self.infoBox.setText(message)

        for _ in xrange(50):
            progressBar.advance()

        # Clear progress bar.
        progressBar.finish()

        self.send('Text data', output_segmentation, self)
    
        self.sendButton.resetSettingsChangedFlag()
        



    # SET CHANGE IN WIDGET

    def set_service_box_visibility(self):
        self.sendButton.settingsChanged()
        
        for serviceBox in self.serviceBoxes:
            serviceBox.setVisible(False)

        if self.service == u'Twitter':
            self.twitterBox.setVisible(True)

        elif self.service == u'Wikipedia':
            self.wikipediaBox.setVisible(True)

        elif self.service == u'Bing':
            self.bingBox.setVisible(True)

        self.adjustSizeWithTimer()

    def changeTwitterLicenseKeyBox(self):

        self.sendButton.settingsChanged()

        if self.useTwitterLicenseKey:
            self.twitterLicenseBox.setVisible(True)
        else:
            self.twitterLicenseBox.setVisible(False)

        self.adjustSizeWithTimer()

     

    def clearCreatedInputs(self):
        """Delete all Input objects that have been created."""
        for i in self.createdInputs:
            Segmentation.set_data(i[0].str_index, None)
        del self.createdInputs[:]

    def onDeleteWidget(self):
        """Free memory when widget is deleted (overriden method)"""
        self.clearCreatedInputs()

    def adjustSizeWithTimer(self):
        qApp.processEvents()
        QTimer.singleShot(50, self.adjustSize)

    def setCaption(self, title):
        if 'captionTitle' in dir(self) and title != 'Orange Widget':
            OWWidget.setCaption(self, title)
            self.sendButton.settingsChanged()
        else:
            OWWidget.setCaption(self, title)

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


if __name__=='__main__':
    myApplication = QApplication(sys.argv)
    myWidget = OWWebSearch()
    myWidget.show()
    myApplication.exec_()
