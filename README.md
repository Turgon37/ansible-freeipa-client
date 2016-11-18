Ansible Role IPA-Client configuration
========

This roles allow configuration of an ipa-client

## OS Family

This role is available for Debian and CentOS

## Features

At this day the role can be used to configure :

  * Automatic configuration for host with have ipa-client available
  * Partial manual installation for other

## Prerequisites

Before try to enroll a new client you have to obtains the certificate authority chains and to put it into the path defined by ```freeipa_client__ca_path``` parameter (default /etc/ipa/ipa.crt).
Please ensure that this file world readable

### Manual installation

The manual installation include Kerberos configuration and SSSD configuration but some tasks are required to be made manually by an human.

  * Before to start the ansible role on a host when only manual install is available, you have to execute theses operation on the IPA server:

```
ipa host-add --ip-address=IP_ADDRESS_OF_THE_FUTURE_CLIENT new-client.domain.com
ipa host-add-managedby --hosts=ipa-server.example.com new-client.domain.com
ipa-getkeytab -s ipa-server.example.com -p host/new-client.domain.com@DOMAIN.COM -k /tmp/deb.keytab
```

Then copy the keytab from /tmp/deb.keytab to client in /etc/krb5.keytab


## Configuration

The variables that can be passed to this role and a brief description about them are as follows:

| Name                           | Description                                                                      |
| ------------------------------ | -------------------------------------------------------------------------------- |
| freeipa_client__server         | The full fqdn of the IPA server                                                  |
| freeipa_client__domain         | The domain realm of the IPA server you want to join to                           |
| freeipa_client__enroll_user    | The username of the administrative account                                       |
| freeipa_client__enroll_pass    | The password of the administrative account given above                           |
| freeipa_client__hostname       | The full fqdn of the client, it will appear in the IPA server during enrollment  |
| freeipa_client__manual_install | If True the client installation will be performed manually (only kerberos, sssd) |