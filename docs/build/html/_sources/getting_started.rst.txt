Installation and Setup
======================

.. tip::
   Everything you need to know about the installation and project setup is explained in this video: `Project Setup Guide <https://www.youtube.com/watch?v=hypM038aNzE>`_.

   .. note::
      The video is in German; you may need to enable English subtitles.

Core Requirements
-----------------
First, you must install the specific versions of the following software to ensure compatibility:

* **FMOD Studio 2.02**: `Download <https://www.fmod.com/download#fmodstudio>`_
* **FMOD Engine 2.02**: `Download <https://www.fmod.com/download#fmodengine>`_
* **CARLA 0.9.15**: `Download <https://github.com/carla-simulator/carla/releases/tag/0.9.15/>`_
* **Python 3.8 & 3.12**: `Download <https://www.python.org/downloads/windows/>`_

After the installations are complete, clone the repository into your preferred IDE.

Virtual Environments (venvs)
----------------------------
This project requires three distinct virtual environments to handle different dependencies.

1. Carla Client Venv
~~~~~~~~~~~~~~~~~~~~
This environment is used to run the Carla simulation client. Navigate to the folder where ``Carla4UE.exe`` is located and enter the ``PythonAPI\examples`` directory:

.. code-block:: powershell

    cd C:\Users\user\yourFolderWhereCarlaIs\WindowsNoEditor\PythonAPI\examples

Create a virtual environment using **Python 3.8**:

.. code-block:: powershell

    py -3.8 -m venv .venv38

Activate the environment:

.. code-block:: powershell

    .\.venv38\Scripts\activate

Install the required packages and the Carla library:

.. code-block:: powershell

    pip install -r requirements.txt
    pip install carla

You can verify the installation with ``pip list`` and then ``deactivate`` the venv.

.. important::
   The following two virtual environments must be created within the internal code structure of the cloned project.

2. Carla Code Venv
~~~~~~~~~~~~~~~~~~
*(Details to be added here based on your project requirements)*

3. FMOD Code Venv
~~~~~~~~~~~~~~~~~
*(Details to be added here based on your project requirements)*