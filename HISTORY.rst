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

0.1.0 (2024-10-30)
~~~~~~~~~~~~~~~~~~

* Birth! First alpha release, published on pypi

0.2.0 (2024-10-30)
~~~~~~~~~~~~~~~~~~

* Updated the setup.py to include the used modules

0.3.0 (2024-10-30)
~~~~~~~~~~~~~~~~~~

* First working pypi package.

0.3.1 (2024-10-30)
~~~~~~~~~~~~~~~~~~

* added basic AADL parser
* added basic CLI tool
* added workflow to release CLI tool for easy use

0.3.2 (2024-10-30)
~~~~~~~~~~~~~~~~~~

* workflow added to release the CLI for windows

0.3.3 (2024-11-5)
~~~~~~~~~~~~~~~~~~

* workflow added to release the CLI for windows

0.3.4 (2024-11-5)
~~~~~~~~~~~~~~~~~~

* workflow added to release the CLI for windows as release asset

0.3.5 (2024-11-12)
~~~~~~~~~~~~~~~~~~

* added AADL to AADLIL parser
* added robochart parser

0.3.6 (2024-11-12)
~~~~~~~~~~~~~~~~~~

* AADLIL metamodel package added

0.3.11 (2024-12-03)
~~~~~~~~~~~~~~~~~~

* Added deployment strategies {native python, virtual enviornment python, docker containerization}
* Updated rpio CLI ( run, platform, transformations)
* ADDED physical architecture and deployment to AADLIL
* robosapiensIO backbone generation (containerized)

0.3.19 (2024-12-05)
~~~~~~~~~~~~~~~~~~

* Updated the run and transformation command (CLI)
* Added template files (TESTING)
* Updated requirements.txt for all nodes

0.3.20 (2024-12-05)
~~~~~~~~~~~~~~~~~~

* Update swc2main
* swc2code updated (user todo added)

0.3.21 (2024-12-10)
~~~~~~~~~~~~~~~~~~

* Update the client library to read from configs
* write-knowledge based on messages

0.3.24 (2024-12-12)
~~~~~~~~~~~~~~~~~~

* Updated package generation to contain ROBOCHART2AADL transformation
* Changed rpio.exe to rpio-cli.exe (integration along with system-level pypi install)

0.4.0 (2025-04-16)
~~~~~~~~~~~~~~~~~~
* Seprate inter and intra component communication manager
* Add time-stamp to messgaes in communication and knowledge manager
* Add random uique-id in event messages
* Support faster communication protocols_redis 
* Support faster communication protocols_rabbitMQ
* Support faster communication protocols_UDP
* Support faster communication protocols_TCP/IP
* Support faster knowledge handing protocols_memcached
* Support faster knowledge handing protocols_kafka
* Support read/write knowledge using standard messages
* Support faster logging protocol in logging and tracking_redis
* Integrate first version of the trustworthiness checker (MQTT)
* Support faster communication for the trustworthiness checker (MQTT)