#!/bin/bash

halLiftover --inMemory --outPsl $1 $2 $3 $4 /dev/stdout | pslPosTarget /dev/stdin $5
