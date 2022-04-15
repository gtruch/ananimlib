.. _install:

=========================
Installation Instructions
=========================

External Dependancies
---------------------

Cairo
^^^^^

If your Linux distribution doesn't include the `Cairo <https://www.cairographics.org>`_ binaries, PyCairo will fail to
install.  On Ubuntu, the following command should get what you need:

.. code-block::

    >sudo apt install libcairo2-dev
    

LaTex
^^^^^

Text and math animations require access to an installation of LaTex.  We have had good luck with texLive on
Linux or MikeTex on Windows.

ffmpeg
^^^^^^

Required for mp4 output.  