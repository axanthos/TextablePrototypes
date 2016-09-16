.. meta::
   :description: Orange Textable Prototypes documentation, Web Search widget
   :keywords: Orange, Textable, Prototypes, documentation, Web Search, widget,
              Twitter, Wikipedia, Bing

.. _Web Search:

Web Search
==========

.. image:: figures/icon_WebSearch_transpa_54.png 

Import Twitter, Wikipedia and Bing data.

Authors
-------

Bassim Matar, Gregory Thonney, Cyril Nghiem, Jean Galleno, Taar Rusconi

Signals
-------

Inputs : None

Outputs : ``Text data``

  Segmentation containing the result of a query on a web service

Description
-----------
The Web Search widget is designed for the Orange Canvas environment to generate textual data retrieved from Twitter, Wikipedia or Bing. 
Depending on the service, the output segmentation has the following annotations with keys :

* Twitter : date, source, search, url and author.
* Wikipedia : source and search.
* Bing : url, source, search and title.

The interface of Web Search adapts itself according to the selected service.

Interface
~~~~~~~~~

As stated before, the interface is dependent of the selected service. In case Twitter is chosen, the interface looks like this :

.. figure:: figures/WebSearch_Twitter.png
    :align: center
    
    *Figure 1 : Web Search widget with Twitter selected*

The **Service** option allows the user to select a search engine (Twitter, Wikipedia or Bing).

The **Language** option enables the user to choose the language of the retrieved data between English, French, German, Spanish, Italian and Dutch  (by default : English). 

The **Query** field contains the searched word(s). By default, the language is set to English.

Clicking on the **Send** button executes the request. The **Info** box above indicates the number of segments sent (in case any matches the request). For more informations about the **Info** box : read `Messages`_.

Depending on which search engine is selected, different options appear on the interface. These specific aspects are stated below.

Twitter
*******

The **Number of tweets** field allows users to retrieve up to 3000 tweets (though the actual number of results may be lower).  

When **Include retweets** is checked, tweets starting with 'RT' are filtered out in order to only send "original" tweets to the output.

By default, the widget uses a public Twitter license key provided by the underlying Pattern Python library. To use a private license key, tick the **Use license key** checkbox. Four keys (which can be found under "Keys and Access Tokens" in user's account) are needed. Visit `<http://apps.twitter.com>`_ to learn more. 

.. figure:: figures/WebSearch_Twitter_key.png
    :align: center
    
    *Figure 2 : Twitter options box with license key parameters*

Wikipedia
*********

.. figure:: figures/WebSearch_Wikipedia.png
    :align: center
    
    *Figure 3 : Wikipedia options box*

When **Segment into sections** is checked, Wikipedia articles are divided into sections : each segment contains a section. 

The **Output format** is either "Plain text" or "HTML".

Bing
****

.. figure:: figures/WebSearch_Bing.png
    :align: center
    
    *Figure 4 : Bing options box*

The **Number of results** field allows users to retrieve up to 1000 Bing results (though the actual number of results may be lower).

Messages
~~~~~~~~

Information
~~~~~~~~~~~

*<n> segments sent to output (<m> characters).*
    This confirms that the widget has operated properly.


Warnings
~~~~~~~~

*Settings were changed, please click 'Send' when ready.*
    Settings have changed but the **Send automatically** checkbox
    has not been selected, so the user is prompted to click the **Send**
    button (or equivalently check the box) in order for computation and data
    emission to proceed.

*Please select one or more titles.*
    The widget instance is not able to emit data to output because no theatre
    play has been selected.

*No data sent to output yet. Please try to change query and settings.*
    The query didn't retrieve any data. When confronted to this message, the 
    user should either try to change the query or modify the settings.
   
Errors
~~~~~~

*Please enter valid Twitter api keys.*
    The entered values don't match any existing key.





