Flask Tagging Test
==================

Sample implementation of Select2 with tagging in Flask and WTForms.

This is a demo app, which saves tags and tag mappings to the session
data store. So, for every new browser session, the tag data starts out
empty. Obviously, in a real-life app, tags would be saved to database
models (e.g. using SQLAlchemy), or to some other persistent data store,
instead.

Here's a `demo of the app in action
<https://flasktaggingtest.herokuapp.com/>`_.


Quickstart
----------

First, set your app's secret key as an environment variable. For example, example add the following to ``.bashrc`` or ``.bash_profile``.

.. code-block:: bash

    export FLASKTAGGINGTEST_SECRET='something-really-secret'


Then run the following commands to bootstrap your environment.


::

    git clone https://github.com/Jaza/flasktaggingtest
    cd flasktaggingtest
    pip install -r requirements/dev.txt
    python manage.py server

You will see a pretty welcome screen.

Run the following to initialize your app:

::

    python manage.py server


Dynamic Secret Key
------------------

You can have a different random secret key each time the app starts,
if you want:

::

    export FLASKTAGGINGTEST_SECRET=`python -c "import os; from binascii import hexlify; print(hexlify(os.urandom(24)))"`; python manage.py server


Deployment
----------

In your production environment, make sure the ``FLASKTAGGINGTEST_ENV`` environment variable is set to ``"prod"``.


Shell
-----

To open the interactive shell, run ::

    python manage.py shell

By default, you will have access to ``app``.


Running Tests
-------------

To run all tests, run ::

    python manage.py test
