#!/bin/bash
halLiftover --inMemory --outPSL $1 $2 $3 $4 /dev/stdout | pslPosTarget /dev/stdin $5
