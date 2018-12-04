# Protosync

Protosync syncs code seamlessly between your local development repo and a remote server. 

No more repeated git commits or long rsync commands just to test code out on the server.


### Install
```
pip install protosync
```


### Quick Start

In your **local source** directory, open a **new terminal** and enter:
```
protosync source
```
Protosync will then print a command like this:
```
protosync dest 7dd2dd14b3734321a69a5492d69b4c2b
```
In your **remote destination** directory, open a new terminal and run this command.
 
You'll see it print:
```
Syncing directory to source
```

And that's it! 

Just make changes in your local directory and see it automatically synced across to the remote directory. 

**Note:** you'll need to keep both terminals running for the sync to work.

### Facts

* Protosync uses your ```.gitignore``` file to automatically ignore unnecessary files.
* If you're worried about network usage, Protosync generates about **2kb/s** of traffic.
