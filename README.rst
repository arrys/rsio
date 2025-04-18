`robosapiensIO <https://rpio.readthedocs.io>`_: developing trustworthy self-adaptive robotics made easy.

This repository provides a flexible software architecture framework for building self-adaptive, trustworthy robotic applications using the RoboSapiens Adaptive Platform. It includes modular building blocks for runtime adaptation, trustworthiness monitoring, and knowledge management, enabling the seamless deployment of adaptive systems in diverse environments. The platform supports both resource-constrained and high-performance computing setups, facilitating reliable, automated responses to changing operational conditions.

Requirements
============

- ``uv`` `installed <https://docs.astral.sh/uv/getting-started/installation/>`__

Usage
=====

By installing
-------------

.. code-block:: bash

   uv pip install .
   rpio

Without installing
------------------

.. code-block:: bash

   uv run python -m rpio

By building an executable
-------------------------

To manually build ``rpio.exe``, execute the following command in the terminal:

.. code-block:: bash

   uvx pyinstaller src/rpio/__main__.py --onefile -n rpio

Development
===========

You should grab all the requirements first.

.. code-block:: bash

   uv pip install -r pyproject.toml --extra dev --extra test --extra doc

Don't forget to run the tests after making changes.

.. code-block:: bash

   uv pip install -e . # Optional
   uv run pytest tests

You can also build the documentation.

.. code-block:: bash

   uv run sphinx-build -b html ./docs public
