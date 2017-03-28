#!/usr/bin/env sh
# Create the imagenet lmdb inputs
# N.B. set the path to the imagenet train + val data dirs
set -e

TARGET=KDEF
PREPROCESS=Hist-eq
CAFFE_ROOT=/home/shinmc/caffe
PROJECT_PATH=$CAFFE_ROOT/workspace/facial_expression
LMDB_OUTPUT=$PROJECT_PATH/lmdb/$TARGET/$PREPROCESS
DB_LIST=$PROJECT_PATH/db_list/$PREPROCESS/$TARGET
TOOLS=$CAFFE_ROOT/build/tools

TRAIN_DATA_ROOT=$PROJECT_PATH/database/preprocessed/$TARGET/train/
TRAIN_LMDB_OUTPUT=$LMDB_OUTPUT/train_lmdb

TEST_DATA_ROOT=$PROJECT_PATH/database/preprocessed/$TARGET/test/
TEST_LMDB_OUTPUT=$LMDB_OUTPUT/test_lmdb

VAL_DATA_ROOT=$PROJECT_PATH/database/preprocessed/$TARGET/val/
VAL_LMDB_OUTPUT=$LMDB_OUTPUT/val_lmdb



# Set RESIZE=true to resize the images to 256x256. Leave as false if images have
# already been resized using another tool.
RESIZE=false
if $RESIZE; then
  RESIZE_HEIGHT=96
  RESIZE_WIDTH=96
else
  RESIZE_HEIGHT=0
  RESIZE_WIDTH=0
fi

if [ ! -d "$TRAIN_DATA_ROOT" ]; then
  echo "Error: VAL_DATA_ROOT is not a path to a directory: $VAL_DATA_ROOT"
  echo "Set the VAL_DATA_ROOT variable in create_imagenet.sh to the path" \
       "where the ImageNet validation data is stored."
  exit 1
fi

if [ ! -d "$TEST_DATA_ROOT" ]; then
  echo "Error: VAL_DATA_ROOT is not a path to a directory: $VAL_DATA_ROOT"
  echo "Set the VAL_DATA_ROOT variable in create_imagenet.sh to the path" \
       "where the ImageNet validation data is stored."
  exit 1
fi

if [ ! -d "$VAL_DATA_ROOT" ]; then
  echo "Error: VAL_DATA_ROOT is not a path to a directory: $VAL_DATA_ROOT"
  echo "Set the VAL_DATA_ROOT variable in create_imagenet.sh to the path" \
       "where the ImageNet validation data is stored."
  exit 1
fi

rm -rf $TRAIN_LMDB_OUTPUT
rm -rf $TEST_LMDB_OUTPUT
rm -rf $VAL_LMDB_OUTPUT



# Create LMDB.
echo "Creating train lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --resize_height=$RESIZE_HEIGHT \
    --resize_width=$RESIZE_WIDTH \
    --shuffle \
    $TRAIN_DATA_ROOT \
    $DB_LIST/train/db_list.txt \
    $TRAIN_LMDB_OUTPUT
echo "Creating train lmdb mean proto..."
$TOOLS/compute_image_mean $TRAIN_LMDB_OUTPUT \
  $TRAIN_LMDB_OUTPUT/mean.binaryproto

echo "Creating test lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --resize_height=$RESIZE_HEIGHT \
    --resize_width=$RESIZE_WIDTH \
    --shuffle \
    $TEST_DATA_ROOT \
    $DB_LIST/test/db_list.txt \
    $TEST_LMDB_OUTPUT
echo "Creating test lmdb mean proto..."
$TOOLS/compute_image_mean $TEST_LMDB_OUTPUT \
  $TEST_LMDB_OUTPUT/mean.binaryproto

echo "Creating val lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --resize_height=$RESIZE_HEIGHT \
    --resize_width=$RESIZE_WIDTH \
    --shuffle \
    $VAL_DATA_ROOT \
    $DB_LIST/val/db_list.txt \
    $VAL_LMDB_OUTPUT
echo "Creating val lmdb mean proto..."
$TOOLS/compute_image_mean $VAL_LMDB_OUTPUT \
  $VAL_LMDB_OUTPUT/mean.binaryproto


echo "======================================================="
echo "Congrats! Process has been sucessfully Done."






