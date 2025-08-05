================================
Redis Stack with Docker Tutorial
================================

**Goal:** This tutorial will walk you through the steps to set up Redis Stack in a Docker container.

**Tutorial level:** Beginner

**Time:** 5-10 minutes

.. contents:: Contents
   :depth: 2
   :local:


Background
----------

Redis is used as backbone of the distributed RoboSAPIENS Adaptive Platform architecture. Redis Stack extends Redis's capabilities, including modules that enable JSON document support, secondary indexing, full-text search, graph data storage, and time-series data storage. This tutorial assumes basic familiarity with Docker and command-line interfaces.

Prerequisites
-------------

- **Docker**: Make sure Docker is installed and running on your machine. You can install it from `Docker's official website <https://www.docker.com/>`_.
- **Docker Hub Account** (optional): If you want to pull the image directly, an account may be needed.

Tasks
-----

1. **Pull the Redis Stack Docker Image**

   Open a terminal and pull the latest Redis Stack image from Docker Hub:

   .. code-block:: bash

      docker pull redis/redis-stack:latest

2. **Run Redis Stack in a Docker Container**

   After pulling the image, you can run Redis Stack with a simple ``docker run`` command:

   .. code-block:: bash

      docker run -d --name redis-stack -p 6379:6379 redis/redis-stack:latest

   Here's what each flag does:

   - ``-d``: Runs the container in detached mode.
   - ``--name redis-stack``: Names the container ``redis-stack``.
   - ``-p 6379:6379``: Maps port 6379 on your machine to the Redis port in the container.

3. **Verify Redis Stack is Running**

   You can check that Redis Stack is running by connecting to it with the ``redis-cli``:

   .. code-block:: bash

      docker exec -it redis-stack redis-cli

   Run a basic command to confirm connectivity, such as:

   .. code-block:: bash

      PING

   If the response is ``PONG``, Redis Stack is up and running.

4. **(Optional) Access Redis Stack GUI**

   Redis Stack includes a web-based GUI. To access it, open your browser and go to ``http://localhost:8001``.

   **Note**: If you want to use the GUI, expose port 8001 in your ``docker run`` command:

   .. code-block:: bash

      docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest

Summary
-------

You have successfully set up Redis Stack on Docker and connected to it with the CLI. The RoboSAPIENS Adaptive Platform backbone is now ready to be used.
