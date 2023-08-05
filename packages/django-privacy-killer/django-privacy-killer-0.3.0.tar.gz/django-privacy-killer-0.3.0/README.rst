=================================================================
django-privacy-killer - Template tags for including tracker codes
=================================================================

.. image:: https://travis-ci.org/matthiask/django-privacy-killer.png?branch=master
   :target: https://travis-ci.org/matthiask/django-privacy-killer

.. image:: https://readthedocs.org/projects/django-privacy-killer/badge/?version=latest
    :target: https://django-privacy-killer.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

This module allows specifying tracking codes through settings (and therefore
through the environment). It currently supports Google Tag Manager and
Google Analytics tracking codes, but pull requests for adding support for
additional trackers is very welcome!


Usage variant 1
===============

- Install the module using ``pip install django-privacy-killer``
- Add ``privacy_killer`` to ``INSTALLED_APPS`` and add the list of tracking
  IDS to your settings as ``PRIVACY_KILLER_IDS = ['GTM-****', 'UA-****', ...]``
  (Note! This is a stupid example -- specifying both GTM and UA codes is
  probably not what you want
- Load the template tag library (``{% load privacy_killer %}``) and add the
  two tags, ``{% privacy_killer_head %}`` near the ``<head>`` of your site,
  and ``{% privacy_killer_body %}`` near the ``<body>`` element.


Usage variant 2
===============

Do not use this module, and also do not use any trackers at all.


Supported trackers
==================

- Google Tag Manager (``GTM-****``)
- Google Universal Analytics (``UA-****``)
- Facebook Pixel (Prefix the ``****`` code with ``FBQ-`` when specifying
  ``PRIVACY_KILLER_IDS``)


- `Documentation <https://django-privacy-killer.readthedocs.io>`_
- `Github <https://github.com/matthiask/django-privacy-killer/>`_
