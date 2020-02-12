kibana-config-transfer
=========

Small package for backup/restore kibana config (search_templates/dashboards)


Requirements
------------

Python 3 or higher

python libs:
  - requests


Usage
------

transfer.py <option>

Options:
  - backup (for backup configuration)
  - restore (for restore configucation)

env variables:
  - GIT_REPO
  - ELASTICSEARCH_URL


Script work-line
----------------

backup:
1) Create local copy of remote repo
2) Search for config in elasticsearch
3) If found - save data in local files
4) Check git status
5) If new files make changes - add, commit, push

restore:
1) Read data from local files
2) Put to elasticsearch


License
-------

MIT

Author Information
------------------

Aleksey Demidov
