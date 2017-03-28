#/bin/bash -e

DB_PATH=/home/shinmc/caffe/workspace/facial_expression/database/preprocessed
DB_LIST_PATH=/home/shinmc/caffe/workspace/facial_expression/db_list/Hist-eq



# fer2013 train
TARGET='fer2013'
USAGE='train'
python get_db_list.py $DB_PATH/$TARGET/$USAGE $DB_LIST_PATH/$TARGET/$USAGE

# fer2013 test
TARGET='fer2013'
USAGE='test'
python get_db_list.py $DB_PATH/$TARGET/$USAGE $DB_LIST_PATH/$TARGET/$USAGE

# fer2013 val
TARGET='fer2013'
USAGE='val'
python get_db_list.py $DB_PATH/$TARGET/$USAGE $DB_LIST_PATH/$TARGET/$USAGE



# KDEF train
TARGET='KDEF'
USAGE='train'
python get_db_list.py $DB_PATH/$TARGET/$USAGE $DB_LIST_PATH/$TARGET/$USAGE

# KDEF test
TARGET='KDEF'
USAGE='test'
python get_db_list.py $DB_PATH/$TARGET/$USAGE $DB_LIST_PATH/$TARGET/$USAGE

# KDEF val
TARGET='KDEF'
USAGE='val'
python get_db_list.py $DB_PATH/$TARGET/$USAGE $DB_LIST_PATH/$TARGET/$USAGE



# CK+ train
TARGET='CKplus'
USAGE='train'
python get_db_list.py $DB_PATH/$TARGET/$USAGE $DB_LIST_PATH/$TARGET/$USAGE

# CK+ test
TARGET='CKplus'
USAGE='test'
python get_db_list.py $DB_PATH/$TARGET/$USAGE $DB_LIST_PATH/$TARGET/$USAGE

# CK+ val
TARGET='CKplus'
USAGE='val'
python get_db_list.py $DB_PATH/$TARGET/$USAGE $DB_LIST_PATH/$TARGET/$USAGE



# SFEW train
TARGET='SFEW'
USAGE='train'
python get_db_list.py $DB_PATH/$TARGET/$USAGE $DB_LIST_PATH/$TARGET/$USAGE

# SFEW test
TARGET='SFEW'
USAGE='test'
python get_db_list.py $DB_PATH/$TARGET/$USAGE $DB_LIST_PATH/$TARGET/$USAGE

# SFEW val
TARGET='SFEW'
USAGE='val'
python get_db_list.py $DB_PATH/$TARGET/$USAGE $DB_LIST_PATH/$TARGET/$USAGE





# Jaffe train
TARGET='Jaffe'
USAGE='train'
python get_db_list.py $DB_PATH/$TARGET/$USAGE $DB_LIST_PATH/$TARGET/$USAGE

# Jaffe test
TARGET='Jaffe'
USAGE='test'
python get_db_list.py $DB_PATH/$TARGET/$USAGE $DB_LIST_PATH/$TARGET/$USAGE

# Jaffe val
TARGET='Jaffe'
USAGE='val'
python get_db_list.py $DB_PATH/$TARGET/$USAGE $DB_LIST_PATH/$TARGET/$USAGE

# Jaffe all
TARGET='Jaffe'
USAGE='all'
python get_db_list.py $DB_PATH/$TARGET/$USAGE $DB_LIST_PATH/$TARGET/$USAGE






# mixed train
TARGET='mixed'
USAGE='train'
python get_db_list.py $DB_PATH/$TARGET/$USAGE $DB_LIST_PATH/$TARGET/$USAGE

# mixed test
TARGET='mixed'
USAGE='test'
python get_db_list.py $DB_PATH/$TARGET/$USAGE $DB_LIST_PATH/$TARGET/$USAGE

# mixed val
TARGET='mixed'
USAGE='val'
python get_db_list.py $DB_PATH/$TARGET/$USAGE $DB_LIST_PATH/$TARGET/$USAGE





