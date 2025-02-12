#!/usr/bin/env bash

set -ex

/opt/bootstrap.sh
/opt/hive-metastore/bin/start-metastore -p 9083