Gotcha's
========

Relative imports
----------------

When importing a file it is important to know that if you're using
relative imports the path of the file is relative to the master
(top-level) file. Using absolute imports makes this unnecessary.

**Example**::

    .
    ├── app_settings
    │   ├── db.json
    │   ├── general.json
    │   └── logging.json
    ├── dev.json    # <- imports should be relative to this level
    ├── prod.json
    └── test.json
