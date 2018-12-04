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
protosync source 85736c2686be4218ba789a50e2425564
```
Run this command in your **local** source directory.
 
You'll see it print:
```
Code synced to remote directory
```

And that's it! 

You local code has now been synced to the remote server.  
Just enter the same command wheneve you want to sync.

**Note:** you'll need to keep the remote terminal running for the sync to work.

### Facts

* Protosync uses your ```.gitignore``` file to automatically ignore unnecessary files.
* If you're worried about network usage, Protosync generates about **2kb/s** of traffic.
