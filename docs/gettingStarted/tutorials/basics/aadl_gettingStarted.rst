.. _aadl_instructions_logical:
# README: Defining the Logical Architecture using AADL for the MAPLE-K Loop

========================================
Adaptive application modeling using AADL
========================================

**Goal:** This tutorial will walk you through the steps to model the self-adaptive (robotics) application using AADL.

**Tutorial level:** Intermediate

**Time:** 30 minutes

.. contents:: Contents
   :depth: 2
   :local:


Background
----------

This tutorial provides a comprehensive guide on defining the logical architecture for the MAPLE-K loop using **AADL (Architecture Analysis & Design Language)**. The following MAPLE-K components are available for configuration:

- **Monitor (M):** Data collection and preprocessing.
- **Analyze (A):** Anomaly detection and state evaluation.
- **Plan (P):** Plan (e.g. path, strategy,...) generation.
- **Legitimate (L):** Plan validation and verification.
- **Execute (E):** Plan implementation on the managed system.
- **Knowledge (K):** Knowledge gathered and used within the managing system.

Each component is modeled as an **AADL process**, with features (inputs/outputs) and threads (functions). These features require **messages** to be passed, which must be explicitly defined in a separate package (e.g., `messages.aadl`).

Prerequisites
-------------

- **AADL knowledge**: Basic knowledge on AADL can be beneficial for this tutorial (not mandatory)

Modeling approach
-----------------

Each MAPLE component, **represented as an AADL process** follows a common modeling pattern:

.. code-block::

    process ComponentName
        features
            -- Input data ports
            inputData1: in event data port messages::MessageType1;  -- Example: messages::weatherConditions
            inputData2: in event data port messages::MessageType2;

            -- Input event ports
            inputEvent: in event port;

            -- Output data ports
            outputData: out event data port messages::MessageType3;

            -- Output event ports
            outputEvent: out event port;

        properties
			rpio::formalism => Python;
			rpio::Containerized => true;

    end ComponentName;

    process implementation ComponentName.impl
        subcomponents
            NodeFunction1: thread NodeFunction1;
            NodeFunction2: thread NodeFunction2;

        connections
            I1: port inputData1 -> NodeFunction1.inputData1;
            O1: port NodeFunction1.outputData -> outputData;
    end ComponentName.impl;


**Features**:
    - **Input/Output Events**: Represent asynchronous communication.
    - **Input/Output Data**: Represent structured data exchange.

**Features**:
    - **rpio::formalism**: Indicate the desired formalism for the given software component
    - **rpio::Containerized**: Indicate whether or not the software component can be deployed and executed as containerized application.


.. note::
    Within the RoboSAPIENS Adaptive Platform, we adhere to a **Message-based communication** method. Therefore, for each feature, a message type needs to be specified.
    These message types must be explicitly defined in the `messages.aadl` package.

**Process implementation**:
    For each of the defined MAPLE components, modeled as a process, a **process implementation** needs to be specified.
    Process implementation can hold subcomponents (AADL processes, AADL threads) which enable to further outline the MAPLE component behavior.

**Threads**:
   Threads implement the node functions or algorithms for the MAPLE component.

**Subcomponents (Optional)**:
   Use subcomponents for complex internal logic.

**Connections**:
   Define data flow between process features and threads. This enables the connection of the component-level interfaces to the subcomponent-level interfaces.

To pass data between MAPLE components in AADL, you need to explicitly define the **messages** in a separate package (messages.aadl).
Each message, **represented as an AADL data** follows a common modeling pattern:

.. code-block::

    package messages
    public
        with Base_Types, Data_Model;

        -- Example: Defining an array of integers
        data ObjectArray
            properties
                Data_Model::Data_Representation => Array;
                Data_Model::Base_Type => (classifier (Base_Types::Integer));
        end ObjectArray;

        -- Example: Ship pose message
        data shipPose
            features
                SurgeSpeed: provides data access Base_Types::Float_64;
                SwaySpeed: provides data access Base_Types::Float_64;
                YawRate: provides data access Base_Types::Float_64;
                RollAngle: provides data access Base_Types::Float_64;
                RollRate: provides data access Base_Types::Float_64;
                Heading: provides data access Base_Types::Float_64;
                x: provides data access Base_Types::Float_64;
                y: provides data access Base_Types::Float_64;
        end shipPose;

    end messages;

