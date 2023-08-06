Audio2book
==========

This program is for converting an audiobooks pages read into print pages
read.

Usage
-----

To use this program, you must have Python 3.6 or higher installed. You
may then install it through pip.

::

   pip install audio2book

Run the program under Python as a module. Arguments to be supplied are:

-  -c, –completed: How much of the audiobook have you completed.
-  -o, –overall: How long is the audiobook overall.
-  -p, –pages: How many pages is the print book overall.

::

   audio2book -c 0:53 -o 10:58 -p 310

You can also use the long arguments.

::

   audio2book --completed 0:53 --overall 10:58 --pages 310

And you can get help.

::

   audio2book -h

Development
-----------

A contribution guide is coming.

Running the tests
~~~~~~~~~~~~~~~~~

Pull the `source code`_.

Then make sure you have first installed the requirements:

::

   pip install -r requirements.txt

Then run the tests.

::

   ./test.sh

The tests include unit tests and mutation tests. All new functionality
must have 100% test coverage and provide any useful logging. Any
reasonable exceptions to this will be considered.

.. _source code: https://www.github.com/safuya/books
