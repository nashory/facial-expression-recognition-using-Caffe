#/bin/bash -e


CAFFE_ROOT=/home/shinmc/caffe
PROJECT_PATH=$CAFFE_ROOT/workspace/facial_expression
TEST_PATH=$PROJECT_PATH/3_Pretrain/fer2013/model/Tang

TARGET=fer2013
test_model=$TEST_PATH/BestModel/fer2013_Tang_iter_120000.caffemodel
test_deploy=$TEST_PATH/test/test_deploy.prototxt
lmdb_path=$PROJECT_PATH/lmdb/$TARGET/Hist-eq/test_lmdb



python ./Test.py $test_model $test_deploy $lmdb_path

