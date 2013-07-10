PusherMan
=========

An attempt to create a fab based platform deployment tool as an alternative for chef, puppet and others that require remote services or specially designed deployment files.


To Use
------

If you installed via pip or easy_install or the like, it should put a basic config file under your home directory: ~/.pusher_man/pusher.conf.  In this file you can define a default user or ssh key.


If you are using EC2 and using tags to setup a boto config file.  Like:

    $ cat ~/.boto
    [Credentials]
    aws_access_key_id = <Your Key Here>
    aws_secret_access_key = <Your Secret Here>

There are some sample pusher scripts under samples. To execute them you can do:

    $ superfly -T Name:DEV_NODE_SERVERS install lessc
    $ superfly -H some.server.com -u a_user install lessc

You will need to either be in the directory with lessc directory or use the full path to the lessc directory (or which ever pusher script you are installing).