**Data**:
    A message is modeled as **AADL data**. Each message can contain datafields, which are modeled as features.

**Features**:
    We currently only support the `provides data access` statement to define fields within the message.
    Each data field also requires an datatype. For now, we support **Base_Type** datatypes and datatypes specified in **Data_Model**.

.. note::
    The following types are part of the Base_type package:
        - Integer_32
        - Float_64
        - Boolean (Base_Types::Boolean)
        - String (Base_Types::String)
        - Enumeration
        - Integer_8
        - Integer_16
        - Integer_64
        - Unsigned_8
        - Unsigned_16
        - Unsigned_32
        - Unsigned_64
        - Natural
        - Float_32
        - Character


Each of the MAPLE-K software components needs to be deployed and executed on a compute platform, e.g. a single-board computer.
Currently, we have a simplified modeling pattern for modeling the compute units, focussing solely on the **processor** and the **networking/interfacing** method.
A compute unit is represented as an **AADL system** containing an **AADL processor** for each processor of the platform, as shown below:

.. code-block::

    system LattePanda_Delta_3
	end LattePanda_Delta_3;

	system implementation LattePanda_Delta_3.impl
		subcomponents
			-- components --
	    	cpu: processor Intel_Celeron_N5105;
	      	mem: memory LPDDR4_8GB_2933MHz;
	      	emmc: memory EMMC_64GB;
	      	gpu: device Integrated_GPU;

			-- interfaces and busses --
      		mem_bus: bus Memory_Bus;
	      	emmc_bus: bus EMMC_Bus;
	      	wlan: bus WLAN_Bus;

		properties
			mbed::IP_Address => "192.168.0.115";

	end LattePanda_Delta_3.impl;

Within this high-level compute unit model, we use the **AADL bus** (e.g. WLAN_Bus), **AADL processor** (e.g. Intel_Celeron_N5105) and **AADL memory** (e.g. LPDDR4_8GB_2933MHz).
A bus interface follows a common modeling pattern:

.. code-block::

    bus WLAN_Bus
	    properties
	    	mbed::BandWidthCapacity => 150.0 Mbps;
    end WLAN_Bus;

.. warning::
    The modeling pattern of the bus interface is currently underspecified. This will be extended in future releases.

A processor interface follows a common modeling pattern:

.. code-block::

    -- Processor (Intel Celeron N5105)
	processor Intel_Celeron_N5105
		properties
	    	mbed::Clock_Frequency => 2.0 GHz;	-- Base frequency (~2.0 GHz)
	  		mbed::Data_Width => 64 bits; -- 64-bit processor
	  		mbed::Operations_Per_Second => 4000000000; -- Approximate value
	end Intel_Celeron_N5105;

.. warning::
    The modeling pattern of the processor is currently underspecified. This will be extended in future releases.

The processor memory, represented as **AADL memory** follows a common modeling pattern:

.. code-block::

     -- Memory (8GB LPDDR4 @ 2933MHz)
	memory LPDDR4_8GB_2933MHz
		properties
	    	mbed::Data_Size => 8 GByte;
	      	mbed::Clock_Frequency => 2933.0 MHz;
	      	-- Additional memory properties as needed
	end LPDDR4_8GB_2933MHz;

.. warning::
    The modeling pattern of the processor is currently underspecified. This will be extended in future releases.

Once the hardware platform is defined, we can specify on which compute unit the software components will be deployed and executed using AADL processor bindings. Several binding mechanisms are available:

- **Actual processor binding:** the process is bound to a specific processor, indicating a fixed allocation.
- **Allowed processor binding:** The process can be bound to one or more candidate processors, but the final allocation may be determined later.

A generic processor binding pattern could be represented as follows:

.. code-block::

    Actual_Processor_Binding => (reference(compute_unit.singleCore.MainProcessor)) applies to SoftwareSystem.ComponentA;
    Actual_Processor_Binding => (reference(compute_unit.singleCore.MainProcessor)) applies to SoftwareSystem.ComponentB;

    Allowed_Processor_Binding => (reference(compute_unit.singleCore.MainProcessor)) applies to SoftwareSystem.ComponentC;
    Allowed_Processor_Binding => (reference(AnotherPlatform.ServerProcessor)) applies to SoftwareSystem.ComponentC;

