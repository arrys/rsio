Hello world
===========

**Repository:** `link <https://github.com/BertVanAcker/rpio-examples/tree/main/HelloWorld>`_

This project illustrates a distributed MAPLE-K loop for anomaly detection and compensation in a simulated TurtleBot 4 environment. The simulation demonstrates handling lidar occlusion and adjusting the robot's navigation dynamically.

Project Overview
----------------

The MAPLE-K loop is designed to detect anomalies in the lidar data and modify the robot's navigation strategy to compensate for occlusions. Rather than changing the robot's trajectory or path, the plan phase alters the robot's navigation parameters to manage the detected anomaly.

Prerequisites
-------------

Ensure the following requirements are met before running the system:

1. **Python Dependencies**: Install required Python libraries:
   .. code-block:: bash

      pip install robosapiensio

2. **MQTT Broker**: Ensure an MQTT broker (like Mosquitto) is running on your PC.

3. **Redis Database**: Start a Redis server to manage the knowledge base and data exchange among MAPE-K components.

Running the Simulation
----------------------

1. **Start the MQTT Broker and Redis Server**:
   - Make sure your MQTT broker is active.
   - Launch your Redis server.

2. **Run the Robot Simulator**:
   - Start the simulation using:

     .. code-block:: bash

        python Realization/ManagingSystem/Simulator/Turtlebotsim.py

   - This opens a dashboard to control the robot and simulate lidar occlusion.

3. **Initialize MAPLE-K Components**:
   - Launch the MAPLE-K loop by running:

     .. code-block:: bash

        python Resources/main.py

   - The `main.py` script sets up the MAPLE-K loop and manages anomaly detection.

MAPE-K Component Development
----------------------------

- **Component Structure**: The MAPE-K components are structured using an AADL-to-code generator. By modifying the AADL model, you can change message configurations or event triggers for each component.
- **Directory**: Check the `Realization/ManagingSystem/Nodes` directory for individual `.py` files of each MAPE-K component.

Simulation Example
------------------

This example demonstrates an anomaly detection simulation for a TurtleBot 4 using the MAPE-K loop. The loop consists of the following phases:

- **Monitor**: Collects lidar data and writes it to the knowledge base.
- **Analysis**: Reads the lidar data from the knowledge base to determine if an occlusion has occurred or if there's simply an obstacle.
- **Plan**: If an anomaly is detected, this component calculates changes to the robot's navigation stack, such as the angle and period of rotation, to compensate for the occlusion.
- **Legitimate**: A legitimacy check ensures the new plan is developed within time constraints.
- **Execute**: Sends the new navigation plan to the robot.

In this simulation, a TurtleBot 4 is used to illustrate lidar data, occlusion scenarios, and the corresponding changes in the robot's navigation stack.

System Behavior
---------------

Once the system is operational:
- Press the **Lidar Occlusion** button in the simulator to observe how the MAPE-K loop adjusts the robot's navigation in response to the occlusion.
- The robot will not change its path but will adjust its navigation parameters to compensate.

Notes
-----

- Ensure your MQTT broker and Redis server are properly configured and running.
- Feel free to modify the code and the AADL model to customize the MAPE-K loop for various scenarios.

Enjoy experimenting with your robot anomaly detection and compensation system!
