.. image:: https://gitlab.com/gitlab-automation-toolkit/gitlab-auto-mr/badges/master/pipeline.svg
   :target: https://gitlab.com/gitlab-automation-toolkit/gitlab-auto-mr
   :alt: Pipeline Status

.. image:: https://img.shields.io/pypi/l/gitlab-auto-mr.svg
   :target: https://pypi.org/project/gitlab-auto-mr/
   :alt: PyPI Project License

.. image:: https://img.shields.io/pypi/v/gitlab-auto-mr.svg
   :target: https://pypi.org/project/gitlab-auto-mr/
   :alt: PyPI Project Version

.. image:: https://readthedocs.org/projects/gitlab-auto-mr/badge/?version=latest
   :target: https://gitlab-auto-mr.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

GitLab Auto MR
==============

This is a simple Python cli script that allows you create MR in GitLab automatically. It is intended to be
used during your CI/CD. However you can chose to use it however you wish.

It is based on the script and idea of `Riccardo Padovani <https://rpadovani.com>`_,
which he introduced with his blog post
`How to automatically create new MR on Gitlab with Gitlab CI <https://rpadovani.com/open-mr-gitlab-ci>`_.

Usage
-----

First you need to create a personal access token,
`more information here <https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html>`_.
With the scope ``api``, so it can create the MR using your API. This access token is passed
to the script with the ``--private-token`` argument.

.. code-block:: bash

    pip install gitlab-auto-mr
    gitlab_auto_mr --help

  Usage: gitlab_auto_mr [OPTIONS]

    Gitlab Auto MR Tool.

  Options:
    --private-token TEXT      Private GITLAB token, used to authenticate when
                              calling the MR API.  [required]
    --source-branch TEXT      The source branch to merge into.  [required]
    --project-id INTEGER      The project ID on GitLab to create the MR for.
                              [required]
    --project-url TEXT        The project URL on GitLab to create the MR for.
                              [required]
    --user-id INTEGER         The GitLab user ID to assign the created MR to.
                              [required]
    -t, --target-branch TEXT  The target branch to merge onto.
    -c, --commit-prefix TEXT  Prefix for the MR title i.e. WIP.
    -r, --remove-branch       Set to True if you want the source branch to be
                              removed after MR.
    -s, --squash-commits      Set to True if you want commits to be squashed.
    -d, --description TEXT    Path to file to use as the description for the MR.
    --use-issue-name          If set to True will use information from issue in
                              branch name, must be in the form #issue-number,
                              i.e feature/#6.
    --allow-collaboration     If set to True allow, commits from members who can
                              merge to the target branch.
    --help                    Show this message and exit.


.. code-block:: bash

    gitlab_auto_mr --private-token $(private_token) --source-branch feature/test --project-id 5 \
                    --project-url https://gitlab.com/stegappasaurus/stegappasaurus-app --user-id 5

GitLab CI
*********

``GITLAB_PRIVATE_TOKEN`` Set a secret variable in your GitLab project with your private token. Name it
GITLAB_PRIVATE_TOKEN (``CI/CD > Environment Variables``). This is necessary to raise the Merge Request on your behalf.
More information `click here <https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html>`_.
An example CI using this can be found
`here <https://gitlab.com/hmajid2301/stegappasaurus/blob/a22b7dc80f86b471d8a2eaa7b7eadb7b492c53c7/.gitlab-ci.yml>`_,
look for the ``create:merge-request`` job.

Add the following to your ``.gitlab-ci.yml`` file:

.. code-block:: yaml

  stages:
    - open

  open_merge_request:
    image: registry.gitlab.com/gitlab-automation-toolkit/gitlab-auto-mr
    before_script: [] # We do not need any setup work, let's remove the global one (if any)
    variables:
      GIT_STRATEGY: none # We do not need a clone of the GIT repository to create a Merge Request
    stage: open
    script:
      - gitlab_auto_mr -t master -c WIP -d ./.gitlab/merge_request/merge_request.md -r -s --use-issue-name


Predefined Variables
^^^^^^^^^^^^^^^^^^^^

Please note some of the arguments can be filled in using environment variables defined during GitLab CI.
For more information `click here <https://docs.gitlab.com/ee/ci/variables/predefined_variables.html>_`.

* If ``--private-token`` is not set the script will look for the ENV variable ``GITLAB_PRIVATE_TOKEN``
* If ``--source-branch`` is not set the script will look for the ENV variable ``CI_COMMIT_REF_NAME``
* If ``--project-id`` is not set it will look for for the ENV variable ``CI_PROJECT_ID``
* If ``--project-url`` is not set it will look for for the ENV variable ``CI_PROJECT_URL``
* If ``--user-id`` is not set it will look for for the ENV variable ``GITLAB_USER_ID``


Development
===========

.. code-block:: bash

  git clone git@gitlab.com:gitlab-automation-toolkit/gitlab-auto-mr.git
  cd gitlab-auto-mr
  pip install tox
  make virtualenv

Changelog
=========

You can find the `changelog here <https://gitlab.com/gitlab-automation-toolkit/gitlab-auto-mr/blob/master/CHANGELOG.md>`_.

Appendix
========

- Extra features: `Allsimon <https://gitlab.com/Allsimon/gitlab-auto-merge-request>`_
- Forked from: `Tobias L. Maier <https://gitlab.com/tmaier/gitlab-auto-merge-request>`_
- Script and idea: `Riccardo Padovani <https://rpadovani.com>`_
