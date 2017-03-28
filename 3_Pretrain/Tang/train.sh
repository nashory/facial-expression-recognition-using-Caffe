#!/usr/bin/env sh
set -e

TARGET=fer2013
CAFFE_ROOT=/home/shinmc/caffe
PROJECT_PATH=$CAFFE_ROOT/workspace/facial_expression
TOOLS=$CAFFE_ROOT/build/tools
SOLVER=/home/shinmc/caffe/workspace/facial_expression/3_Pretrain/fer2013/model/Tang/model/solver.prototxt
LOG=/home/shinmc/caffe/workspace/facial_expression/3_Pretrain/fer2013/model/Tang/result/log/log.txt

$TOOLS/caffe train \
    --solver=$SOLVER 2>&1 | tee $LOG
