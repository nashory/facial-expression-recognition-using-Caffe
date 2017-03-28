#!/usr/local/bin/python
# - *- coding: utf- 8 - *-

# ------------------------------------------
# Coded by M.C.SHIN
# Last modified : 2016.09.30
#
#
#-------------------------------------------

import time
import random
import numpy as np
import os
import scipy.misc
from google.protobuf import text_format

os.environ['GLOG_minloglevel'] = '2'
import caffe
import lmdb
import PIL.Image
import matplotlib.pyplot as plt
from caffe.proto import caffe_pb2


def SetUp(mode, dev_no=0):
	if mode=='gpu':
		caffe.set_device(dev_no)
		caffe.set_mode_gpu()
		print 'GPU Mode ON.'
	elif mode=='cpu':
		caffe.set_mode_cpu()
		print 'CPU Mode ON.'


def find_layer_by_name(model, layer_name):
	k = 0
	while model.layer[k].name != layer_name:
		k += 1
		if (k > len(model.layer)):
			raise IOError('layer with name %s not found' % layer_name)
	return k

def random_offset(image, size, nPatch):
	channel, height, width = image.shape
	rest_w = width/nPatch-size
	rest_h = height-size
	#print 'full width : %d, rest_w: %d' % (width, rest_w)
	
	offset_w = random.randrange(0,rest_w)
	offset_h = random.randrange(0,rest_h)
	return offset_w, offset_h

def crop_by_offset(image, offset_w, offset_h, size):
	crop_img = []
	crop_img = image[:,offset_h:offset_h+size, offset_w:offset_w+size]
	return crop_img

def crop_input(image, size, opt):
	
	crop_img = []
	channel, width, height = image.shape
	rest_w = width-size
	rest_h = height-size
	#print '-----------------------------'	
	#print image.shape 
	if opt=='random':
		if rest_w==0:		offset_w = 0
		else: 			offset_w = random.randrange(0,rest_w)
		if rest_h==0:		offset_h = 0		
		else: 			offset_h = random.randrange(0,rest_h)
		#print '(%d,%d,%d) rest_w : %d    rest_h : %d' % (channel, width, height, rest_w, rest_h)
		#print 'offset_w : %d   offset_h : %d' % (offset_w, offset_h)
		crop_img = image[:,offset_w:offset_w+size, offset_h:offset_h+size]
	#print crop_img.shape
	elif opt=='center':
		offset_w = int(rest_w/2)
		offset_h = int(rest_h/2)
		crop_img = image[:,offset_w:offset_w+size, offset_h:offset_h+size]
	return crop_img


def Read_lmdb(lmdb_path, opt, mode='RGB'):					# lmdb_path, trina/val, RGB
	if opt=='train':
		lmdb_file = lmdb_path+'train_lmdb/'
	elif opt=='val':
		lmdb_file = lmdb_path+'val_lmdb/'
	lmdb_env = lmdb.open(lmdb_file)
	lmdb_txn = lmdb_env.begin()
	lmdb_cursor = lmdb_txn.cursor()
	datum = caffe_pb2.Datum()

	images = []
	labels = []
	for key, value in lmdb_cursor:
		datum.ParseFromString(value)

		label = datum.label
		data = caffe.io.datum_to_array(datum)
		im = data.astype(np.uint8)
		im = np.array(im)
		
		images.append(im)					# add image to array
		labels.append(label)				# add label to array

	return {'images':images, 'labels':labels}



def __Debug_lmdb(image):
	image = np.transpose(image, (1,2,0))			# original (dim, col, row)
	plt.imshow(image)
	plt.show()
	

def Get_network(caffe_model, deploy_file):
	return caffe.Net(deploy_file, caffe_model, caffe.TEST)

def Get_transformer(deploy_file, mean_file=None):
	network = caffe_pb2.NetParameter()
	with open(deploy_file) as infile:
		#print infile.read()
		text_format.Merge(infile.read(), network)


	dims = network.input_dim	
	t = caffe.io.Transformer(
			inputs = {'data':dims}
			)
	t.set_transpose('data', (2,0,1))			# transpose to (channel, height, width)

	# color_images
	if dims[1] == 3:								# dims[channel][height][weight]
		# channel swap
		t.set_channel_swap('data', (2,1,0))		# 'RGB' --> 'BGR'
	# set mean pixel
	if mean_file:
		with open(mean_file) as infile:
			blob = caffe_pb2.BlobProto()
			blob.MergeFromString(infile.read())
			if blob.HasField('shape'):
				blob_dims = blob.shape
				assert len(blob_dims) == 4, 'Shape should have 4 dimensions - shape is "%s"' % blob.shape
			elif blob.HasField('num') and blob.HasField('channels') and \
					blob.HasField('height') and blob.HasField('width'):
				blob_dims = (blob.num, blob.channels, blob.height, blob.width)
			else:
				raise ValueError('blob does not provide shape or 4d dimensions')
			pixel = np.reshape(blob.data, blob_dims[1:]).mean(1).mean(1)
			t.set_mean('data', pixel)

	return t


