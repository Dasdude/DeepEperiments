
from keras.layers import Input,Flatten,Dense,Dropout,Activation,AveragePooling2D,MaxPooling2D
from keras.optimizers import SGD
from Layers.gate_layer import gate_layer,gated_layers_sequence
from keras.engine import Model
import numpy as np
from keras.utils.visualize_util import plot

def gated_net_functional_model(opts,nb_filter = 4,filter_size=3,depth =5 , input_shape=(3,224,224),
                               input_tensor=None,
                                include_top=True,initialization = 'glorot_normal'):
	if include_top:
		input_shape=(3,224,224)
	else:
		input_shape=(3,None,None)
	if input_tensor==None:
		img_input = Input(shape=input_shape, name='image_batch')
	else:
		img_input = input_tensor

	# out2 = gated_layers_sequence(input_tensor=img_input,total_layers=depth,nb_filter=nb_filter,filter_size=filter_size,
	#                              input_shape=input_shape)
	x = gate_layer(img_input, 32, 5, input_shape=input_shape,opts=opts)
	x = MaxPooling2D(pool_size=(2, 2))(x)
	x = Activation('sigmoid')(x)
	x = gate_layer(x, 32, 5,input_shape=(32,112,112),opts=opts)
	x = AveragePooling2D(pool_size=(2, 2))(x)
	x = Activation('sigmoid')(x)
	x = gate_layer(x, 64, 5,input_shape=(32,56,56),opts=opts)
	x = AveragePooling2D(pool_size=(2, 2))(x)
	x = Activation('sigmoid')(x)
	x = gate_layer(x, 64, 5,input_shape=(64,28,28),opts=opts)
	x = Activation('sigmoid')(x)
	x = gate_layer(x, 64, 5,input_shape=(64,28,28),opts=opts)
	if not include_top:
		model = Model(input=img_input,output=x)
	else:
		x = Flatten(name='flatten')(x)
		x = Dense(1024,activation='relu',init=initialization)(x)
		x = Dropout(p=.5)(x)
		x = Dense(512,activation='relu',init=initialization)(x)
		x = Dropout(p=.5)(x)
		x = Dense(20,activation='softmax',name='prediction',init=initialization)(x)
		model = Model(input=img_input,output=x)
		model.summary()
	return model
if __name__ == '__main__':
    model = gated_net_functional_model(include_top=True)
    model.summary()
    plot(model, to_file='model.png')
    sgd = SGD(lr=0.01, momentum=.9, decay=5 * 1e-4, nesterov=True)
    model.compile(optimizer=sgd,loss = 'mse')
    np.random.seed(0)
    input_im = np.random.randint(0,256,(1,3,4,4))
    print "input data: \n",input_im
    a = model.predict(input_im)
    print "Predictions"
    print a
    print a.shape

