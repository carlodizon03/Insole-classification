import pandas as pd
import numpy as np
from collections import OrderedDict

# lf_front =  pd.read_csv("data/raw/data_left100/Lf_100.csv")
# lf_left = pd.read_csv("data/raw/data_left100/Ll_100.csv")
# lf_frontLeft = pd.read_csv("data/raw/data_left100/Lfl_100.csv")
# lf_bottomLeft = pd.read_csv("data/raw/data_left100/Lbl_100.csv")
# lf_bottom =  pd.read_csv("data/raw/data_left100/Lb_100.csv")
valid_data_lf_frontLeft = pd.read_csv("python_model_training/data/raw/data_left100/data_2.csv")
valid_data_lf_left = pd.read_csv("python_model_training/data/raw/data_left100/data_2.csv")

lf_valid_front = pd.read_csv("python_model_training\data/raw\data_left20\Lf_20.csv")
lf_valid_left = pd.read_csv("python_model_training\data/raw\data_left20\Ll_20.csv")
lf_valid_frontLeft = pd.read_csv("python_model_training\data/raw\data_left20\Lfl_20.csv")
lf_valid_bottomLeft = pd.read_csv("python_model_training\data/raw\data_left20\Lbl_20.csv")
lf_valid_bottom = pd.read_csv("python_model_training\data/raw\data_left20\Lb_20.csv")


rf_front = pd.read_csv("python_model_training/data/raw/data_right100/Rf_100.csv")
rf_frontRight = pd.read_csv("python_model_training/data/raw/data_right100/Rfr_100.csv")
rf_right = pd.read_csv("python_model_training/data/raw/data_right100/Rr_100.csv")
rf_bottomRight = pd.read_csv("python_model_training/data/raw/data_right100/Rbr_100.csv")
rf_bottom = pd.read_csv("python_model_training/data/raw/data_right100/Rb_100.csv")

df_data = lf_valid_bottom
df_save_path = 'python_model_training\data/npy\Left_Foot_Valid/lf_valid_bottom.npy'

data_idx = 0
zero_count = 0
data_count = 0 
sample_count_list = []
sample_count = 0
for idx,row in df_data.iterrows():
    row_data = np.nan_to_num([row['x'], row['y'], row['z'], row['s1'], row['s2'], row['s3'], row['s4']], nan = 0)
    is_all_zeros = not np.any(row_data)
    if(is_all_zeros == True):
        data_count+=1
        zero_count+=1
        if(zero_count == 2):
            zero_count = 0
            is_all_zeros = False
            sample_count_list.append(sample_count)
            sample_count = 0
            continue
    else:
        sample_count+=1
print(max(sample_count_list))
N,H,W = int(data_count/2),max(sample_count_list),7
print(N,H,W)
data = np.empty((N,H,W))
temp_buffer = []
data_idx = 0
zero_count = 0
data_count = 0 
for idx, row in df_data.iterrows():
    row_data = np.nan_to_num([row['x'], row['y'], row['z'], row['s1'], row['s2'], row['s3'], row['s4']], nan = 0)
    is_all_zeros = not np.any(row_data)
    if(is_all_zeros == True):
        zero_count+=1
        if(zero_count == 2):
            data[data_idx,:len(temp_buffer),:W] = temp_buffer
            temp_buffer =[]
            data_idx+=1
            is_all_zeros = False
            zero_count = 0
            continue         
    else:
        temp_buffer.append(row_data)

with open(df_save_path,'wb') as f:
    np.save(f,data)
with open(df_save_path, 'rb') as f:
    data_ = np.load(f)
for idx, sample in enumerate(data_):
    print(sample)

print(data_.shape)