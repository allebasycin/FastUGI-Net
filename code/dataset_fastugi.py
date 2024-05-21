import os.path
import numpy as np
import torch
import csv
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
from PIL import Image
from tqdm import tqdm
import torchvision.transforms.functional as f

interp = transforms.InterpolationMode.BICUBIC

def normalize(image, mean, std):
    normalize_function = transforms.Normalize(mean, std)
    return normalize_function(image)

def resize(image, h_size, w_size):
    resize_function = transforms.Resize([h_size, w_size],
                            interpolation=interp,
                            antialias=True)
    return resize_function(image)

to_Tensor = transforms.Compose([
    transforms.ToTensor(),
    transforms.ConvertImageDtype(torch.float32),
])

anatomical_classes = {
    'esophagus': {'label': 0},
    'squamocolumnar_junction': {'label': 1},
    'fundus': {'label': 2},
    'body_antegrade': {'label': 3},
    'body_retroflex': {'label': 4},
    'angulus': {'label': 5},
    'antrum': {'label': 6},
    'duodenal_bulb': {'label': 7},
    'descending_part_of_duodenum': {'label': 8}
}

disease_classes = {
    'normal': {'label': 0},
    'esophageal_neoplasm': {'label': 1},
    'esophageal_varices': {'label': 2},
    'gatroesophageal_reflux_disease': {'label': 3},
    'gastric_neoplasm': {'label': 4},
    'gastric_polyp': {'label': 5},
    'gastric_ulcer': {'label': 6},
    'gastric_varices': {'label': 7},
    'duodenal_diseases(bulb)': {'label': 8},
    'duodenal_diseases(descending)': {'label': 9}
}
disease_class_num = len(disease_classes)
anatomical_class_num = len(anatomical_classes)

class EndoDataset(Dataset):
    def __init__(self,
                 raw_path,
                 split_path,
                 task,
                 w_size,
                 h_size,
                 transform=None,
                 mean=0,
                 std=0
                 ):

        self.data = []
        self.anatomical_label = []
        self.disease_label = []
        self.transform = transform
        self.task = task
        self.mean = mean
        self.std = std
        self.h_size = h_size
        self.w_size = w_size
        for d_cl in disease_classes.keys():
            for a_cl in anatomical_classes.keys():
                split_file = split_path + d_cl+ '/' + str(a_cl) + '/' + task + '.csv'
                split_file_trueorfalse = os.path.isfile(split_file)
                if split_file_trueorfalse == False:
                    pass
                else:
                    with open(split_file, newline='') as split:
                        reader = csv.reader(split)
                        for file in reader:
                            file = file[0]
                            img = Image.open(raw_path  + d_cl+ '/' + str(a_cl) + '/' + file)
                            img = img.convert("RGB")
                            img = resize(to_Tensor(img), h_size=self.h_size, w_size=self.w_size)
                            img = normalize(img, self.mean, self.std)
                            self.data.append(img)
                            self.anatomical_label.append(anatomical_classes[a_cl]['label'])
                            a = disease_classes[d_cl]['label']
                            self.disease_label.append(a)


    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        img = self.data[idx]
        anatomical_label = self.anatomical_label[idx]
        disease_label = self.disease_label[idx]

        return img, anatomical_label, disease_label

class image_batch:
    def __init__(self, data):
        transposed_data = list(zip(*data))
        self.img = torch.stack(transposed_data[0], 0)
        self.anatomical_label = torch.tensor(transposed_data[1], dtype=torch.int64)
        self.disease_label = torch.tensor(transposed_data[2], dtype=torch.int64)
        self.size = self.img.size(0)

    # custom memory pinning method on custom type
    def pin_memory(self):
        self.img = self.img.pin_memory()
        return self

    def export_images(self, index, path):
        return NotImplementedError


def image_batch_wrapper(batch):
    return image_batch(batch)