In this scenario, Components A and B are statically bound to the **MainProcessor** on the single-core compute unit.
Component C is allowed to execute on either **MainProcessor** or on **ServerProcessor** of a different platform,
enabling flexibility and optimization during the system realization phase.


In order to execute the MAPLE-K loop, we need to configure and deploy the robosapiensio backend, which enables the use of the RoboSAPIENS Adaptive Platform.
This can be achieved by modeling the backend as a **AADL system** and bind it to the processor that will run the backend:

.. code-block::

    -- robosapiensio backend configuration
	system robosapiensio_backend
		properties
			rpio::Storage_type => global;
			rpio::Redis_port => 6379;
			rpio::Redis_Database => 0;
			rpio::MQTT_port => 1883;
			rpio::Quality_of_Service => AtLeastOnce;

	end robosapiensio_backend;

	system implementation robosapiensio_backend.impl

	end robosapiensio_backend.impl;

    ...

    -- robosapiens backend
    Actual_Processor_Binding => ( reference( companion.cpu) ) applies to rpio_backend;


.. warning::

    Please note that two AADL extensions are used to add RoboSAPIENS specific properties, **rpio.aadl** (:download:`download<files/rpio.aadl>`) and **mbed.aadl** (:download:`download<files/mbed.aadl>`).
    They can be downloaded here for testing purposes. They are still under construction!


Tasks
-----

1. **Specify the custom messages (by example)**

Below an example of the messages of the NTNU case:

.. code-block::

    package messages
    public
    with Base_Types, Data_Model;

    data ObjectArray
        properties
            Data_Model::Data_Representation => Array;
            Data_Model::Base_Type => (classifier (Base_Types::Integer));
    end ObjectArray;

    data FloatArray
        properties
            Data_Model::Data_Representation => Array;
            Data_Model::Base_Type => (classifier (Base_Types::Float_64));
    end FloatArray;

       data Array
            properties
                Data_Model::Data_Representation => Array;
      end Array;

    data weatherConditions
        features
            windDirection: provides data access Base_Types::Float_64;
            windSpeed: provides data access Base_Types::Float_64;
            windSpeed2: provides data access Array;
    end weatherConditions;


    data shipPose
        features
            SurgeSpeed: provides data access Base_Types::Float_64;
            SwaySpeed: provides data access Base_Types::Float_64;
            YawRate: provides data access Base_Types::Float_64;
            RollAngle: provides data access Base_Types::Float_64;
            RollRate: provides data access Base_Types::Float_64;
            Heading: provides data access Base_Types::Float_64;
            x: provides data access Base_Types::Float_64;
            y: provides data access Base_Types::Float_64;
    end shipPose;

    data shipAction
        features
            RudderAngle: provides data access Base_Types::Float_64;
            rpm: provides data access Base_Types::Float_32;
    end shipAction;

    data predictedPath
        features
            Confidence: provides data access Base_Types::Float_32;
            waypoints: provides data access Base_Types::String;	--TODO: this needs to be a list of waypoints
    end predictedPath;

    end messages;


2. **Specify the logical architecture (by example)**

Below an example of the logical architecture of the NTNU case:

