#!/bin/bash

java="java"
cp="./target/classes"
real="com.scobd.Translator"
$java -cp $cp $real $1 $2
