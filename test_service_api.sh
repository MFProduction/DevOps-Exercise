#!/bin/bash

function output() {
  if [[ $(echo $response | jq .error?) = "null" ]]
  then
    type=$(echo $response  | jq .type | cut -d "\"" -f 2 )
    text=$(echo $response  | jq .text | cut -d "\"" -f 2 )
    range=$(echo $response | jq .range )
    echo "[$(date +"%Y-%m-%d_%T")] GET $url: Type: $type Range: $range  Text: $text"
  else
    error=$(echo $response | jq .error | cut -d "\"" -f 2)
    echo "[$(date +"%Y-%m-%d_%T")] GET $url: Error: $error"
  fi
}

function call_api() {
  curl -s h $url
}

function test_api() {
  for i in {1..1000}
  do
    endpoint=$(( ( RANDOM % 4 )  + 1 ))
    if [[ endpoint -eq 1 ]]
    then
      url="http://mockbin.org/bin/d21a0e91-05aa-491b-a4a0-d795aeadb24d"
      response=$(call_api $url)
      output $response $url
    elif [[ endpoint -eq 2 ]]
    then
      url="http://mockbin.org/bin/f017a29e-8ef5-4929-9219-542c5016af4e"
      response=$(curl -s $url)
      output $response $url
    elif [[ endpoint -eq 3 ]]
    then
      url="http://mockbin.org/bin/3379d830-7fd9-4c43-8fce-eb0b91145697"
      response=$(curl -s $url)
      output $response $url
    elif [[ endpoint -eq 4 ]]
    then
      url="http://mockbin.org/bin/1f070f39-3781-4213-8fe1-71e072fb9128"
      response=$(curl -s $url)
      output $response $url
    else
      echo "ERROR: Endpont not found"
      exit 1
    fi
  done
}

echo "Testing service API:"
test_api
echo "Done."
