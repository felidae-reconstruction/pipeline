#!/bin/bash
set -beEu -o pipefail; /hive/users/ksenia/apps/hal/bin/halLiftover --inMemory --outPSL $1 $2 $3 $4  /scratch/tmp/liftover.bed ;  pslPosTarget /scratch/tmp/liftover.bed $5; rm /scratch/tmp/liftover.bed
