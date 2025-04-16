==========================================
robosapiensIO backend with Docker Tutorial
==========================================

**Goal:** This tutorial will walk you through the steps to set up the robosapiensIO backend using Docker and Docker Compose.
This can be used when manually running (e.g.using main.py) self-adaptive applications instead of the generated docker containers or for experimenting purpose.

**Tutorial level:** Beginner

**Time:** 5-10 minutes

.. contents:: Contents
   :depth: 2
   :local:


Background
----------

The robosapiensIO backend, used to develop and commission trustworthy self-adaptive systems using the RoboSAPIENS Adaptive Platform architecture, is provided as a multi-container Docker application.
It includes the following services bundled in a Docker Compose configuration:

- **EMQX Enterprise MQTT Broker**
- **Redis**

A standalone robosapiensIO backend is provided for experimenting purposes or to run the self-adaptive applications in a manual way (e.g. using main.py).

Prerequisites
-------------

- **Git**: Make sure Git is installed on your machine. You can install it from `Git's official website <https://git-scm.com/downloads>`_.
- **Docker**: Make sure Docker is installed and running on your machine. You can install it from `Docker's official website <https://docs.docker.com/get-docker/>`_.
- **Docker compose**: Make sure Docker compose is installed and running on your machine. You can install it from `Docker's official website <https://docs.docker.com/compose/install/>`_.

Tasks
-----

1. **Clone the repository**

   Open a terminal and run the following commands:

   .. code-block:: bash

       git clone https://github.com/BertVanAcker/rpio-backend-docker.git
       cd rpio-backend-docker

2. **Start the services using Docker Compose**

   After pulling the git repository, you can run the robosapiensIO backend using ``docker compose`` command:

   .. code-block:: bash

      docker compose up --detach

   Here's what each flag does:

   - ``--detach``: Runs the container in detached mode.

3. **Verify that the services are running**

   You can check that Redis Stack is running by connecting to it with the ``redis-cli``:

   .. code-block:: bash

      docker exec -it redis redis-cli

   Run a basic command to confirm connectivity, such as:

   .. code-block:: bash

      PING

   If the response is ``PONG``, Redis Stack is up and running.

    You can check that the EMQX MQTT broker is running by running the following command:

   .. code-block:: bash

      docker exec -it emqx emqx ping

   If the response is ``pong``, EMQX MQTT broker is up and running.





Summary
-------

You have successfully set up robosapiensIO on Docker and is now ready to be used.
