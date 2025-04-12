# FastUGI-Net and UGIAD Dataset
This repository provides the official codes of FastUGI-Net and the UGIAD dataset.

## Dataset Details
The UGIAD dataset provides open access to 3425 UGI endoscopic images from Macao Kiang Wu Hospital and Xiangyang Centre Hospital, mainly captured using WLE and partly by NBI. These images encompass three key areas: esophagus, stomach, and duodenum, each annotated with specific anatomical landmarks and disease types, and these annotations are both applied and subsequently verified by medical specialists from the two contributing hospitals. The dataset is developed ensuring patient anonymity and privacy, with all materials fully anonymized by excluding patient information from the images and renaming the files according to their anatomical landmark and disease labels, and thereby exempting it from patient consent requirements. The images consist of different resolutions that range between 268x217 and 1545x1156 with most of the black borders removed. 
The dataset can also be downloaded using the following links: <br />
Google Drive: https://drive.google.com/file/d/1mrJiWXsGEDMog2uoM5EmBtjEtYbx8t2F/view?usp=drive_link <br />
Baidu Cloud: https://pan.baidu.com/s/1YFtl532uoCYwZcXd01r9_Q (key: n2z6)

The dataset is divided into 9 anatomical landmark classes and 10 disease classes (9 diseases or normal) based on the following annotations:

### Anatomical landmark annotation
Our anatomical annotation approach is guided by previous photodocumentation guidelines such as the British and Japanese guidelines. The images are categorised into 9 landmarks. Anatomical landmarks identified in the antegrade view within the UGIAD dataset encompass the esophagus (E), squamocolumnar junction (SJ), gastric body in antegrade view (Ba), antrum (Ant), duodenal bulb (DB) and descending part of the duodenum (DD). Conversely, the retroflex view encompasses landmarks such as the fundus (F), gastric body in retroflex view (Br) and angulus (Ang).

<p align="center">
    <img src="/assets/anatomical_annotation.png" alt="Anatomical landmark annotation of the UGIAD Dataset" width="350">
</p>

### Disease annotation
For disease annotation, the images in the dataset are classified into normal findings or 9 upper gastrointestinal (UGI) diseases including esophageal neoplasm, esophageal varices, gastroesophageal reflux disease (GERD), gastric neoplasm, gastric polyp, gastric ulcer, gastric varices, duodenal bulb diseases and diseases of the descending part of the duodenum.
<p align="center">
    <img src="/assets/disease_example.png" alt="Representative images of UGIAD Dataset" width="1200">
</p>

The following table displays the data distribution of the UGIAD dataset.
| Anatomical landmark / Disease    | Normal | Esophageal neoplasm | Esophageal varices | GERD | Gastric neoplasm | Gastric polyp | Gastric ulcer | Gastric varices | Diseases of duodenal bulb | Diseases of descending part of duodenum | Total |
|----------------------------------|--------|---------------------|--------------------|------|------------------|---------------|---------------|-----------------|---------------------------|-----------------------------------------|-------|
| Esophagus                        | 98     | 222                 | 133                | 24   | 0                | 0             | 0             | 0               | 0                         | 0                                       | 477   |
| Squamocolumnar junction          | 96     | 35                  | 95                 | 119  | 0                | 0             | 0             | 0               | 0                         | 0                                       | 345   |
| Fundus                           | 97     | 0                   | 0                  | 0    | 49               | 76            | 49            | 84              | 0                         | 0                                       | 355   |
| Gastric body (antegrade)         | 166    | 0                   | 0                  | 0    | 178              | 293           | 61            | 0               | 0                         | 0                                       | 698   |
| Gastric body (retroflex)         | 65     | 0                   | 0                  | 0    | 112              | 48            | 11            | 0               | 0                         | 0                                       | 236   |
| Angulus                          | 87     | 0                   | 0                  | 0    | 80               | 57            | 82            | 0               | 0                         | 0                                       | 306   |
| Antrum                           | 95     | 0                   | 0                  | 0    | 67               | 56            | 163           | 0               | 0                         | 0                                       | 381   |
| Duodenal bulb                    | 156    | 0                   | 0                  | 0    | 0                | 0             | 0             | 0               | 202                       | 0                                       | 358   |
| Descending part of duodenum      | 154    | 0                   | 0                  | 0    | 0                | 0             | 0             | 0               | 0                         | 115                                     | 269   |
| Total                            | 1014   | 257                 | 228                | 143  | 486              | 530           | 366           | 84              | 202                       | 115                                     | 3425  |

## Pretrained weights
You can download the pretrained weights of the median model of each model size of FastUGI-Net via the below links.
| Model size  | Anatomical landmark accuracy | Disease accuracy | Consistency accuracy |Link |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| B0+XXS  | 91.70% | 91.42% | 98.57% | [Link](https://drive.google.com/file/d/1XNWLUYP271csG0Jh4xtU-A9zpWWBAOCw/view?usp=sharing) |
| B3+XXS  | 92.27% | 92.99% | 98.57% | [Link](https://drive.google.com/file/d/1CsB7vsVg640pjXZ95Pl1MATa9Ktzu2Ah/view?usp=sharing)  |
| B5+XXS  | 92.27% | 93.71% | 98.36% | [Link](https://drive.google.com/file/d/1e1fDCTi5CqHWgOOTEJdVqnWZ-Wr4AfSz/view?usp=sharing)   |
| B7+XXS  | 92.70% | 94.13% | 98.16% | [Link](https://drive.google.com/file/d/19B2TpIttZ08_bQXm4mtxuW7qA0OYGT3T/view?usp=sharing) |

## Citation
If you use FastUGI-Net or the UGIAD dataset in your research, please cite our paper:
```
@article{FastUGI-Net,
    title={FastUGI-Net: Enhanced Real-Time Endoscopic Diagnosis with Efficient Multi-Task Learning},
    author={In Neng Chan and Pak Kin Wong and Tao Yan and Yanyan Hu and Chon In Chan and Peixuan Ge and Zheng Li and Ying Hu and Shan Gao and Hon Ho Yu},
    journal={Expert Systems with Applications},
    DOI = {10.1016/j.eswa.2025.127444},
    note = {(Published online)}
    year={2025}
}
```
