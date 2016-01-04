import numpy as np
import matplotlib.pyplot as plt

# Make sure that caffe is on the python path:
caffe_root = '/home/xucb/projects/caffe/'   # the installed caffe_root
caffe_install = '/home/xucb/projects/caffe/build/install/'
import sys
sys.path.insert(0, caffe_install + 'python')

import caffe

# Set the right path to your model definition file, pretrained model weights,
# and the image you would like to classify.
MODEL_FILE = caffe_root+'models/bvlc_reference_caffenet/deploy.prototxt'
PRETRAINED = caffe_root+'models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel'
IMAGE_FILE = caffe_root+'examples/images/cat.jpg'

caffe.set_mode_cpu()
net = caffe.Classifier(MODEL_FILE, PRETRAINED,
                       mean=np.load(caffe_install + 'python/caffe/imagenet/ilsvrc_2012_mean.npy').mean(1).mean(1),
                       channel_swap=(2,1,0),
                       raw_scale=255,
                       image_dims=(256, 256))
input_image = caffe.io.load_image(IMAGE_FILE)
plt.imshow(input_image)

prediction = net.predict([input_image])  # predict takes any number of images, and formats them for the Caffe net automatically
print prediction

print 'prediction shape:', prediction.shape
cls = prediction[0].argmax()
print 'predicted class:',cls, "confidence:",prediction[0][cls]
plt.show()

