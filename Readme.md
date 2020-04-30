# Webpage Update Notifier Daemon
Wund is a simple python daemon that will check if the content
of a website page is updated.
# Install
The daemon require the following python package:
```
sqlite
requests
notify2
```
To install `git clone` this repo and put `Wund.py` in your path or a symlink to it.
# Usage
+ To start the daemon run:
```{sh}
$ python3 Wund.py --daemon
```
+ To add website to the check:
```{sh}
$ python3 Wund.py --insert URL
```
+ To remove website:
```{sh}
$ python3 Wund.py --remove URL
```
+ To list the website the daemon is checking:
```{sh}
$ python3 Wund.py --list
```