.. code-block::

    package LogicalArchitecture
    public
        with messages,Base_Types,rpio;

        -- ****************************** KNOWLEDGE component ****************************** --
        process knowledge
            features
                -- input from managed system
                weatherConditions: in out event data port messages::weatherConditions;
                shipPose: in out event data port messages::shipPose;
                shipAction: in out event data port messages::shipAction;
                -- output to managed system
                pathEstimate: in out event data port messages::predictedPath;
                --internal knowledge
                pathAnomaly: in out event data port Base_Types::Boolean;
                plan: in out event data port messages::predictedPath;
                isLegit:in out event data port Base_Types::Boolean;

        end knowledge;




        -- ****************************** MONITOR component ****************************** --
        process monitor
            features
                weatherConditions: in event data port messages::weatherConditions;
                shipPose: in event data port messages::shipPose;
                shipAction: in event data port messages::shipAction;
                pathEstimate: out event data port messages::predictedPath;

            properties
                rpio::formalism => Python;
                rpio::Containerized => true;

        end monitor;

        process implementation monitor.impl
            subcomponents
                shipPoseEstimation: thread shipPoseEstimation;

            connections
                I1: port shipPose -> shipPoseEstimation.shipPose;
                I2: port weatherConditions -> shipPoseEstimation.weatherConditions;
                I3: port shipAction -> shipPoseEstimation.shipAction;
                O1: port shipPoseEstimation.pathEstimate -> pathEstimate;

        end monitor.impl;


        thread shipPoseEstimation
            features
                weatherConditions: in event data port messages::weatherConditions;
                shipPose: in event data port messages::shipPose;
                shipAction: in event data port messages::shipAction;
                pathEstimate: out event data port messages::predictedPath;


        end shipPoseEstimation;

        thread implementation shipPoseEstimation.impl

        end shipPoseEstimation.impl;

        -- ****************************** ANALYSIS component ****************************** --
        process analysis
            features
                pathEstimate: in event data port messages::predictedPath;
                pathAnomaly: out event data port Base_Types::Boolean;

            properties
                rpio::formalism => Python;
                rpio::Containerized => true;

        end analysis;

        process implementation analysis.impl
            subcomponents
                analyzePathPredictions: thread analyzePathPredictions;

            connections
                I1: port pathEstimate -> AnalyzePathPredictions.pathEstimate;
                O1: port analyzePathPredictions.pathAnomaly -> pathAnomaly;


        end analysis.impl;


        thread analyzePathPredictions
            features
                pathEstimate: in event data port messages::predictedPath;
                pathAnomaly: out event data port Base_Types::Boolean;


        end AnalyzePathPredictions;

        thread implementation AnalyzePathPredictions.impl

        end AnalyzePathPredictions.impl;


        -- ****************************** PLAN component ****************************** --
        process plan
            features
                --todo: what does the plan-phase use as input?
                plan: out event data port messages::predictedPath;

            properties
                rpio::formalism => Python;
                rpio::Containerized => true;

        end plan;

        process implementation plan.impl
            subcomponents
                planner: thread planner;

            connections
                --todo: what does the plan-phase use as input?
                O1: port planner.plan-> plan;


        end plan.impl;


        thread planner
            features
                --todo: what does the plan-phase use as input?
                plan: out event data port messages::predictedPath;

        end planner;

        thread implementation planner.impl

        end planner.impl;

        -- ****************************** LEGITIMATE component ****************************** --
        process legitimate
            features
                --todo: what does the plan-phase use as input?
                plan: in event data port messages::predictedPath;
                verifyPlan: in event port;

                planRejected: out event port;
                planAccepted: out event port;

            properties
                rpio::formalism => Python;
                rpio::Containerized => true;

        end legitimate;

        process implementation legitimate.impl
            subcomponents
                Initialise_impl: thread initialise.impl in modes(Initialise);
                WaitForSignal_impl: thread waitingForSignal.impl in modes(WaitForSignal);
                PerformVerification_impl: thread performVerification.impl in modes(PerformVerification);


            connections
                I1: port plan -> PerformVerification_impl.plan;
                I2: port plan -> WaitForSignal_impl.plan;
                O1: port PerformVerification_impl.planAccepted -> planAccepted;
                O2: port PerformVerification_impl.planRejected -> planRejected;


            modes
                Initialise :initial mode;
                WaitForSignal: mode;
                PerformVerification: mode;


                Initialise -[Initialise_impl.initialisationDone]-> WaitForSignal;
                WaitForSignal -[verifyPlan]-> PerformVerification;
                PerformVerification -[PerformVerification_impl.planAccepted]-> WaitForSignal;
                PerformVerification -[PerformVerification_impl.planRejected]-> WaitForSignal;


        end legitimate.impl;


        thread waitingForSignal
            features
                plan: in event data port messages::predictedPath;


        end waitingForSignal;

        thread implementation waitingForSignal.impl

        end waitingForSignal.impl;

        thread initialise
            features
                initialisationDone: out event port;
        end initialise;

        thread implementation initialise.impl

        end initialise.impl;

        thread performVerification
            features
                plan: in event data port messages::predictedPath;
                planRejected: out event port;
                planAccepted: out event port;

        end performVerification;

        thread implementation performVerification.impl

        end performVerification.impl;


        -- ****************************** EXECUTE component ****************************** --
        process execute
            features
                plan: in event data port messages::predictedPath;
                isLegit:in event data port Base_Types::Boolean;
                pathEstimate: out event data port messages::predictedPath;

            properties
                rpio::formalism => Python;
                rpio::Containerized => true;

        end execute;

        process implementation execute.impl
            subcomponents
                executer: thread executer;

            connections
                I1: port plan -> executer.plan;
                I2: port isLegit -> executer.isLegit;
                O1: port executer.pathEstimate-> pathEstimate;


        end execute.impl;


        thread executer
            features
                plan: in event data port messages::predictedPath;
                isLegit:in event data port Base_Types::Boolean;
                pathEstimate: out event data port messages::predictedPath;


        end executer;

        thread implementation executer.impl

        end executer.impl;


    ---------------------------------------- MANAGED SYSTEM ELEMENTS -------------------------------
    process controlSoftware
            features
                dataIn: in event data port messages::predictedPath;

            properties
                rpio::formalism => Python;
                rpio::Containerized => true;

        end controlSoftware;

        process implementation controlSoftware.impl
            subcomponents
                controller: thread controller;

            connections
                --todo: what does the plan-phase use as input?
                O1: port dataIn -> controller.dataIn;


        end controlSoftware.impl;


        thread controller
            features
                dataIn: in event data port messages::predictedPath;

        end controller;

        thread implementation controller.impl

        end controller.impl;




    end LogicalArchitecture;

