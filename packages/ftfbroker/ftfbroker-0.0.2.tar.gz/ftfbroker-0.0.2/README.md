# FTF Broker

[![Build Status](https://travis-ci.org/fachschaft/ftfbroker.svg?branch=master)](https://travis-ci.org/fachschaft/ftfbroker)

This repository contains protobuf schema definitions and typed python consumer/producer for ftf services

## Usage

Usage examples are shown in [cli/](./cli)

## Supported Environment Variables

All supported environment variables are listed and documented in [environment.py](./ftfbroker/environment.py)

## Extending a Protocol Buffer

- You **must not** change the tag numbers of any existing fields.
- You **must not** add or delete any required fields.
- You **may** delete optional or repeated fields.
- You **may** add new optional or repeated fields but you must use fresh tag numbers (i.e. tag numbers that were never used in this protocol buffer, not even by deleted fields).

For further details see [protobuf docs](https://developers.google.com/protocol-buffers/docs/pythontutorial#extending-a-protocol-buffer)

## Release a new version

```shell
$ make release
# Enter version
$ git push --tags
```