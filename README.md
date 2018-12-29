# Protosync

Protosync syncs code seamlessly between your local development repo and a remote server. 

No more repeated git commits or long rsync commands just to test code out on the server.


### Install
```
pip install protosync
```


### Quick Start

In your **remote** directory, open a **new terminal** and enter:
```
protosync dest
```
Protosync will then print a command like this:
```
protosync source m0X1a-km0C6mCzWkl56xO0-hUQvYrhL0q5I5lK5qZgU=
```
Run this command in your **local** source directory.

And that's it! 

You local code will now be synced to the remote server.  

Just enter the same command whenever you want to sync again.

**Note:** you'll need to keep the remote terminal running for the sync to work.

### Facts

* Protosync uses your ```.gitignore``` to automatically ignore unnecessary files.
* Protosync ignores files larger than **5Mb** to prevent syncing of unwanted binaries.
* Protosync uses **end-to-end encryption** when syncing your files. The server **cannot** decrypt your data.
