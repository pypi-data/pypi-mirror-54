A simple module used to count or list the attributes of files in a directory.
This module can be used from the command line, with the command `countfiles`.

### Usage (CLI):

    countfiles <directory> [options...]

### Usage (Python):

    import countfiles

    counter = countfiles.Counter(path='.', count=True, size=False)
    counter.call()

### Options include:
- `path` (str)
- `count` (bool)
- `size` (bool)
