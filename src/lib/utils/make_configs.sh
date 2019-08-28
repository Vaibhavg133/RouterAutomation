#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

TEST_DIR=${DIR}/../../tests

find ${TEST_DIR} -name "*.csv" -exec rm {} \;
find ${TEST_DIR} -name "*.json" -exec rm {} \;

sleep 1
find ${TEST_DIR} -name "*.conf" -exec /usr/bin/python config_to_csv.py {} \;
find ${TEST_DIR} -name "*.csv"  -exec /usr/bin/python csv_reader.py {} \;
find ${TEST_DIR} -name "*.json" -exec bash -c 'mkdir -p $(dirname "$0")/../json; mv $0 $(dirname "$0")/../json/' {} \;
find ${TEST_DIR} -name "*.csv" -exec bash -c 'mkdir -p $(dirname "$0")/../csv; mv $0 $(dirname "$0")/../csv/' {} \;
