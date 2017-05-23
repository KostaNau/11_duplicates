# Anti-Duplicator

## Description
The script finds files with equal name and size or with hash comparison in a target directory.


## How to use
Run the script with absolute path to the target directory for basic comparison. For comparison files by hash, add optional argument ```--md5 True```. 
By default optional argument ```--md5``` is ```False```.


## Example
Equal name and size:
```python duplicates.py /some/path```

Hash comparison:
```python duplicates.py /some/path --md5 True```

### Output
```
File name: filename
Path: /some/path/dir/filename
Path: /some/path/other_dir/filename
==========================================================
```


# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