3. **Specify the physical architecture (by example)**

.. code-block::

    package PhysicalArchitecture
    public
        with mbed;

        -- ******************************************* COMPONENTS *************************************************************

        -- Processor (Intel Celeron N5105)
        processor Intel_Celeron_N5105
            properties
                mbed::Clock_Frequency => 2.0 GHz;	-- Base frequency (~2.0 GHz)
                mbed::Data_Width => 64 bits; -- 64-bit processor
                mbed::Operations_Per_Second => 4000000000; -- Approximate value
        end Intel_Celeron_N5105;

        -- Processor (Intel Celeron N5105)
        processor Intel_i9
            properties
                mbed::Clock_Frequency => 3.6 GHz;	-- Base frequency (~2.0 GHz)
                mbed::Data_Width => 64 bits; -- 64-bit processor
                mbed::Operations_Per_Second => 6400000000; -- Approximate value
        end Intel_i9;

         -- Memory (8GB LPDDR4 @ 2933MHz)
        memory LPDDR4_8GB_2933MHz
            properties
                mbed::Data_Size => 8 GByte;
                mbed::Clock_Frequency => 2933.0 MHz;
                -- Additional memory properties as needed
        end LPDDR4_8GB_2933MHz;


        -- Memory (8GB LPDDR4 @ 2933MHz)
        memory LPDDR4_64GB_2666MHz
            properties
                mbed::Data_Size => 64 GByte;
                mbed::Clock_Frequency => 2666.0 MHz;
                -- Additional memory properties as needed
        end LPDDR4_64GB_2666MHz;

        -- GPU Device (Integrated Graphics)
        device Integrated_GPU
            properties
                -- Placeholder properties
                mbed::Clock_Frequency => 0.4 GHz; -- Example base frequency for iGPU
        end Integrated_GPU;

        -- eMMC (64GB)
        memory EMMC_64GB
            properties
                mbed::Data_Size => 64 GByte;
                mbed::Non_Volatile => true;
                -- You could add additional properties like:
                -- Access_Time, Write_Cycles, etc., if needed.
        end EMMC_64GB;

        -- eMMC (2TB)
        memory EMMC_2TB
            properties
                mbed::Data_Size => 2 TByte;
                mbed::Non_Volatile => true;
                -- You could add additional properties like:
                -- Access_Time, Write_Cycles, etc., if needed.
        end EMMC_2TB;

        bus Memory_Bus
        properties
          mbed::Data_Width => 64 bits;
          -- Example data rate, adjust as needed
          mbed::BandWidthCapacity => 23.46 Mbps;
        end Memory_Bus;

        bus EMMC_Bus
            properties
              -- eMMC typically uses up to HS400 mode (~400MB/s max)
              -- This is just an example property:
                mbed::BandWidthCapacity => 400.0 Mbps;
        end EMMC_Bus;

        bus WLAN_Bus
            properties
                mbed::BandWidthCapacity => 150.0 Mbps;
        end WLAN_Bus;


        -- ******************************************* LATTEPANDA DELTA 3 MODEL *************************************************************

        system LattePanda_Delta_3
        end LattePanda_Delta_3;

        system implementation LattePanda_Delta_3.impl
            subcomponents
                -- components --
                cpu: processor Intel_Celeron_N5105;
                mem: memory LPDDR4_8GB_2933MHz;
                emmc: memory EMMC_64GB;
                gpu: device Integrated_GPU;

                -- interfaces and busses --
                mem_bus: bus Memory_Bus;
                emmc_bus: bus EMMC_Bus;
                wlan: bus WLAN_Bus;

            properties
                mbed::IP_Address => "192.168.0.115";

        end LattePanda_Delta_3.impl;


        -- ******************************************* LATTEPANDA DELTA 3 MODEL *************************************************************

        system Ship_computer
        end Ship_computer;

        system implementation Ship_computer.impl
            subcomponents
                -- components --
                cpu: processor Intel_i9;
                mem: memory LPDDR4_64GB_2666MHz;
                emmc: memory EMMC_2TB;
                gpu: device Integrated_GPU;

                -- interfaces and busses --
                mem_bus: bus Memory_Bus;
                emmc_bus: bus EMMC_Bus;
                wlan: bus WLAN_Bus;

            properties
                mbed::IP_Address => "192.168.0.10";

        end Ship_computer.impl;


    end PhysicalArchitecture;

