======
Verdoc
======

Deploy references from source control.

Installation
============

Use `pipx <https://pipxproject.github.io/pipx/>`__ to install ``verdoc``.

.. code:: sh

    pipx install verdoc

Usage
=====

``verdoc`` currently requires the use of Git and tox.
It will check out specified references (in temporary clones) and build them by running ``tox -e verdoc -- "$dir"`` (or ``-e foo`` if ``--build-opt env=foo`` is provided) where ``$dir`` is a subdirectory of ``--dest`` named after the reference.
Additionally, ``verdoc-index "$url"`` can be used to create an ``index.html`` file that redirects to ``$url`` (which can be handy for deploying websites).

See `the documentation <https://dmtucker.github.io/verdoc/>`__ for more information.
