Welcome to Spoken Numbers!
==========================

Generate spoken numbers mp3 files used for Memory Competitions and training.


Usage and command line options
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block::

    usage: spokennumbers [-h] [-n NUMBERS] [-p INIT_SILENCE] [-c] [-s SPEED]
                        [-d SOURCE] [-e EXCLUDE] [-o OUTPUT_FILE] [-i]

    Generate spoken numbers audio files.

    If no options are provided, a random 100-digit mp3 file will be created.
    A text file will also be created next to the mp3 file contaning the raw
    numbers (used for recall).

    optional arguments:
    -h, --help            show this help message and exit
    -n NUMBERS, --numbers NUMBERS
                            The number of random digits to generate. Defaults to
                            100. If a text file is specified, all digits it
                            contains will be used instead (parsed by regexp).
    -p INIT_SILENCE, --init-silence INIT_SILENCE
                            Add some seconds of silence in the beginning of the
                            audio file. Defaults to 3 seconds.
    -c, --skip-countdown  By default, a countdown sequence will be spoken at
                            start: "3 ... 2 ... 1 ... a ... b ... c ... ...". This
                            option skips the countdown.
    -s SPEED, --speed SPEED
                            The pace at which numbers will be spoken in seconds.
                            Defaults to one digit per second.
    -d SOURCE, --source SOURCE
                            Audio files source. The string "default" will use the
                            default audio files included in the Python package.
                            For custom audio files, you can specify the path to a
                            directory as source. The directory must contain the
                            required audio wav files: 0.wav ... 9.wav and a.wav,
                            b.wav and c.wav.
    -e EXCLUDE, --exclude EXCLUDE
                            This option is used to exclude specified digits from
                            the output. For example, if `--exclude 789` is used,
                            the digits 7, 8 and 9 will not be present in the
                            output file.
    -o OUTPUT_FILE, --output-file OUTPUT_FILE
                            Name of output file. Defaults to `spoken.mp3`.
    -i, --skip-txt-file   Do not create the txt file containing the spoken
                            numbers next to the audio file. The txt file is used
                            for recall.

    Example:
        $ spokennumbers -n 150 --speed 1.2 -o monday_training.mp3

Installation
^^^^^^^^^^^^
From PyPI:

.. code-block:: bash

    $ python3 -m pip install spokennumbers

or from source (make sure you have ``python3 -m pip install wheel setuptools`` first):

.. code-block:: bash

    $ git clone https://github.com/Penlect/spokennumbers.git
    $ cd spokennumbers
    $ python3 setup.py bdist_wheel
    $ python3 -m pip install ./dist/spokennumbers-*.whl

or from generated Debian package:

.. code-block:: bash

    # Install build dependencies
    $ sudo apt install python3-all python3-setuptools dh-python
    $ git clone https://github.com/Penlect/spokennumbers.git
    $ cd spokennumbers
    $ make deb
    $ sudo apt install ./python3-spokennumbers_*.deb

**NOTE:** This project has a dependency to pydub which requires **ffmpeg** to be installed.
Install `ffmpeg <https://www.ffmpeg.org/>`_ and make sure it is available in PATH.


Changelog
^^^^^^^^^
The changelog is maintained in the debian directory, please check there: `changelog <debian/changelog>`_.
