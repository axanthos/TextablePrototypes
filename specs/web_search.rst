##################################
Spécification: Widget Textable WebSearch
##################################



1 Introduction
**************


1.1 But du projet
=================
Créer un Widget Textable qui a pour fonction de créer un corpus textuel généré à partir d'un mot clé donné par l'utilisateur depuis Twitter, Bing et Wikipédia. 
Dernière version en Python 2 disponible


1.2 Aperçu des étapes
=====================
* Première version de la spécification: 17 mars 2016
* Remise de la spécification: 24 mars 2016
* Version alpha du projet:  28 avril 2016
* Remise et présentation du projet:  26 mai 2016

1.3 Equipe et responsabilités
==============================

* Bassim Matar `bassim.matar@unil.ch`_ :

.. _bassim.matar@unil.ch: mailto:bassim.matar@unil.ch

    - Codage 
    - Test
    - Gestion de projet


* Taar Rusconi `taar.rusconi@unil.ch`_ :

.. _taar.rusconi@unil.ch: mailto: taar.rusconi@unil.ch

    - Documentation
    - Codage
    
    
* Cyril Nghiem `cyril.nghiem@unil.ch`_ :

.. _cyril.nghiem@unil.ch: mailto:cyril.nghiem@unil.ch

    - Design interface
    - Codage
    - Specification
    
* Jean Galleno `jean.galleno@unil.ch`_ :

.. _jean.galleno@unil.ch: mailto:jean.galleno@unil.ch

    - Codage
    - Gestion de projet

* Grégory Thonney `gregory.thonney.1@unil.ch`_ :

.. _gregory.thonney.1@unil.ch: mailto:gregory.thonney.1@unil.ch

    - Documentation
    - Specification
    - Codage

1.4 Ressources et documentations
==============================
* Documentation de Pattern-web: http://www.clips.ua.ac.be/pages/pattern-web
* Code source de Textable: https://bitbucket.org/langtech/orange-textable/src/ec4a228f683a2681c18104bee05e06d2e34a968d?at=master
* Tutoriel Orange Canvas: http://orange.biolab.si/getting-started/
* Orange Widgets Development: http://orange.biolab.si/docs/latest/extend-widgets/rst/
* Github theatre-classique: https://github.com/axanthos/TextablePrototypes


2. Technique
************


2.1 Mock-up de l'interface
==========================
.. image:: images/WebSearch_interface0.2.png
.. image:: images/WebSearch_interface0.2adv.png


2.2 Fonctionnalités minimales
=============================
- Utiliser un mot-clé donné par l'utilisateur pour rechercher du texte via Twitter et l'afficher. Le texte est segmenté en fonction du tweet (1 tweet = 1 segment). L'utilisateur pourra aussi définir le nombre de tweets à afficher. 

2.3 Fonctionnalités principales
===============================
- Permettre à l'utilisateur de générer un corpus de texte depuis les sections de la page Wikipédia du mot-clé utilisé. Chaque section représente un segment. 
- Avec Bing, permettre à l'utilisateur d'avoir un corpus textuel (sous forme du résumé de l'URL) généré depuis les entrées des recherches effectuées sur le moteur de recherche avec le mot-clé et segmenté selon les entrées. 
- Permettre à l'utilisateur de sélectionner plusieurs moteurs de recherche à la fois.


2.4 Fonctionnalités optionnelles
===============================
- Permettre à l'utilisateur d'entrer une clé de licence pour Bing, Twitter, etc. 
- Indiquer à l'utilisateur le nombre de requêtes restantes à effectuer par API. 
- Avec Twitter, donner à l'utilisateur la possibilité d'inclure ou non les retweets.


2.5 Tests
=========
Le widget est considéré comme fonctionnel si:
    - L'utilisateur peut entrer un mot clé dans le widget et choisir si le corpus sera généré par Twitter, Bing et/ou Wikipédia.
    - Il envoie en sortie un corpus de texte segmenté selon le moteur de recherche puis segmenté selon les tweets, sections, entrées.



3. Etapes
*********
- Se renseigner sur les fonctionnalités de pattern et des différentes API.
- Tester indépendemment chaque fonctionnalité du widget hors d'Orange Canvas.
- Implémenter les fonctionnalités dans le widget.
- Tests et corrections. 

En parallèle: 
- Interface graphique
- Etablir la documentation du widget.



3.1 Version alpha
=================
* L'interface graphique est complètement construite.
* Les fonctionnalités minimales sont prises en charge par le logiciel.



3.2 Remise et présentation
==========================
* Les fonctionnalités principales sont complètement prises en charge par le logiciel.
* La documentation du logiciel est complète.
* Le logiciel possède des routines de test de ses fonctionnalités (principales ou optionelles).


4. Infrastructure
=================
Le projet est disponible sur GitHub à l'adresse https://github.com/Bassim789/textable-pattern-web/