def forward_all(images, net, transformer, batch_size=1):					# this function has lots of bugs.   use forward_from_to() function
	caffe_images = []
	for image in images:
		if image.ndim == 2:
			caffe_images.append(image[:,:,np.newaxis])
		else:
			caffe_images.append(image)
	
	caffe_images = np.array(caffe_images)
	dims = transformer.inputs['data'][1:]

	scores = None
	for chunk in [caffe_images[x:x+batch_size] for x in xrange(0, len(caffe_images), batch_size)]:
		new_shape = (len(chunk),) + tuple(dims)
		if net.blobs['data'].data.shape != new_shape:
			net.blobs['data'].reshape(*new_shape)
		
		for index, image in enumerate(chunk):
			image_data = transformer.preprocess('data', image)
			net.blobs['data'].data[index] = image_data

			output = net.forward()['prob']
			print output
			if scores is None:
				scores = output
				scores = np.vstack((scores, output))
			else:
				scores = np.vstack((scores, output))
			print 'Processed %s/%s images ...%d' % (len(scores), len(caffe_images),x)
		
	for idx in range(0,batch_size):
		print idx
		scores = np.delete(scores, (0), axis=0)					# delete duplicated row  (it seems bug.)
	return scores

def forward_from_to(images, net, transformer, start_layer, end_layer, batch_size=3):		# feature extraction
	caffe_images = []
	for image in images:
		image = crop_input(image, 224, 'random')
		if image.ndim == 2:
			caffe_images.append(image[:,:,np.newaxis])
		else:
			caffe_images.append(image)
	
	caffe_images = np.array(caffe_images)
	dims = transformer.inputs['data'][1:]

	scores = None
	for x in xrange(0,len(caffe_images), batch_size):
		for chunk in [caffe_images[x:x+batch_size]]:
			new_shape = (len(chunk),) + tuple(dims)
			if net.blobs['data'].data.shape != new_shape:
				net.blobs['data'].reshape(*new_shape)
			for index, image in enumerate(chunk):
				image_data = transformer.preprocess('data', image)
				net.blobs['data'].data[index] = image_data

			output = net.forward(None,start_layer,end_layer)[end_layer]
			
			if scores is None:
				scores = output
				scores = np.vstack((scores, output))
			else:
				scores = np.vstack((scores, output))
			print 'Processed %s/%s images ...' % (len(scores)-batch_size, len(caffe_images))

	for idx in range(0,batch_size):
		scores = np.delete(scores, (0), axis=0)					# delete duplicated row  (it seems bug.)
	return scores
	

def classify(caffe_model, deploy_file, images, labels, mean_file=None):
	net = Get_network(caffe_model, deploy_file)		# set network structure and weights.
	transformer = Get_transformer(deploy_file)

	_, channels, height, width = transformer.inputs['data']

    # Classify the image
	classify_start_time = time.time()
	scores = forward_all(images, net, transformer)
	print 'Classification took %s seconds.' % (time.time() - classify_start_time,)

    ### Process the results

	indices = (-scores).argsort()[:, :5] # take top 5 results
	classifications = []
	for image_index, index_list in enumerate(indices):
		result = []
		for i in index_list:
            # 'i' is a category in labels and also an index into scores
			#if labels is None:
			#	label = 'Class #%s' % i
			#else:
			#	label = labels[i]
			label = 'TCL'
			result.append((label, round(100.0*scores[image_index, i],4)))
		classifications.append(result)

	for index, classification in enumerate(classifications):
		#print '{:-^80}'.format(' Prediction for %s ' % image_files[index])
		for label, confidence in classification:
			print '{:9.4%} - "{}"'.format(confidence/100.0, label)
		print


#-------------------------------- ONLY FOR SPECIAL USE ---------------------------------#

