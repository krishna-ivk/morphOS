#!/bin/bash

echo "Running tests..."

if ! command -v pytest >/dev/null 2>&1
then
  echo "pytest not found" > test_results.txt
  echo "TEST_FAILURE"
  exit 127
fi

pytest -q > test_results.txt 2>&1
test_status=$?

if [ "$test_status" -ne 0 ]
then
  echo "TEST_FAILURE"
  exit "$test_status"
else
  echo "TEST_SUCCESS"
fi
