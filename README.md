# Protosync

Protosync solves the problem of seamlessly syncing experimental code between your local development repo and remote server. 

No more need for repeated commits or rsyncs just to get code across.


### Install
```
pip install protosync
```


### Quick Start

In your **local source** directory, enter:
```
protosync source
```
Protosync will then print a command like this:
```
protosync dest 7dd2dd14b3734321a69a5492d69b4c2b
```
Run this command in your **remote destination** directory.
 
You'll see it print:
```
Syncing directory to source
```

And that's it! Just make changes in your local directory and see it automatically synced across to the remote directory. 
