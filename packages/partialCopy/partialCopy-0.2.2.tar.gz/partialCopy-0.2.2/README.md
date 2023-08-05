# partialCopy
A tool to copy big data to multiple smaller disks

## Motivation

As the storage becomes larger in big projects, we need to a tool to break large folders (100 TBs) to smaller chunks to be allow to migrate to another location or storing it on tapes.

## Installation

```sudo pip install partialCopy```

## Usage
```
pcp [-h] [-lg LOG] [-ls LST] [-ns NO_SCAN] [-rs RSYNC] src dest

positional arguments:
  src                   Source Directory
  dest                  Dest Mountpoint

optional arguments:
  -h, --help            show this help message and exit
  -lg LOG, --log LOG    Log File to use
  -ls LST, --lst LST    List File to use
  -ns, --no-scan        Don't rescan the folder, this needs a previous run
  -rs RSYNC, --rsync RSYNC         Extra rsync parameters
```

## Notes

* A log file will be written as $src/.pcp_log (by default)
* A list file will be written as $src/.pcp_lst (by default)
* The conf file is /etc/pcp.cfg
* A user can has his own config as ~/.pcp.cfg
* When the dest is full, the exit code is -125

# Contributors
* [Zeeshan Ali Shah](https://github.com/zeeshanali)
