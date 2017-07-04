"""
mac: Applications/Orange.app/Contents/MacOS/python OWTreetagger.py
"""

"""
Class OWTreetagger
Copyright 2016 University of Lausanne
-------------------------------------------------------------------------------
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

__version__ = u'0.0.1'
__author__ = "Xavier Barros"
__maintainer__ = "Xavier Barros"
__email__ = "xavier.barros@unil.ch"

"""
<name>Treetagger</name>
<description>...</description>
<icon>icons/icon_treetagger.png</icon>
<priority>1</priority>
"""

import Orange
from OWWidget import *
import OWGUI

from LTTL.Segmentation import Segmentation
from LTTL.Input import Input
import LTTL.Segmenter as Segmenter
import LTTL.Processor as Processor

from _textable.widgets.TextableUtils import *   # Provides several utilities.

import subprocess as sp
import os
import re
import sys
import codecs
import inspect

class OWTreetagger(OWWidget):
    """Orange widget to get corpus from pattern web"""

    # Widget settings declaration...
    settingsList = [
        u'treetagger_link',
    ]

    def __init__(self, parent=None, signalManager=None):
        """Widget creator."""
        OWWidget.__init__(
            self,
            parent,
            signalManager,
            wantMainArea = 0,
            wantStateInfoWidget = 0
        )

        # DEFINE OUTPUT / INPUT
        self.inputs = [
            ('Text Input', Segmentation, self.processInputData),
            Single
        ]
        self.outputs = [('Text data', Segmentation)]

        # Settings and other attribute initializations...

        # BASIC SETTING
        self.autoSend = False
        self.createdInputs = list()
        self.inputData = None
        self.system = os.name
        self.user = os.environ.get("USER")

        # Always end Textable widget settings with the following 3 lines...
        self.uuid = None
        self.loadSettings()
        self.uuid = getWidgetUuid(self)

        # NONE BASIC SETTING
        self.langues = list()
        self.created_inputs = list()
        self.language = 0
        self.check_firt_use = False
        self.activer_xml = False
        self.unknown = False
        self.compteur = 0

        # liste des langues possible
        self.langues_possibles = {
            "French": ["french.par", "french-abbreviations"],
            "English": ["english-utf8.par", "english-abbreviations"],
            "German": ["german-utf8.par", "german-abbreviations"],
            "Italian": ["italian-utf8.par", "italian-abbreviations"],
            "Swahili": ["swahili.par", "swahili-abbreviations"],
            "Portuguese" : ["portuguese.par", "portuguese-abbreviations"],
            "Russian": ["russian.par", "russian-abbreviations"],
            "Spanish": [
                "spanish-utf8.par",
                "spanish-abbreviations",
                "spanish-mwls"
            ],
            "Slovenian": ["slovenian-utf8.par"],
            "Slovak": ["slovak2-utf8.par"],
            "Romanian": ["romanian.par"],
            "Polish": ["polish-utf8.par"],
            "Mongolian": ["mongolian.par"],
            "Latin": ["latin.par"],
            "Galician": ["galician.par"],
            "Finnish": ["finnish-utf8.par"],
            "Estonian": ["estonian.par"],
            "Bulgarian": ["bulgarian-utf8.par"],
            "Spoken French": ["spoken-french.par", "french-abbreviations"]
        }

        # Next two instructions are helpers from TextableUtils. Corresponding
        # interface elements are declared here and actually drawn below (at
        # their position in the UI)...
        self.infoBox = InfoBox(widget=self.controlArea)
        self.sendButton = SendButton(
            widget=self.controlArea,
            master=self,
            callback=self.sendData,
            infoBoxAttribute=u'infoBox',
            sendIfPreCallback=self.updateGUI
        )

        # The AdvancedSettings class, also from TextableUtils, facilitates
        # the management of basic vs. advanced interface. An object from this
        # class (here assigned to self.advancedSettings) contains two lists
        # (basicWidgets and advanceWidgets), to which the corresponding
        # widgetBoxes must be added.

        # User interface...

        # OPTION BOX
        OWGUI.separator(
            widget = self.controlArea,
            height = 5
        )

        self.infoBox1 = OWGUI.widgetBox(
            self.controlArea,
            u"Option",
            addSpace = True
        )

        # definir la langue
        self.langueBox = OWGUI.comboBox(
            widget=self.infoBox1,
            master = self,
            value = 'language',
            items = self.langues,
            orientation = u'horizontal',
            label = "Select text language :",
            callback = self.settings_changed
        )

        self.langueBox.setMaximumWidth(100)

        OWGUI.separator(
            widget = self.controlArea,
            height = 3
        )

        # Checkbox pour activer output avec code xml
        self.choix_xml = OWGUI.checkBox(
            widget = self.infoBox1,
            master = self,
            value = 'activer_xml',
            label = " Output with XML code",
            callback = self.settings_changed
        )

        # Checkbox pour afficher unknown si le mot est inconnu
        self.choix_unknown = OWGUI.checkBox(
            widget = self.infoBox1,
            master = self,
            value = 'unknown',
            label = " Output without '[unknown]'",
            callback = self.settings_changed
        )

        # The following lines:
        # Bouton pour aller cherche le lien vers treetagger...
        self.treetagger_box = OWGUI.widgetBox(
            self.controlArea,
            u"Please, enter a correct path to TreeTagger :",
            addSpace = True
        )

        OWGUI.button(
            widget = self.treetagger_box,
            master = self,
            label = 'Browse',
            callback = self.treetagger_search
        )

        OWGUI.separator(
            widget = self.treetagger_box,
            height = 3
        )

        OWGUI.rubber(self.controlArea)

        # Now Info box and Send button must be drawn...
        self.sendButton.draw()
        self.infoBox.draw()

        # Send data if autoSend.
        self.sendButton.sendIf()

        # ajuster taille widjet
        self.adjustSize()

        # verifie lien treetagger
        self.treetagger_check()


    # ALL FUNCTIONS

    def treetagger_check(self):

        # liste des element que doit contenir le dossier treetagger...
        liste = list()
        tokenize = os.path.normpath("/cmd/tokenize.pl")
        tokenize_utf8 = os.path.normpath('/cmd/utf8-tokenize.perl')
        treetagger = os.path.normpath('/bin/tree-tagger')

        # definir le ce que l'on trouve dans le chemin vers treetagger
        if self.system == "nt":
            check_list = [tokenize, tokenize_utf8, treetagger+'.exe']
        else:
            check_list = [tokenize, tokenize_utf8, treetagger]

        # definir le chemin vers treetagger automatiquement
        path = os.path.dirname(
                os.path.abspath(inspect.getfile(inspect.currentframe()))
            ) # --> temporaire

        # stoquer le lien vers treetagger (windows ou autre)...
        if self.system == "nt":
            if os.path.exists("treetagger_link.txt"):
                file = open('treetagger_link.txt', 'r')
                self.treetagger_link = file.read()
            else:
                self.treetagger_link = os.path.normpath("C:\TreeTagger")

        else:
            if os.path.exists(os.path.normpath("/Users/" + \
            self.user + "/treetagger_link.txt")):
                file = open(os.path.normpath(
                    "/Users/" + self.user + "/treetagger_link.txt"),
                    'r'
                )
                self.treetagger_link = file.read()
            else:
                self.treetagger_link = os.path.normpath(
                    "/Applications/TreeTagger"
                )

        # verifier si le chemin est correcte
        for check in check_list:
            check = os.path.exists(self.treetagger_link + check)
            liste.append(check)

        # afficher le bouton pour aller chercher le lien
        # et verouiller le reste des posibilite...
        if False in liste:
            self.NoLink = True
            # botton encore visible et les autres verouille
            self.treetagger_box.setVisible(True)
            self.infoBox1.setDisabled(True)

            # afficher les probleme s'il y en a...
            if self.check_firt_use is False:
                self.infoBox.setText(
                    u"Please click 'Browse' and select the path \
                    to TreeTagger base folder. ",
                    "warning"
                )
            else:
                self.infoBox.setText(
                    u"Sorry, TreeTagger's link isn't correct.",
                    "error"
                )

        # cacher le bouton pour aller chercher le lien
        # et deverouiller le reste des posibilite...
        else:
            if self.check_firt_use is True:
                self.infoBox.setText(
                    u"TreeTagger's link is correct !\n\n \
                    Now, Widget needs input.",
                    "warning"
                )
            else:
                self.infoBox.setText(
                    u"Widget needs input.",
                    "warning"
                )

            # affiche les langues
            self.language_possibility()
            for langue_actualise in self.langues:
                self.langueBox.addItem(langue_actualise)

            # modification affichage de l'interface
            self.NoLink = False
            self.treetagger_box.setVisible(False)
            self.infoBox1.setDisabled(False)

        self.saveSettings()

        return liste

    def treetagger_search(self):

        # rentre un lien comme lien de base marche pas
        self.treetagger_link = os.path.normpath(
            unicode(
                QFileDialog.getExistingDirectory(
                    self, u'Enter a path to Treetagger'
                )
            )
        )

        # Try to save list in this module's directory for future reference...
        if self.system == "nt":
            file = open("treetagger_link.txt", 'w')
        else:
            file = open(os.path.normpath(
                "/Users/" + self.user + "/treetagger_link.txt"),
                'w'
            )

        file.write(self.treetagger_link)
        file.close()

        self.check_firt_use = True

        # verifie si le lien marche
        self.treetagger_check()

    def language_possibility(self):

        # initilise que les langues installees dans treetagger
        # la liste dans son dossier
        langue_verification = os.listdir('.')

        langues_presentes = list()

        # On cherche quelles langue sont installees dans l'ordinateur
        for langue in self.langues_possibles.keys():
            check = True
            for file_utile in self.langues_possibles[langue]:
                check = check and os.path.isfile(
                    os.path.normpath(
                        self.treetagger_link + "/lib/" + file_utile
                    )
                )
                if not check:
                    break
            if check:
                langues_presentes.append(langue)

        self.langues = langues_presentes

        return langues_presentes

    #recoit l'input
    def processInputData(self, inputData):

        # ici on prend le input
        self.inputData = inputData

        #change l'infobox quand input change
        if self.compteur != 0:
            self.infoBox.inputChanged()

        # Send data to output.
        self.sendButton.sendIf()

    def sendData(self):
        
        # Si le lien vers treetagger n'est pas trouve
        if self.NoLink:
            self.infoBox.setText(
                u"Sorry, TreeTagger's link not found.",
                "error"
            )
            self.send('Text data', None)
        # Important: if input data is None, propagate this value to output...
        elif not self.inputData:
            self.infoBox.setText(
                u"Widget needs input",
                "warning"
            )
            self.send('Text data', None)
        # affiche que quelque chose se passe...
        else:
            self.infoBox.setText(
                u'TreeTagger is running...',
                "warning"
            )

            # Initialisation de variables
            total_tagged_text = list()
            new_segmentations = list()
            i = 0
            
            # Initialize progress bar.
            self.progressBar = OWGUI.ProgressBar(
                self,
                iterations = 5
            )
            
            # ajouter la seguementation du seguement
            for seg_idx, segment in enumerate(self.inputData):
                attr = " ".join(["%s='%s'" % \
                item for item in segment.annotations.items()])
                for itema in segment.annotations.items():
                    print itema
                print attr
                segment.annotations["tt_xb"] = attr
                self.inputData[seg_idx] = segment
                # si on re-utilise le widget il faut supprimer l'annotation tt_xb sinon bug car déjà existante
            
            # avancer la progressBar d'un cran
            self.progressBar.advance()

            concatenated_text = self.inputData.to_string(
                formatting="<xb_tt %(tt_xb)s>%(__content__)s</xb_tt>",
                display_all=True,
            )
            
            
            
            # avancer la progressBar d'un cran
            self.progressBar.advance()
            
            tagged_text = self.tag(concatenated_text)
            tagged_input = Input(tagged_text)
            tagged_segmentation = Segmenter.import_xml(tagged_input, "xb_tt")
            
            # avancer la progressBar d'un cran
            self.progressBar.advance()
            
            # Si checkBox xml active
            if self.activer_xml == True:
                xml_segmentation = Segmenter.recode(
                        tagged_segmentation,
                        substitutions = [
                            (re.compile(r"<unknown>"), '[unknown]'),
                            (re.compile(
                                r"(.+)\t(.+)\t(.+)"),
                                '<w lemma="&3" type="&2">&1</w>'
                            ),
                            (re.compile(r'"""'), '"&quot;"'),
                        ],
                    )
                final_segmentation = xml_segmentation
            # Si checkBox xml desactive
            else:
                xml_segmentation = Segmenter.recode(
                        tagged_segmentation,
                        substitutions=[
                            (re.compile(r"<unknown>"), '[unknown]'),
                            (re.compile(
                                r"(.+)\t(.+)\t(.+)"),
                                '<w lemma="&3" type="&2">&1</w>'
                            ),
                            (re.compile(r'"""'), '"&quot;"'),

                        ],
                    )
                final_segmentation = Segmenter.import_xml(
                    xml_segmentation,
                    "w"
                )

            self.infoBox.dataSent('')

            # Enregistrer le lien de treetagger...
            if self.system == "nt":
                file = open("treetagger_link.txt", 'w')
            else:
                file = open(os.path.normpath(
                    "/Users/" + self.user + "/treetagger_link.txt"),
                    'w'
                )

            file.write(self.treetagger_link)
            file.close()

            # Clear progress bar.
            self.progressBar.finish()

            # envoyer la seguementation
            self.send('Text data', final_segmentation, self)
            self.compteur += 1
            self.sendButton.resetSettingsChangedFlag()

    def tag(self, inputData):

        # fichier temporaire...
        tmp = os.path.normpath(os.path.expanduser("~/tmp_file.txt"))
        tmp2 = os.path.normpath(os.path.expanduser("~/tmp_file2.txt"))

        # ecrire dans un premier fichier le texte
        f = open(tmp, 'w')
        f.write(inputData.encode("UTF-8"))
        f.close()

        # liste de langue en option...
        option = str()
        if self.langues[self.language] == "French":
            option = "-f"
        elif self.langues[self.language] == "English":
            option = "-e"
        elif self.langues[self.language] == "Italian":
            option = "-i"

        # commande perle executee pour separer le texte en mot
        if option:
            commande1 = [
                "perl",
                os.path.normpath(
                    self.treetagger_link + "/cmd/utf8-tokenize.perl"
                ),
                option,
                "-a",
                os.path.normpath(
                    self.treetagger_link + "/lib/" + \
                    self.langues_possibles[self.langues[self.language]][1]
                ),
                tmp
            ]
        else:
            commande1 = [
                "perl",
                os.path.normpath(self.treetagger_link + "/cmd/tokenize.pl"),
                "-a",
                os.path.normpath(
                    self.treetagger_link + "/lib/" + \
                    self.langues_possibles[self.langues[self.language]][1]
                ),
                tmp
            ]

        # evoyer un ordre a la ligne de commande
        if self.system == "nt":
            outcom1 = sp.Popen(commande1, stdout=sp.PIPE, shell=True)
            out = outcom1.communicate()[0]\
                         .decode(encoding="utf-8", errors="ignore")\
                         .replace('\r', '')
        else:
            outcom1 = sp.Popen(commande1, stdout=sp.PIPE, shell=False)
            out = outcom1.communicate()[0]\
                         .decode(encoding="utf-8", errors="ignore")

        # avancer la progressBar d'un cran
        self.progressBar.advance()
            
        # ecrire dans un deuxieme fichier le texte separe en mots
        f = codecs.open(tmp2, 'w')
        f.write(out.encode("UTF-8"))
        f.close()

        if self.system ==  "nt":
            bin_treetagger = "/bin/tree-tagger.exe"
        else:
            bin_treetagger = "/bin/tree-tagger"

        # taguer le texte avec type et lemma
        if self.unknown == True:
            commande2 = [
                os.path.normpath(self.treetagger_link + bin_treetagger),
                os.path.normpath(
                    self.treetagger_link + "/lib/" + \
                    self.langues_possibles[self.langues[self.language]][0]
                ),
                "-token",
                "-lemma",
                "-sgml",
                "-no-unknown",
                '-quiet',
                tmp2
            ]

        if self.unknown == False:
            commande2 = [
                os.path.normpath(self.treetagger_link + bin_treetagger),
                os.path.normpath(
                    self.treetagger_link + "/lib/" + \
                    self.langues_possibles[self.langues[self.language]][0]
                ),
                "-token",
                "-lemma",
                "-sgml",
                '-quiet',
                tmp2
            ]

        if self.system == "nt":
            output = sp.Popen(commande2, stdout=sp.PIPE, shell=True)
            outtext = output.communicate()[0]\
                            .decode(encoding="utf-8", errors="ignore")
        else:
            output = sp.Popen(commande2, stdout=sp.PIPE, shell=False)
            outtext = output.communicate()[0]\
                            .decode(encoding="utf-8", errors="ignore")

        # supprimer ficher temporaire
        os.remove(tmp)
        os.remove(tmp2)
        
        # avancer la progressBar d'un cran
        self.progressBar.advance()
        
        return outtext

    def updateGUI(self):
        """Update GUI state"""
        pass

    def clearCreatedInputs(self):
        #Delete all Input objects that have been created.
        for i in self.createdInputs:
            Segmentation.set_data(i[0].str_index, None)
        del self.createdInputs[:]

    def settings_changed(self):
        # eviter qu'un changement arrive
        # si le widget n'a pas encore evoyer d'output...
        if self.compteur > 0:
            return self.sendButton.settingsChanged()

    def onDeleteWidget(self):
        """Free memory when widget is deleted (overriden method)"""
        self.clearCreatedInputs()

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

    def adjustSizeWithTimer(self):
        qApp.processEvents()
        QTimer.singleShot(50, self.adjustSize)

if __name__ == '__main__':
    myApplication = QApplication(sys.argv)
    myWidget = OWTreetagger()
    myWidget.show()
    myWidget.processInputData(Input('salut les amis'))
    myApplication.exec_()
