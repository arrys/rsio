==========================================================
RoboSAPIENS Model Transformation and Code Generation Guide
==========================================================

**Goal:** This guide provides instructions to perform model-to-model and model-to-code transformations using the `rpio` CLI for the RoboSAPIENS Adaptive Platform.

**Tutorial level:** Intermediate

**Time:** 10 minutes

.. contents:: Contents
   :depth: 2
   :local:


Background
----------

The RoboSAPIENS Adaptive Platform supports a structured workflow for transforming high-level models into deployable application code. The transformations covered in this guide include:

1. **RoboChart-to-AADL**: Transforms the set of RoboChart models into a set of AADL models
2. **AADL-to-AADLIL**: Transforms the AADL models into an intermediate pythonic language, used to experiment with the necessary AADL extension points
3. **AADLIL-to-Code**: Generates code skeletons and configurations for the RoboSAPIENS Adaptive Platform software architecture, to enable proper deployment and execution of the adaptive application

Prerequisites
-------------

- **rpio CLI**: Ensure that the `rpio` command-line tool is installed and available on your system.
- **RoboChart Model**: Have your initial RoboChart models prepared in the Concept directory.


Tasks
-----

1. **RoboChart to AADL transformation**

.. note::
    Please ensure that the following roboChart models are in the Concept folder of the robosapiensIO package:
        -   **MAPLE-K.rct:** Contains the adaptive application structure
        -   **Monitor.rct:** Contains the structure of the Monitor component
        -   **Analysis.rct:** Contains the structure of the Analysis component
        -   **Plan.rct:** Contains the structure of the Plan component
        -   **Legitimate.rct:** Contains the structure of the Legitimate component
        -   **Execute.rct:** Contains the structure of the Execute component
        -   **Knowledge.rct:** Contains the structure of the Knowledge component

To transform the collection of RoboChart models into AADL format, open a terminal in the robosapiensIO package and execute:

   .. code-block:: bash

        rpio-cli transformation --roboarch2aadl --verbose

Here's what each argument in the command does:

   - ``transformation``: Specify the transformation within the robosapiensIO package.
   - ``--roboarch2aadl``: Specifies the transformation from RoboChart to AADL.
   - ``--verbose``: Enables detailed output during the transformation process.

2. **AADL to AADL Intermediate Language transformation (IL)**

.. note::
    Please ensure that the following AADL models are in the Design folder of the robosapiensIO package:
        - **messages.aadl:** Contains the allowed messages
        - **LogicalArchitecture.aadl:** Contains the logical architecture of the adaptive application
        - **PhysicalArchitecture.aadl:** Contains the physical architecture of the adaptive application


To transform the AADL models into AADL IL format, open a terminal in the robosapiensIO package and execute:

   .. code-block:: bash

        rpio-cli transformation --aadl2aadlil --verbose

Here's what each argument in the command does:

   - ``transformation``: Specify the transformation within the robosapiensIO package.
   - ``--aadl2aadlil``: Specifies the transformation from AADL to AADL Intermediate Language
   - ``--verbose``: Enables detailed output during the transformation process.

2. **AADLIL to code skeletons and RoboSAPIENS Adaptive Platform configuration**

.. note::
    Please ensure that the following AADLIL model is in the Design folder of the robosapiensIO package:
        - **system.json:** Contains the system representation of the adaptive application in json format

To transform the AADLIL model into code skeletons and configuration, open a terminal in the robosapiensIO package and execute:

   .. code-block:: bash

        rpio-cli transformation --aadlil2code --verbose

Here's what each argument in the command does:

   - ``transformation``: Specify the transformation within the robosapiensIO package.
   - ``--aadlil2code``: Specifies the transformation from AADLIL to code skeletons and RoboSAPIENS Adaptive Platform configuration
   - ``--verbose``: Enables detailed output during the transformation process.

After this transformation process, the code skeletons for the adaptive application can be found under Realization/ManagedSystem and Realization/ManagingSystem.


Summary
-------

This guide has provided the steps to perform the key transformation using the ``rpio`` command line tool:
1. Transform a RoboChart models to AADL.
2. Transform the AADL models to AADL Intermediate Language (IL).
3. Generate code skeletons from the AADLIL.

These initial code structures are ready for further development and customization as needed.