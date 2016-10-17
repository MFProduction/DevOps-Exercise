#!/bin/bash
if [[ $1 == "test" ]]
then
  ./test_service_api.sh
else
  python2.7 mind_the_gap.py $@
fi