def forward_from_to_concat(images, net, transformer, start_layer, end_layer, batch_size=1):		# input is concat image.	batch_size must be 1.
	caffe_images = []
	for image in images:
		if image.ndim == 2:
			caffe_images.append(image[:,:,np.newaxis])
		else:
			caffe_images.append(image)
	
	caffe_images = np.array(caffe_images)
	dims = transformer.inputs['data'][1:]

	scores = None
	output = []
	for x in xrange(0,len(caffe_images), batch_size):
		for chunk in [caffe_images[x:x+batch_size]]:
			new_shape = (len(chunk),) + tuple(dims)
			
			for index, image in enumerate(chunk):
				image_data = transformer.preprocess('data', image)
				nImg, img_shape, slice_img = slice_image(image_data)

				# reshape 'data' blob dimension
				my_shape = (nImg,) + img_shape
				net.blobs['data'].reshape(*my_shape)
				
				# save each patch into data blob.
				for j in range(0,nImg):
					net.blobs['data'].data[j] = slice_img[j]
				
				# forward data.
				output = net.forward(None,start_layer,end_layer)[end_layer]
				output = MaxPooling(output)				# max-pooling features.   img-level ==> video-level feature
			
			if scores is None:
				scores = output
				scores = np.vstack((scores, output))
			else:
				scores = np.vstack((scores, output))
			print scores
			print 'Processed %s/%s images ...' % (len(scores)-batch_size, len(caffe_images))

	for idx in range(0,batch_size):
		scores = np.delete(scores, (0), axis=0)					# delete duplicated row  (it seems bug.)

	return scores

def slice_image(concat_img, nPatch):
	channel, width, height = concat_img.shape
	size = min([width, height])
	x_width = max([width, height])

	print concat_img.shape
	if not ((x_width)%nPatch==0):
		print '[Error] input image dimension is wrong!'
		return
	
	n_side = x_width/nPatch
	image_list = []
	#n=5	
	for i in range(0,nPatch):
		concat = concat_img[:,:,(i*n_side):((i+1)*n_side)]		## image[channel][height][width]
		#concat = concat_img
		image_list.append(concat)
	image_list = np.array(image_list)
	
	return nPatch, image_list

def MaxPooling(array):
	n_array, n_features = array.shape			# n_array : # of feature array // n_features : # of elements in a feature array.
	
	max_pool = []
	test=None
	for index in range(0, n_features):
		element = []
		for k in range(0, n_array):
			element.append(array[k][index])
		max_pool.append(max(element))
	
	return max_pool

def GetResizedConcatImage(image, size, nPatch):
	channel, width, height = image.shape
	nImg, slice_img = slice_image(image, nPatch)
	offset_w, offset_h = random_offset(image,224,nPatch)
	resized_img = np.zeros((channel, size, size*nImg))
	
	for j in range(0,nImg):
		resized_img[:, :, (j)*size:(j+1)*size] = crop_by_offset(slice_img[j],offset_w, offset_h,size)

	img_shape = (channel, size, size)
	return resized_img, img_shape
		



def Train_With_Pretrained_Network(images, net, transformer, start_layer, end_layer, target_net, solver, nPatch=20, batch_size=1):		# input is concat image.	batch_size must be 1.
	caffe_images = []
	cnt = 0
	for image in images:
		cnt = cnt+1
		image, img_shape = GetResizedConcatImage(image, 224, nPatch)
		print '[%d]		Resizing image for network input....' % cnt

		if image.ndim == 2:
			caffe_images.append(image[:,:,np.newaxis])
		else:
			caffe_images.append(image)

	
	caffe_images = np.array(caffe_images)
	dims = transformer.inputs['data'][1:]

	scores = None
	output = []
	for x in xrange(0,len(caffe_images), batch_size):
		for chunk in [caffe_images[x:x+batch_size]]:
			new_shape = (len(chunk),) + tuple(dims)
			
			for index, image in enumerate(chunk):
				nImg, slice_img = slice_image(image, nPatch)

				# reshape 'data' blob dimension
				my_shape = (nImg,) + img_shape
				net.blobs['data'].reshape(*my_shape)
				
				# save each patch into data blob.
				for j in range(0,nImg):
					image_data = transformer.preprocess('data', slice_img[j])
					net.blobs['data'].data[j] = image_data
				
				# forward data.
				output = net.forward(None,start_layer,end_layer)[end_layer]
				output = MaxPooling(output)				# max-pooling features.   img-level ==> video-level feature
				print output




def CopyPretrainedWeights(pretrain_net, target_net, lfrom, lto):

	nFlag = False
	cnt = 0
	print 'Copying weights and bias from the pretrained network...'
	for layer_name, layer_blob in pretrain_net.params.items():
		if layer_name == lfrom:
			nFlag = True

		if (nFlag):
			cnt = cnt+1
			target_net.params[layer_name][0].data[...] = layer_blob[0].data[...]	# weights
			target_net.params[layer_name][1].data[...] = layer_blob[1].data[...]	# bias
			print '[%2d] layer name: \'%s\', weight shape: %s, bias shape: %s' % (cnt, layer_name, layer_blob[0].data.shape, layer_blob[1].data.shape)
	
		if layer_name == lto:
			nFlag = False

	print 'Successfully Copied network.'

		






