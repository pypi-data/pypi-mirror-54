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

1. put your template at the ``template directory``, and that name just like ``{template_name}.template`` (i.e. the suffix is equal **template**)

    .. note:: The path of template directory, which located at ``Python\Lib\site-packages\Carson\Tool\CreateTemplate\template``

#. create_template.bat {template_name} {output file name}
    - first argument means: ref : template_name
    - second argument means: new_file_name: output file name

    example: ``create_template.bat PEP PEP.0484.py``


.. _`Apache 2.0`: https://github.com/CarsonSlovoka/carson-tool.create_template/blob/master/LICENSE