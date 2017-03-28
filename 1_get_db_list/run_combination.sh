#/bin/bash -e

DB_PATH=/home/shinmc/caffe/workspace/facial_expression/database/preprocessed/Combination
DB_LIST_PATH=/home/shinmc/caffe/workspace/facial_expression/db_list/Hist-eq/Combination

# C1
TARGET='C1'
python get_db_list.py $DB_PATH/$TARGET $DB_LIST_PATH/$TARGET

# C2
TARGET='C2'
python get_db_list.py $DB_PATH/$TARGET $DB_LIST_PATH/$TARGET

# C3
TARGET='C3'
python get_db_list.py $DB_PATH/$TARGET $DB_LIST_PATH/$TARGET

# C4
TARGET='C4'
python get_db_list.py $DB_PATH/$TARGET $DB_LIST_PATH/$TARGET

# C5
TARGET='C5'
python get_db_list.py $DB_PATH/$TARGET $DB_LIST_PATH/$TARGET

# C6
TARGET='C6'
python get_db_list.py $DB_PATH/$TARGET $DB_LIST_PATH/$TARGET

# C7
TARGET='C7'
python get_db_list.py $DB_PATH/$TARGET $DB_LIST_PATH/$TARGET

# C8
TARGET='C8'
python get_db_list.py $DB_PATH/$TARGET $DB_LIST_PATH/$TARGET

# C9
TARGET='C9'
python get_db_list.py $DB_PATH/$TARGET $DB_LIST_PATH/$TARGET

# C10
TARGET='C10'
python get_db_list.py $DB_PATH/$TARGET $DB_LIST_PATH/$TARGET

# C11
TARGET='C11'
python get_db_list.py $DB_PATH/$TARGET $DB_LIST_PATH/$TARGET

# C12
TARGET='C12'
python get_db_list.py $DB_PATH/$TARGET $DB_LIST_PATH/$TARGET

# C13
TARGET='C13'
python get_db_list.py $DB_PATH/$TARGET $DB_LIST_PATH/$TARGET

# C14
TARGET='C14'
python get_db_list.py $DB_PATH/$TARGET $DB_LIST_PATH/$TARGET

# C15
TARGET='C15'
python get_db_list.py $DB_PATH/$TARGET $DB_LIST_PATH/$TARGET
