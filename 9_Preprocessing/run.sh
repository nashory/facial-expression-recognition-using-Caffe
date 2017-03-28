#/bin/bash -e

DB_PATH=/home/shinmc/caffe/workspace/facial_expression/database/detected
OUTPUT_PATH=/home/shinmc/caffe/workspace/facial_expression/database/preprocessed
RESIZE=48

# FER2013
#DB_NAME=fer2013
#python Hist-eq_and_resize.py $DB_NAME $DB_PATH/$DB_NAME $OUTPUT_PATH/$DB_NAME $RESIZE

# SFEW
#DB_NAME=SFEW
#python Hist-eq_and_resize.py $DB_NAME $DB_PATH/$DB_NAME $OUTPUT_PATH/$DB_NAME $RESIZE

# KDEF
#DB_NAME=KDEF
#python Hist-eq_and_resize.py $DB_NAME $DB_PATH/$DB_NAME $OUTPUT_PATH/$DB_NAME $RESIZE

# CK_plus
#DB_NAME=CKplus
#python Hist-eq_and_resize.py $DB_NAME $DB_PATH/$DB_NAME $OUTPUT_PATH/$DB_NAME $RESIZE

# Jaffe
#DB_NAME=Jaffe
#python Hist-eq_and_resize.py $DB_NAME $DB_PATH/$DB_NAME $OUTPUT_PATH/$DB_NAME $RESIZE

# mixed
DB_NAME=mixed
python Hist-eq_and_resize.py $DB_NAME $DB_PATH/$DB_NAME $OUTPUT_PATH/$DB_NAME $RESIZE
