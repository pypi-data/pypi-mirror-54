pygtail
=======

A python "port" of `logcheck's logtail2 <http://logcheck.org>`__.

Pygtail reads log file lines that have not been read. It will even
handle log files that have been rotated.

Usage
-----

From the command line:

::

    Usage: pygtail.py [options] logfile

    Print log file lines that have not been read.

    Options:
      -h, --help            show this help message and exit
      -o OFFSET_FILE, --offset-file=OFFSET_FILE
                            File to which offset data is written (default:
                            <logfile>.offset).
      -p, --paranoid        Update the offset file every time we read a line
                            (as opposed to only when we reach the end of the
                            file).
      -n N, --every-n=N     Update the offset file every N'th time we read a
                            line (as opposed to only when we reach the end of
                            the file).
      --no-copytruncate     Don't support copytruncate-style log rotation.
                            Instead, if the log file shrinks, print a warning.
      --read-from-end       Read log file from the end if offset file is
                            missing. Useful for large files.
      --log-pattern         Custom log rotation glob pattern. Use %s to
                            represent the original filename. You may use this
                            multiple times to provide multiple patterns.
      --full_lines          Only log when line ends in a newline `\n`
                            (default: False)
      --version             Print version and exit.

In your code:

.. code:: python

    from pygtail import Pygtail

    for line in Pygtail("some.log"):
        sys.stdout.write(line)

Contributing
------------

Pull requests are very much welcome, but I will not merge your changes if you don't include a test. Run tests with `python setup.py test`.

Build status
------------

|Build Status|

.. |Build Status| image:: https://secure.travis-ci.org/bgreenlee/pygtail.png
   :target: http://travis-ci.org/bgreenlee/pygtail
