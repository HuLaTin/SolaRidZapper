#!/bin/bash

if [ $# -lt 4 ]; then
  echo Command line arguments are required, see examples.
  echo General syntax
  echo $0 triggerVal loopCount fileStem emailID
  echo $0 150 42 backPorch rebelford@ualr.edu
  echo $0 150 42 iLikeBigBugs phwilliams@ualr.edu
  exit
fi

echo start time $(date)

for (( N = 1; N <= $2; N++ ))
do
  echo counter $N
  #./paramsInFilenameWithTriggerWriteToFile.py 40 -2.1 8000 $2Run$N.csv
  #./singleValueTriggerParamsInFilename.py $1 8000 $3Run$N.csv
  #./singleValueTriggerParamsInFilename2chanOnly.py $1 8000 $3Run$N.csv
  ./singleValueTriggerParamsInFilename2chanOnly.py $1 10000 $3Run$N.csv | tee out.tmp
  #./singleEndedMCP3008-v1.py $1 8000 $3Run$N.csv | tee out.tmp
  SENDFILE=$(grep ^outFile ./out.tmp | awk '{print $2}')
  #./emailAttachment.py phwilliams@ualr.edu $SENDFILE
  # ./emailAttachment.py rebelford@ualr.edu $SENDFILE
  ./emailAttachment.py $4 $SENDFILE
done

echo "========================== $0 Done ============================"

############################################################
exit


