# ansible-zwift #

This is a work in progress.

Quick instructions: source a rax environment, then run the
provision.yml playbook:

    ansible-playbook provision.yml -e rax_keypair=NameOfYourKeyPair

if you want a cluster named something other than "c1", add the extra
arg `prefix`:

    ansible-playbook provision.yml -e c2

Once the cluster has clusterated, you can configure the cluster by
running configure.yml. Limit the cluster to the cluster you created
using -l:

    ansible-playbook configure.yml -l c1

There are tags and stuff you can use too.  Some variables as well.  Meh.
