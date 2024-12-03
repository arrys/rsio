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


.. warning::
    In order to automate the deployment, the physical architecture needs to be modeled and the mapping needs to be specified.
    This will be added in this tutorial in later stages.

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
	with messages,Base_Types,MBED;

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

.. warning::
    This part is under construction

4. **Specify the deployment (by example)**

.. warning::
    This part is under construction

Summary
-------

This guide provides a detailed framework for modeling MAPLE components in AADL. By systematically defining processes, threads, and messages, the architecture ensures modularity, clarity, and reusability.

Below the best practices:

1. **Define Messages Separately**: Centralize all message definitions in a dedicated file (e.g., `messages.aadl`) for reusability and clarity.
2. **Modularity**: Design each MAPLE component as a self-contained process to improve maintainability.
3. **Explicit Connections**: Clearly define data flows between processes to ensure correctness.


