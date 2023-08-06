# dfmpy

Sometimes pronounced "_diff-em-py_" and is a small play on words.  dfmpy is 
another Dot-Files Manager, but with robust features that can essentially
"_diff_" the dotfiles actually installed versus the expected installed files.
Hence the "_diff-em_".

dfmpy is not just another dotfiles manager, it supports multiple environments
based on hostname, system type, or a combination of the two.  It also ignores
files/directories based on user defined globs which can be particularly useful
if dfmpy has to traverse directories that have large I/O latencies (large
directory inodes, too many files to stat, or even just network mounted
directories, etc.).

Furthermore, dfmpy is fully customizable!  See the documentation on this page's
***Usage*** section.

# Installation

Since dfmpy is a 
[registered Python package on Pypi](https://pypi.org/project/dfmpy), you can
install dfmpy through the standard `pip` methods.

Install locally as a normal user:

```bash
pip3 install --user --force --upgrade dfmpy
```

Or install globally, as the all powerful root, for all users of the system:

```bash
sudo pip3 install --force --upgrade dfmpy
```

# Usage

TODO

# Config Files

TODO
