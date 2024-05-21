# FastUGI-Net and UGIAD Dataset
This repository provides the codes of FastUGI-Net and the UGIAD dataset.

## Dataset
The UGIAD dataset provides open access to 3425 UGI endoscopic images from Macao Kiang Wu Hospital and Xiangyang Centre Hospital, mainly captured using WLE and partly by NBI. These images encompass three key areas: esophagus, stomach, and duodenum, each annotated with specific anatomical landmarks and disease types, and these annotations are both applied and subsequently verified by medical specialists from the two contributing hospitals. The dataset is developed ensuring patient anonymity and privacy, with all materials fully anonymized by excluding patient information from the images and renaming the files according to their anatomical landmark and disease labels, and thereby exempting it from patient consent requirements. The images consist of different resolutions that range between 268x217 and 1545x1156 with most of the black borders removed. 
The dataset can also be downloaded using the following links: <br />
Google Drive: https://drive.google.com/file/d/1ZTC7dyO84uOFG0qsiJrp-BSatsQ2KEo7/view?usp=drive_link <br />
Baidu Cloud: https://pan.baidu.com/s/18qJIDrRZy9Yx_nYKuZ8b8w (key: tcfg)

## Get Started
### Pretrained weights
You can download the pretrained weights of the median model of each model size of FastUGI-Net via the below links.
| Model size  | Anatomical landmark accuracy | Disease accuracy | Link |
| ------------- | ------------- | ------------- | ------------- |
| B0+XXS  | 91.70% | 91.42% | https://drive.google.com/file/d/1XNWLUYP271csG0Jh4xtU-A9zpWWBAOCw/view?usp=drive_link |
| B3+XXS  | 92.27% | 92.99% |  [Link](https://pages.github.com/)  |
| B5+XXS  | 92.27% | 93.71% | https://drive.google.com/file/d/1e1fDCTi5CqHWgOOTEJdVqnWZ-Wr4AfSz/view?usp=drive_link   |
| B7+XXS  | 92.70% | 94.13% | https://drive.google.com/file/d/19B2TpIttZ08_bQXm4mtxuW7qA0OYGT3T/view?usp=drive_link)
