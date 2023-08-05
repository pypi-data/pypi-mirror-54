

.. contents:: Table of Contents




Introduction
============


Provides a content navigation behavior, which allows you to show sub content by category.


Compatibility
-------------

Plone 4.3.x and 5.1.x support


Installation
============

- Add the package to your buildout configuration:

::

    [instance]
    eggs +=
        ...
        ftw.contentnav


- Install the generic import profile.


Usage
=====

The contentnav listing viewlet is registered for all Dexterity-Types.
It shows categorized subcontent, within the context

The ftw.contentnav categorisation behavior extends your DX content by the functionality to add categories in the edit-view

You can simply add the contentnav categorisation behavior to your content by adding the following line to FTI:

.. code-block:: xml

    <property name="behaviors">
        <element value="ftw.contentnav.behaviors.content_categories.IContentCategories" />
    </property>

Development
===========

**Python:**

1. Fork this repo
2. Clone your fork
3. Shell: ``ln -s development.cfg buidlout.cfg``
4. Shell: ``python boostrap.py``
5. Shell: ``bin/buildout``

Run ``bin/test`` to test your changes.

Or start an instance by running ``bin/instance fg``.


Links
=====

- Github: https://github.com/4teamwork/ftw.contentnav
- Issues: https://github.com/4teamwork/ftw.contentnav/issues
- Pypi: http://pypi.python.org/pypi/ftw.contentnav
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.contentnav


Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.contentnav`` is licensed under GNU General Public License, version 2.
