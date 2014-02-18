# ansible-zwift #

This is a work in progress.

## Requirements ##

We require ansible1.4, pyrax, and python-ipaddr

## Quick instructions ## 

source a rax environment (novarc / openrc format), then run the
provision.yml playbook:

    ansible-playbook provision.yml -e rax_keypair=NameOfYourKeyPair

if you want a cluster named something other than "c1", add the extra
arg `prefix`:

    ansible-playbook provision.yml -e prefix=c2

Once the cluster has clusterated, you can configure the cluster by
running configure.yml. Limit the cluster to the cluster you created
using -l:

    ansible-playbook configure.yml -l c1 -e prefix=c1

There are tags and stuff you can use too.  Some variables as well.  Meh.
