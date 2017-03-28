#/bin/bash -e

DB_PATH=/home/shinmc/caffe/workspace/facial_expression/database/Combination
OUTPUT_PATH=/home/shinmc/caffe/workspace/facial_expression/database/preprocessed/Combination
RESIZE=48

# C1
DB_NAME=C1
python Combination_Hist-eq_and_resize.py $DB_NAME $DB_PATH/$DB_NAME $OUTPUT_PATH/$DB_NAME $RESIZE

# C2
DB_NAME=C2
python Combination_Hist-eq_and_resize.py $DB_NAME $DB_PATH/$DB_NAME $OUTPUT_PATH/$DB_NAME $RESIZE

# C3
DB_NAME=C3
python Combination_Hist-eq_and_resize.py $DB_NAME $DB_PATH/$DB_NAME $OUTPUT_PATH/$DB_NAME $RESIZE

# C4
DB_NAME=C4
python Combination_Hist-eq_and_resize.py $DB_NAME $DB_PATH/$DB_NAME $OUTPUT_PATH/$DB_NAME $RESIZE

# C5
DB_NAME=C5
python Combination_Hist-eq_and_resize.py $DB_NAME $DB_PATH/$DB_NAME $OUTPUT_PATH/$DB_NAME $RESIZE

# C6
DB_NAME=C6
python Combination_Hist-eq_and_resize.py $DB_NAME $DB_PATH/$DB_NAME $OUTPUT_PATH/$DB_NAME $RESIZE

# C7
DB_NAME=C7
python Combination_Hist-eq_and_resize.py $DB_NAME $DB_PATH/$DB_NAME $OUTPUT_PATH/$DB_NAME $RESIZE

# C8
DB_NAME=C8
python Combination_Hist-eq_and_resize.py $DB_NAME $DB_PATH/$DB_NAME $OUTPUT_PATH/$DB_NAME $RESIZE

# C9
DB_NAME=C9
python Combination_Hist-eq_and_resize.py $DB_NAME $DB_PATH/$DB_NAME $OUTPUT_PATH/$DB_NAME $RESIZE

# C10
DB_NAME=C10
python Combination_Hist-eq_and_resize.py $DB_NAME $DB_PATH/$DB_NAME $OUTPUT_PATH/$DB_NAME $RESIZE

# C11
DB_NAME=C11
python Combination_Hist-eq_and_resize.py $DB_NAME $DB_PATH/$DB_NAME $OUTPUT_PATH/$DB_NAME $RESIZE

# C12
DB_NAME=C12
python Combination_Hist-eq_and_resize.py $DB_NAME $DB_PATH/$DB_NAME $OUTPUT_PATH/$DB_NAME $RESIZE

# C13
DB_NAME=C13
python Combination_Hist-eq_and_resize.py $DB_NAME $DB_PATH/$DB_NAME $OUTPUT_PATH/$DB_NAME $RESIZE

# C14
DB_NAME=C14
python Combination_Hist-eq_and_resize.py $DB_NAME $DB_PATH/$DB_NAME $OUTPUT_PATH/$DB_NAME $RESIZE

# C15
DB_NAME=C15
python Combination_Hist-eq_and_resize.py $DB_NAME $DB_PATH/$DB_NAME $OUTPUT_PATH/$DB_NAME $RESIZE





















