# ansible-zwift #

This is a work in progress.


## Requirements ##

We require ansible1.4, pyrax, and python-ipaddr


## Quick instructions ##

source a rax environment (novarc / openrc format), then run the
mkcluster command:

    ./mkcluster -e rax_keypair=NameOfYourKeyPair

if you want a cluster named something other than "c1", add the extra
arg `-c <cluster-prefix>`

    ./mkcluster -c c2 -e rax_keypair=NameOfYourKeyPair

The mkcluster command is a simple wrapper around ansible-playbook on
the provision.yml playbook.  You can look at the mkcluster command and
see how it works.

Once the cluster has clusterated, you can configure the cluster by
running configure.yml.  Limit the cluster to the cluster you created
using -l:

    ansible-playbook configure.yml -l c1 -e prefix=c1

This configuration will set up a zerovm-integrated swift cluster in a
production(ish) way. There will be a proxy server fronted by haproxy
doing ssl termination, talking to apache2 with mod_proxy to unify
static resources (the web ui) as well as the endpoint.

This is a little wonky, but it works for testing, and scales up
reasonably to large cluster size.

Currently, the auth mechanism is swauth, so once the cluster is
initially configured, you should run the one-time swauth setup with:

    ansible-playbook onetime.yml -l c1 -e prefix=c1

After that, http to the public ip of the cluster and play around with
the web ui!