4. **Specify the deployment (by example)**

Below an example of the mapping architecture of the NTNU case:


.. code-block::

    package NTNU_CASE
    public
        with PhysicalArchitecture,LogicalArchitecture,messages,rpio;

        -- self-adaptive system model containing the managing and managed system and interconnections
        system adaptiveSystem

        end adaptiveSystem;

        system implementation adaptiveSystem.impl
            subcomponents
                -- software
                managedSystem: system managedSystem.impl;
                managingSystem: system managingSystem.impl;
                -- hardware
                companion: system PhysicalArchitecture::LattePanda_Delta_3.impl;
                shipCompute: system PhysicalArchitecture::Ship_computer.impl;
                -- robosapiens backend
                rpio_backend : system robosapiensio_backend.impl;

            connections
                c1: port managedSystem.weatherConditions -> managingSystem.weatherConditions;
                c2: port managedSystem.shipPose -> managingSystem.shipPose;
                c3: port managedSystem.shipAction -> managingSystem.shipAction;

                c4: port managingSystem.predictedPath -> managedSystem.predictedPath;

            properties
                Actual_Processor_Binding => ( reference( companion.cpu) ) applies to managingSystem.m;
                Actual_Processor_Binding => ( reference( companion.cpu) ) applies to managingSystem.a;
                Actual_Processor_Binding => ( reference( companion.cpu) ) applies to managingSystem.p;
                Actual_Processor_Binding => ( reference( companion.cpu) ) applies to managingSystem.l;
                Actual_Processor_Binding => ( reference( companion.cpu) ) applies to managingSystem.e;
                Actual_Processor_Binding => ( reference( companion.cpu) ) applies to managingSystem.k;

                Actual_Processor_Binding => ( reference( shipCompute.cpu) ) applies to managedSystem.controlSoftware;

                -- robosapiens backend
                Actual_Processor_Binding => ( reference( companion.cpu) ) applies to rpio_backend ;

        end adaptiveSystem.impl;

        -- managed system part
        system managedSystem

            features
                weatherConditions: out event data port messages::weatherConditions;
                shipPose: out event data port messages::shipPose;
                shipAction: out event data port messages::shipAction;

                predictedPath: in event data port messages::predictedPath;

        end managedSystem;

        system implementation managedSystem.impl
            subcomponents
                controlSoftware: process LogicalArchitecture::controlSoftware.impl;


        end managedSystem.impl;



        -- managing system part
        system managingSystem

            features
                weatherConditions: in event data port messages::weatherConditions
                {
                    rpio::Port_Protocol => MQTT;
                    rpio::Port_Dataformat => Message;
                    rpio::Port_MQTT_Override_Topic => true;
                    rpio::Port_MQTT_Topic => "/weather_condition";
                    rpio::Port_Dispatch_Protocol => Periodic;
                    rpio::Port_Frequency => 10.0 Hz; -- Publish every 100ms
                };
                shipPose: in event data port messages::shipPose
                {
                    rpio::Port_Protocol => MQTT;
                    rpio::Port_Dataformat => Message;
                    rpio::Port_MQTT_Override_Topic => true;
                    rpio::Port_MQTT_Topic => "/ship_status";
                    rpio::Port_Dispatch_Protocol => Periodic;
                    rpio::Port_Frequency => 10.0 Hz; -- Publish every 100ms
                };
                shipAction: in event data port messages::shipAction
                {
                    rpio::Port_Protocol => MQTT;
                    rpio::Port_Dataformat => Message;
                    rpio::Port_MQTT_Override_Topic => false;
                    rpio::Port_Dispatch_Protocol => Periodic;
                    rpio::Port_Frequency => 10.0 Hz; -- Publish every 100ms
                };

                predictedPath: out event data port messages::predictedPath
                {
                    rpio::Port_Protocol => MQTT;
                    rpio::Port_Dataformat => Message;
                    rpio::Port_MQTT_Override_Topic => true;
                    rpio::Port_MQTT_Topic => "/new_model";
                    rpio::Port_Dispatch_Protocol => Sporadic;
                };

        end managingSystem;

        system implementation managingSystem.impl
            subcomponents
                m: process LogicalArchitecture::monitor.impl;
                a: process LogicalArchitecture::analysis.impl;
                p: process LogicalArchitecture::plan.impl;
                l: process LogicalArchitecture::legitimate.impl;
                e: process LogicalArchitecture::execute.impl;
                k: process LogicalArchitecture::knowledge;

            connections
                -- managed system to knowledge
                K1: port shipPose -> k.shipPose;
                K2: port weatherConditions -> k.weatherConditions;
                K3: port shipAction -> k.shipAction;

                -- monitor links
                M1: port k.shipPose -> m.shipPose;
                M2: port k.weatherConditions -> m.weatherConditions;
                M3: port k.shipAction -> m.shipAction;
                M4: port m.pathEstimate -> k.pathEstimate;

                -- analysis links
                A1: port k.pathEstimate -> a.pathEstimate;
                A2: port a.pathAnomaly -> k.pathAnomaly;

                -- plan links
                --todo: what does the plan-phase use as input?
                P1: port p.plan -> k.plan;

                -- legitimate links
                L1: port k.plan -> l.plan;
                --L2: port l.isLegit -> k.isLegit;

                -- execute links
                E1: port k.plan -> e.plan;
                E2: port k.isLegit -> e.isLegit;
                E3: port e.pathEstimate -> k.pathEstimate;

                -- knowledge to managed system
                K4: port k.pathEstimate -> predictedPath;

        end managingSystem.impl;

        -- robosapiensio backend configuration
        system robosapiensio_backend
            properties
                rpio::Storage_type => global;
                rpio::Redis_port => 6379;
                rpio::Redis_Database => 0;
                rpio::MQTT_port => 1883;
                rpio::Quality_of_Service => AtLeastOnce;

        end robosapiensio_backend;

        system implementation robosapiensio_backend.impl

        end robosapiensio_backend.impl;


    end NTNU_CASE;



Summary
-------

This guide provides a detailed framework for modeling MAPLE components in AADL. By systematically defining processes, threads, and messages, the architecture ensures modularity, clarity, and reusability.

Below the best practices:

1. **Define Messages Separately**: Centralize all message definitions in a dedicated file (e.g., `messages.aadl`) for reusability and clarity.
2. **Modularity**: Design each MAPLE component as a self-contained process to improve maintainability.
3. **Explicit Connections**: Clearly define data flows between processes to ensure correctness.


