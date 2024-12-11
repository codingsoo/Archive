import os
import json
import matplotlib.pyplot as plt
import numpy as np



def files_in_dir(target):
    arr = []
    files = os.listdir(target)
    for item in files:
        arr.append(os.path.join(target, item))

    return arr


if __name__ == '__main__':
    dir_name = 'C:\\Users\\myeongsoo\\Downloads\\hackathon_data_3000\\REAL(1500)\\REAL_SENTENCE_keypoints'

    target = files_in_dir(dir_name)

    for t_dir in target:
        f_file = files_in_dir(t_dir)[0]


        with open(f_file, 'r') as f:
            try:
                p_data = json.loads(f.read())['people']
                p_keys = p_data.keys()

                for key in p_keys:
                    if key != 'person_id':
                        if '2d' in key:
                            mat_length = len(p_data[key])
                            reform = []
                            for i in range(mat_length):
                                if i % 3 != 2:
                                    reform.append(p_data[key][i])
                            print(key)
                            reform = np.array(reform).reshape(int(len(reform)/2), 2)
                            print(len(reform))
                            # plt.imshow(reform)
                            # plt.show()

                        else:
                            mat_length = len(p_data[key])
                            reform = []
                            for i in range(mat_length):
                                if i % 4 != 3:
                                    reform.append(p_data[key][i])
                            print(key)
                            reform = np.array(reform).reshape(int(len(reform) / 3), 3)
                            print(len(reform))
                            # plt.imshow(reform)
                            # plt.show()
            except:
                pass