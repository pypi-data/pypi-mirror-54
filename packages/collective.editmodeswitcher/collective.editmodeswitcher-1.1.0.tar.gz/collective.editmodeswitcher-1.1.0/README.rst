collective.editmodeswitcher
===========================

collective.editmodeswitcher allows to toggle between edit and view only mode.
This enables users with modify permissions to view a page without editable
borders.
The current setting is stored in a cookie and thus effective for multiple
page views.
This is especially useful in single sign on environments.


Install
-------

Add ``collective.editmodeswitcher`` to your buildout configuration:

.. code:: ini

    [instance]
    eggs +=
        collective.editmodeswitcher

or add it as a dependency to one of your packages.


Compatibility
-------------

Runs with `Plone <http://www.plone.org/>`_ `4.2`, `4.3` and `5.1`.


Usage
-----

For toggling the edit-mode call the view ``@@switch-editmode``.
This will toggle the edit mode and store the current edit mode status
in a cookie for further requests. You can get the current state by calling
``@@switch-editmode/get_state``, this will return `enabled`, or 'disabled'.

You may want to place an action somewhere for toggling the edit mode - this
integration is not done by ``collective.editmodeswitcher``.


Caching
-------

``collective.editmodeswitcher`` provides a ``plone.app.caching`` etag adapter
named ``editmode``.
This etag can be used in the caching configuration in order to make the cache
flush when switching the edit mode.



Links
-----

- Github: https://github.com/4teamwork/collective.editmodeswitcher
- Issues: https://github.com/4teamwork/collective.editmodeswitcher/issues
- Pypi: http://pypi.python.org/pypi/collective.editmodeswitcher
- Continuous integration: https://jenkins.4teamwork.ch/search?q=collective.editmodeswitcher


Copyright
---------

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``collective.editmodeswitcher`` is licensed under GNU General Public License, version 2.
