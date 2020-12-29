import numpy as np
import random
import os
from collections import OrderedDict
import tensorflow as tf

class Loader():
    def __init__(self, dataset = "Left_Foot", num_samples_per_direction = 100, sample_size = 350, shuffle = True ):
        self.dataset = dataset
        self.dataset_path = os.path.join("python_model_training/data/npy/",self.dataset)
        self.sample_size = sample_size
        self.num_samples_per_direction = num_samples_per_direction
        self.shuffle = shuffle
        if dataset == "Left_Foot": self.labels = ['lf_front','lf_frontLeft','lf_left','lf_bottomLeft','lf_bottom']
        elif dataset == "Right_Foot": self.labels = ['rf_front','rf_frontLeft','rf_left','rf_bottomLeft','rf_bottom']
        self.data = OrderedDict()
        self.data[self.labels[0]] = np.load(os.path.join(self.dataset_path,self.labels[0]+'.npy')) 
        self.data[self.labels[1]] = np.load(os.path.join(self.dataset_path,self.labels[1]+'.npy')) 
        self.data[self.labels[2]] = np.load(os.path.join(self.dataset_path,self.labels[2]+'.npy')) 
        self.data[self.labels[3]] = np.load(os.path.join(self.dataset_path,self.labels[3]+'.npy')) 
        self.data[self.labels[4]] = np.load(os.path.join(self.dataset_path,self.labels[4]+'.npy')) 

    def load(self):
        label_idx = [0,1,2,3,4]
        N, H, W = self.num_samples_per_direction*len(label_idx), self.sample_size, 7
        all_data = np.empty((N,H,W))
        all_labels = []
        N_ = 0
        for i in range(N):
            random.shuffle(label_idx)
            for idx, label in enumerate(label_idx):
                all_data[N_,:H,:] = tf.keras.utils.normalize(self.data[self.labels[label]][i,:H,:W])
                all_labels.append(label)
                N_+=1
            if N_ == N: break
        train_data = np.array(all_data[:300,:,:])
        train_labels = np.array(all_labels[:300])
        test_data = np.array(all_data[300:,:,:])
        test_labels = np.array(all_labels[300:])
        return train_data,train_labels,test_data,test_labels


# lf_loader = Loader()
# lf_loader.load()
