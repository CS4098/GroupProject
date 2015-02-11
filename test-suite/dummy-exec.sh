#!/bin/bash

java="java"
cp="./build/classes/main"
real="com.scobd.Translator"
$java -cp $cp $real $1 $2
