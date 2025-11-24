Release Notes
=============

.. _release_notes:

**Developing and commissioning trustworthy self-adaptive systems made easy!**

robosapiensIO 1
---------------

**robosapiensIO 1.x.x - ready for experimental use by users**

1.0.0 (2024-??-??)
~~~~~~~~~~~~~~~~~~

* add main release notes

robosapiensIO Preview
---------------------

**robosapiensIO 0.x.x - active development and internal experimental use**

0.5.1 (2025-mm-dd)
~~~~~~~~~~~~~~~~~~
* Replace model2model transformations with robotransform.

0.5.0 (2025-04-21)
~~~~~~~~~~~~~~~~~~
* Replace generic exit codes.
* Fix typos.
* Update release engineering.
* Unify test cases.
* Expand test cases.
* Clean up code.
* Refactor logging.
* Convert output to proper logs.
* Rename rpio to rsio.

0.4.0 (2025-04-16)
~~~~~~~~~~~~~~~~~~
* Separate inter and intra component communication manager.
* Add time-stamp to messages in communication and knowledge manager.
* Add random unique-id in event messages.
* Support faster communication protocols_redis.
* Support faster communication protocols_rabbitMQ.
* Support faster communication protocols_UDP.
* Support faster communication protocols_TCP/IP.
* Support faster knowledge handing protocols_memcached.
* Support faster knowledge handing protocols_kafka.
* Support read/write knowledge using standard messages.
* Support faster logging protocol in logging and tracking_redis.
* Integrate first version of the trustworthiness checker (MQTT).
* Support faster communication for the trustworthiness checker (MQTT).

0.3.24 (2024-12-12)
~~~~~~~~~~~~~~~~~~~

* Updated package generation to contain ROBOCHART2AADL transformation.
* Changed rsio.exe to rsio-cli.exe (integration along with system-level pypi install).


0.3.21 (2024-12-10)
~~~~~~~~~~~~~~~~~~~

* Update the client library to read from configs.
* Write-knowledge based on messages.

0.3.20 (2024-12-05)
~~~~~~~~~~~~~~~~~~~

* Update swc2main.
* swc2code updated (user todo added).


0.3.19 (2024-12-05)
~~~~~~~~~~~~~~~~~~~

* Updated the run and transformation command (CLI).
* Added template files (TESTING).
* Updated requirements.txt for all nodes.

0.3.11 (2024-12-03)
~~~~~~~~~~~~~~~~~~~

* Added deployment strategies {native python, virtual environment python, docker containerization}.
* Updated rsio CLI ( run, platform, transformations).
* ADDED physical architecture and deployment to AADLIL.
* robosapiensIO backbone generation (containerized).

0.3.6 (2024-11-12)
~~~~~~~~~~~~~~~~~~

* AADLIL metamodel package added.

0.3.5 (2024-11-12)
~~~~~~~~~~~~~~~~~~

* Added AADL to AADLIL parser.
* Added robochart parser.

0.3.4 (2024-11-5)
~~~~~~~~~~~~~~~~~

* Workflow added to release the CLI for windows as release asset.

0.3.3 (2024-11-5)
~~~~~~~~~~~~~~~~~

* Workflow added to release the CLI for windows.

0.3.2 (2024-10-30)
~~~~~~~~~~~~~~~~~~

* Workflow added to release the CLI for windows.

0.3.1 (2024-10-30)
~~~~~~~~~~~~~~~~~~

* Added basic AADL parser.
* Added basic CLI tool.
* Added workflow to release CLI tool for easy use.

0.3.0 (2024-10-30)
~~~~~~~~~~~~~~~~~~

* First working pypi package.

0.2.0 (2024-10-30)
~~~~~~~~~~~~~~~~~~

* Updated the setup.py to include the used modules.


0.1.0 (2024-10-30)
~~~~~~~~~~~~~~~~~~

* Birth! First alpha release, published on pypi.
