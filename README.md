kibana-config-transfer
=========

Small package for backup/restore kibana config (visualization/search/dashboards/index-pattern)


Requirements
------------

Python 3 or higher

python libs:
  - requests


Compability
------------
| Kibana version | Backuper tool version |
| --- | --- |
| 4.* | 0.0.2 |
| 6.* | 0.0.5 |
| 7.6+ | 0.0.6 |


Usage
------

transfer.py <option>

Options:
  - backup (for backup configuration)
  - restore (for restore configucation)

env variables:
  - GIT_REPO
  - GIT_BRANCH (for backup/restore. default: master)
  - KIBANA_URL
  - KIBANA_BACKUP_PREFIX (optional parameter. If defined, will backup only objects which includes prefix)


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
2) Post to kibana


License
-------

MIT

Author Information
------------------

Aleksey Demidov
