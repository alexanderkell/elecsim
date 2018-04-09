ElecSim: Agent-based modelling for the electricity sector
=========================================

`ElecSim`_ is an MIT licensed agent-based modelling toolkit for assessing the impacts of policy and technology advancements in the electricity sector.

It allows users to quickly create an electricity infrastructure with electricity generators, generating companies, electricity markets and demand. 



.. image:: https://cloud.githubusercontent.com/assets/166734/8611697/ce61ad08-268a-11e5-880b-4776dd738e0e.png
   :width: 100%
   :scale: 100%
   :alt: A screenshot of the Schelling Model in Mesa

*Above: A Mesa implementation of the Schelling segregation model,
being visualized in a browser window and analyzed in an IPython
notebook.*

.. _`Mesa` : https://github.com/projectmesa/mesa/


Features
--------

* Modular components
* Browser-based visualization
* Built-in tools for analysis

Using Mesa
----------

Getting started quickly:

.. code-block:: bash

    $ pip install mesa

To launch an example model, open any of the directories in the `examples <https://github.com/projectmesa/mesa/tree/master/examples>`_ folder and launch the ``run.py`` file there, e.g.:

.. code-block:: bash

    schelling $ python run.py

For more help on using Mesa, check out the following resources:

* `Mesa Introductory Tutorial`_
* `Mesa Advanced Tutorial`_
* `GitHub Issue Tracker`_
* `Email list`_
* `PyPI`_

.. _`Mesa Introductory Tutorial` : tutorials/intro_tutorial.html
.. _`Mesa Advanced Tutorial` : tutorials/adv_tutorial.html
.. _`GitHub Issue Tracker` : https://github.com/projectmesa/mesa/issues
.. _`Email list` : https://groups.google.com/d/forum/projectmesa
.. _`PyPI` : https://pypi.python.org/pypi/Mesa/

Contributing back to Mesa
-------------------------

If you run into an issue, please file a `ticket`_ for us to discuss. If possible, follow up with a pull request.

If you would like to add a feature, please reach out via `ticket`_ or the `email list`_ for discussion. A feature is most likely to be added if you build it!

* `Contributors guide`_
* `Github`_

.. _`ticket` : https://github.com/projectmesa/mesa/issues
.. _`email list` : https://groups.google.com/d/forum/projectmesa
.. _`Contributors guide` : https://github.com/projectmesa/mesa/blob/master/CONTRIBUTING.rst
.. _`Github` : https://github.com/projectmesa/mesa/


Mesa Packages
--------------------------------------

ABM features users have shared that you may want to use in your model

* `See the Packages <https://github.com/projectmesa/mesa/wiki>`_
* :ref:`Mesa-Packages`


.. toctree::
   :hidden:
   :maxdepth: 6

   Mesa Overview <overview>
   tutorials/intro_tutorial
   tutorials/adv_tutorial
   Best Practices <best-practices>
   API Documentation <apis/api_main>
   Mesa Packages <packages>

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
