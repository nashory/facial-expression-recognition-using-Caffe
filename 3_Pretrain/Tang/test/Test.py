# ------------------------------------------
# Coded by M.C.SHIN
# Last modified : 2016.09.25
#
#
#-------------------------------------------

import caffe
import numpy as np
import lmdb
import sys, os
from mc_caffe import *
from caffe.proto import caffe_pb2




## Specify the path
CAFFE_ROOT = '/home/shinmc/caffe/'
PROJECT_PATH = CAFFE_ROOT + 'workspace/activity/database/ImageNet'
test_model = '../model/pretrain/VGG_weights_16.caffemodel'
test_deploy = '/home/shinmc/caffe/workspace/activity/database/ImageNet/2_Test/model/test/test_ImageNet_deploy.prototxt'
lmdb_path = '/home/shinmc/caffe/workspace/activity/database/ImageNet/lmdb'
#lmdb_path = '/home/shinmc/caffe/workspace/activity/database/UCF101/lmdb/1_keyframes/val_lmdb'

def __Debug_lmdb(image):
	image = np.transpose(image, (1,2,0))			# original (dim, col, row)
	plt.imshow(image)
	plt.show()

if __name__=='__main__':

	if (len(sys.argv) != 4):
		print "[ERROR] Wrong input!"
		print "[USAGE] ./Test.py [caffemodel] [deploy.prototxt] [lmdb_path]"


	# Set GPU mode ON.
	SetUp('gpu',0)

	# input arguments.
	test_model = sys.argv[1]
	test_deploy = sys.argv[2]
	lmdb_path = sys.argv[3]
	
	# Load network.
	print "[TRY] Loading trained network model."
	test_net = caffe.Net(test_deploy, test_model, caffe.TEST)
	print "[SUCCESS] Successfully loaded the network."


	## Add transformer.
	transformer = caffe.io.Transformer({'data': test_net.blobs['data'].data.shape})
	transformer.set_transpose('data', (2,0,1))

	# Read mean.binaryproto and set mean_pixel.
	mean_file = lmdb_path + '/mean.binaryproto'
	blob = caffe.proto.caffe_pb2.BlobProto()
	data = open( mean_file , 'rb' ).read()
	blob.ParseFromString(data)
	mean = np.array( caffe.io.blobproto_to_array(blob) )[0]
	mean_pixel = mean
	transformer.set_mean('data', mean_pixel)	
	
	# scale range 0~255
	#transformer.set_raw_scale('data', 255)
	
	# reshape blob.
	#test_net.blobs['data'].reshape (1,3,112,112)	# (batch, channel, width, height)


	## Initialize batch and forward.	
	# Init batch
	lmdb_env = lmdb.open(lmdb_path)
	lmdb_txn = lmdb_env.begin()
	lmdb_cursor = lmdb_txn.cursor()
	datum = caffe_pb2.Datum()
	
	# Calculate number of images in test set.
	nImage = 0
	while (lmdb_cursor.next()==True):
		nImage = nImage + 1
	
	# reset cursor.
	lmdb_cursor = lmdb_txn.cursor()

	# forward one by one.	batch size should be 1.
	correct = 0
	total = 0
	nIter = 10
	for iter in range(0, nIter):
		# reset cursor.
		lmdb_cursor = lmdb_txn.cursor()
		
		# forward.
		for i in range(0,nImage):
			lmdb_cursor.next()	
			key = lmdb_cursor.key()
			value = lmdb_cursor.value()
			datum.ParseFromString(value)
			label = datum.label
			data = caffe.io.datum_to_array(datum)
			im = data.astype(np.uint8)
			im = np.array(im)

		
			im = crop_input(im, 42, 'random')
			im = transformer.preprocess('data',im.transpose(1,2,0))
			#__Debug_lmdb(im)

			test_net.blobs['data'].data[...] = im
		
			output = test_net.forward()
			predict = np.argmax(output['prob'], axis = 1)

			total = total + 1
			if int(predict) == int(label):
				correct = correct+1
		
		
			accu = float(correct)/float(total)*100
			print "[%d processed..] predict: %d, label: %d,			--Current accuracy : %2.4f" % (total, predict, label, accu)
		

	accuracy = float(correct)/float(total)*100
	print "######################################################################"
	print "[Finished]	Final accuracy  : %2.4f" % accuracy










