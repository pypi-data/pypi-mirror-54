Pretix Telephone Contact Question
=================================

This is a plugin for `pretix`_. It adds a Question asking for the telephone number to the contact information form. The information can be seen under a contact information panel in the order detail view. The helptext and wether the question is required can be changed in the backend.

You can install the plugin manually or use ``pip`` to install ``pretix-telephone``.

Development setup
-----------------

1. Make sure that you have a working `pretix development setup`_.

2. Clone this repository, eg to ``local/pretix-telephone``.

3. Activate the virtual environment you use for pretix development.

4. Execute ``python setup.py develop`` within this directory to register this application with pretix's plugin registry.

5. Execute ``make`` within this directory to compile translations.

6. Restart your local pretix server. You can now use the plugin from this repository for your events by enabling it in
   the 'plugins' tab in the settings.


License
-------

Copyright 2018 Felix Rindt

Released under the terms of the Apache License 2.0


.. _pretix: https://github.com/pretix/pretix
.. _pretix development setup: https://docs.pretix.eu/en/latest/development/setup.html
