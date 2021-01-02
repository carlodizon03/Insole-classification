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
        self.test_data = OrderedDict()
        self.test_data[self.labels[2]] = np.load(os.path.join("python_model_training/data/npy/Left_Foot_Valid", "valid_data_lf_left.npy"))
        self.test_data[self.labels[1]] = np.load( os.path.join("python_model_training/data/npy/Left_Foot_Valid", "valid_data_lf_frontLeft.npy"))

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
        train_data = np.array(all_data[:400,:,:])
        train_labels = np.array(all_labels[:400])
        val_data = np.array(all_data[400:,:,:])
        val_labels = np.array(all_labels[400:])
        
        test_label_idx = [2,1]
        N, H, W = self.num_samples_per_direction*len(test_label_idx), self.sample_size, 7
        all_test_data = np.empty((N,H,W))
        all_test_labels = []
        N_ = 0
        for i in range(N):
            random.shuffle(test_label_idx)
            for idx, label in enumerate(test_label_idx):
                all_test_data[N_,:H,:] = tf.keras.utils.normalize(self.test_data[self.labels[label]][i,:H,:W])
                all_test_labels.append(label)
                N_+=1
            if N_ == N: break
        test_data = np.array(all_test_data)
        test_labels = np.array(all_test_labels)

        return train_data, train_labels, val_data, val_labels, test_data, test_labels


# lf_loader = Loader()
# train_data, train_labels, val_data, val_labels, test_data, test_labels = lf_loader.load()
# print(train_data.shape, train_labels.shape, val_data.shape, val_labels.shape, test_data.shape, test_labels.shape)