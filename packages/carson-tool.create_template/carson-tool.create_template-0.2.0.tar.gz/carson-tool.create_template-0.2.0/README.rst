===================
Create Template
===================

:Source Code: https://github.com/CarsonSlovoka/carson-tool.create_template/blob/master/Carson/Tool/CreateTemplate/create_template.py
:Compatible: Python >3.6
:Platform: Windows
:License: `Apache 2.0`_
:Author Doc: https://carsonslovoka.github.io/CarsonDoc/

.. sectnum::

File templates are specifications of the default contents to be generated when creating a new file.

This Script helps you create the template file at the current work directory.

Just like PyCharm `File and code templates <https://www.jetbrains.com/help/pycharm/using-file-and-code-templates.html>`_

The only difference is that it supports you using the command line to finished.

Install
===============

* ``pip install carson-tool.create_template``

USAGE
===============

- ``create_template.bat [REFERENCE TEMPLATE] [OUTPUT FILE NAME]`` to create template, for example: ``create_template.bat PEP PEP.0484.py``
- ``create_template.bat -l *`` to get all available template
- ``create_template.bat -o open`` open template directory so that you can put your template file there.

positional arguments:
  -ref                   reference template
  -outfile               output file name

optional arguments:
  -h, --help            show this help message and exit
  --list LIST, -l LIST
    example: -l *

    description: list current available template. (accept regex)

  --option OPTION, -o OPTION
        .. csv-table:: Option
            :header: Example, Description
            :widths: 20, 60

            -o open, "open template directory so that you can put your template file there."


.. image:: https://github.com/CarsonSlovoka/carson-tool.create_template/blob/master/demo/usage.gif?raw=true
    :alt: usage.gif

.. _`Apache 2.0`: https://github.com/CarsonSlovoka/carson-tool.create_template/blob/master/LICENSE