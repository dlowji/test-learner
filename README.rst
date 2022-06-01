Learner Pathway Progress
=============================

|pypi-badge| |ci-badge| |codecov-badge| |doc-badge| |pyversions-badge|
|license-badge|


Overview
------------------------
Learner-pathway-progress is a plugin that is supposed to be installed inside the ``edx-platform`` and integrated in ``lms``, it contains the code to track the progress of learners in learner pathways.


Development Workflow
--------------------

One Time Setup
~~~~~~~~~~~~~~
.. code-block::

  # Clone the repository
  git clone git@github.com:edx/learner-pathway-progress.git
  cd learner-pathway-progress

  # Set up a virtualenv using virtualenvwrapper with the same name as the repo and activate it
  mkvirtualenv -p python3.8 learner-pathway-progress


Every time you develop something in this repo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block::

  # Activate the virtualenv
  workon learner-pathway-progress

  # Grab the latest code
  git checkout master
  git pull

  # Install/update the dev requirements
  make requirements

  # Run the tests and quality checks (to verify the status before you make any changes)
  make validate

  # Make a new branch for your changes
  git checkout -b <your_github_username>/<short_description>

  # Using your favorite editor, edit the code to make your change.
  vim …

  # Run your new tests
  pytest ./path/to/new/tests

  # Run all the tests and quality checks
  make validate

  # Commit all your changes
  git commit …
  git push

  # Open a PR and ask for review.

License
-------

The code in this repository is licensed under the AGPL 3.0 unless
otherwise noted.

Please see `LICENSE.txt <LICENSE.txt>`_ for details.

How To Contribute
-----------------

Contributions are very welcome.
Please read `How To Contribute <https://github.com/edx/edx-platform/blob/master/CONTRIBUTING.rst>`_ for details.
Even though they were written with ``edx-platform`` in mind, the guidelines
should be followed for all Open edX projects.

The pull request description template should be automatically applied if you are creating a pull request from GitHub. Otherwise you
can find it at `PULL_REQUEST_TEMPLATE.md <.github/PULL_REQUEST_TEMPLATE.md>`_.

The issue report template should be automatically applied if you are creating an issue on GitHub as well. Otherwise you
can find it at `ISSUE_TEMPLATE.md <.github/ISSUE_TEMPLATE.md>`_.

Reporting Security Issues
-------------------------

Please do not report security issues in public. Please email security@edx.org.

Getting Help
------------

If you're having trouble, we have discussion forums at https://discuss.openedx.org where you can connect with others in the community.

Our real-time conversations are on Slack. You can request a `Slack invitation`_, then join our `community Slack workspace`_.

For more information about these options, see the `Getting Help`_ page.

.. _Slack invitation: https://openedx-slack-invite.herokuapp.com/
.. _community Slack workspace: https://openedx.slack.com/
.. _Getting Help: https://openedx.org/getting-help

.. |pypi-badge| image:: https://img.shields.io/pypi/v/learner-pathway-progress.svg
    :target: https://pypi.python.org/pypi/learner-pathway-progress/
    :alt: PyPI

.. |ci-badge| image:: https://github.com/edx/learner-pathway-progress/workflows/Python%20CI/badge.svg?branch=master
    :target: https://github.com/edx/learner-pathway-progress/actions
    :alt: CI

.. |codecov-badge| image:: https://codecov.io/github/edx/learner-pathway-progress/coverage.svg?branch=master
    :target: https://codecov.io/github/edx/learner-pathway-progress?branch=master
    :alt: Codecov

.. |doc-badge| image:: https://readthedocs.org/projects/learner-pathway-progress/badge/?version=latest
    :target: https://learner-pathway-progress.readthedocs.io/en/latest/
    :alt: Documentation

.. |pyversions-badge| image:: https://img.shields.io/pypi/pyversions/learner-pathway-progress.svg
    :target: https://pypi.python.org/pypi/learner-pathway-progress/
    :alt: Supported Python versions

.. |license-badge| image:: https://img.shields.io/github/license/edx/learner-pathway-progress.svg
    :target: https://github.com/edx/learner-pathway-progress/blob/master/LICENSE.txt
    :alt: License
