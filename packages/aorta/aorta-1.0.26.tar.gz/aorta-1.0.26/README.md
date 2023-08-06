# Aorta Message Publishing Library

![IBR Logo](https://media.ibrb.org/ibr/images/logos/landscape1200.png)

The `aorta` library provides various implementations around the
`proton` AMQP messaging framework.

The `aorta` codebase is subject to a feature freeze until test coverage
is at 100%.

## Table of Contents

- [Security](#security)
- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [TODO](#todo)
- [License](#license)


## Security

- Authentication is not implemented. All producers/consumers that can connect
  to the Aorta system are assumed to be allowed to do so, and that access control
  is managed at the network (firewall) level.
- We suggest mounting `/var/spool/aorta` on a separate (encrypted)
  filesystem.
- Implementors must ensure that the `/var/spool/aorta` directory is mounted
  on a filesystem that does not lie when invoking `fsync()`.


## Background


### Message types

The Aorta framework specifies various message types containing
information for interested consumers.

#### Command

A **Command** is the *only* way to change the state of a system. Commands are
responsible for introducing all changes to the system. They are fire-and-forget
and their invocation does not return any value to the caller.


#### Event


#### Task


#### Notify


#### Heartbeat


## Install

## Usage

## TODO

- Authentication.


## License

© 2018 International Blockchain Reserve B.V.
