import torch
from sklearn.metrics import classification_report, confusion_matrix
from .dataset_fastugi import EndoDataset, image_batch_wrapper
from .fastugi_net import FastUGINet
from torch.utils.data import DataLoader

def test_loop_fn_multlabel(test_loader, model, device):
    y_pred_a = []
    y_true_a = []
    correct_a = 0

    y_pred_d = []
    y_true_d = []
    correct_d = 0
    consistent_count_pred = 0
    non_zero_count_pred = 0

    total_samples = 0
    model.to(device)
    model.eval()
    for (i, data) in enumerate(test_loader):
        image_data = data.img
        anatomical_label_data = data.anatomical_label
        disease_label_data = data.disease_label

        image, anatomical_target, disease_target = image_data.to(device), anatomical_label_data.to(
            device), disease_label_data.to(device)
        with torch.no_grad():
            anatomical_output, disease_output = model(image)
            pred_a = anatomical_output.max(1, keepdim=True)[1]
            correct_a += pred_a.eq(anatomical_target.view_as(pred_a)).sum().item()

            pred_d = disease_output.max(1, keepdim=True)[1]
            correct_d += pred_d.eq(disease_target.view_as(pred_d)).sum().item()

            total_samples += image.size()[0]
            anatomical_output = (torch.max(torch.exp(anatomical_output), 1)[1]).data.cpu().numpy()
            disease_output = (torch.max(torch.exp(disease_output), 1)[1]).data.cpu().numpy()
            output_a = pred_a.data.cpu().numpy()
            output_d = pred_d.data.cpu().numpy()

            y_pred_a.extend(output_a)  # Save Prediction
            y_pred_d.extend(output_d)  # Save Prediction
            anatomical_targets = anatomical_target.data.cpu().numpy()
            disease_targets = disease_target.data.cpu().numpy()
            y_true_a.extend(anatomical_targets)  # Save Truth
            y_true_d.extend(disease_targets)  # Save Truth

            # Calculate consistency accuracy
            consistency_matrix = torch.tensor([[1, 1, 0, 0, 0, 0, 0, 0, 0],
                                               [1, 1, 0, 0, 0, 0, 0, 0, 0],
                                               [1, 1, 0, 0, 0, 0, 0, 0, 0],
                                               [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                               [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                               [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                               [0, 0, 1, 0, 0, 0, 0, 0, 0],
                                               [0, 0, 0, 0, 0, 0, 0, 1, 0],
                                               [0, 0, 0, 0, 0, 0, 0, 0, 1]]).to(device)

            # Remove images that are predicted as normal images from the disease prediction and anatomical
            # landmark prediction in each batch
            disease_pred_tensor = torch.tensor(disease_output)
            anatomical_pred_tensor = torch.tensor(anatomical_output)
            disease_nonzero_indexes = torch.where(pred_d != 0)
            if len(disease_nonzero_indexes[0]) == 0:
                consistent_count_pred += 0
                non_zero_count_pred += 0
            else:
                anatomical_pred_label_non_zero = anatomical_pred_tensor[disease_nonzero_indexes[0]]
                disease_pred_label_nonzero = disease_pred_tensor[disease_nonzero_indexes[0]]

                non_zero_count_pred += len(disease_pred_label_nonzero)

                # Look up the consistent value from the consistency_matrix
                for i in range(len(disease_pred_label_nonzero)):
                    disease_value = (disease_pred_label_nonzero[i] - 1)
                    anatomical_value = anatomical_pred_label_non_zero[i]
                    consistent_value = consistency_matrix[disease_value][anatomical_value]
                    if consistent_value == 1:
                        consistent_count_pred += 1

    accuracy_a = 100.0 * correct_a / total_samples
    accuracy_d = 100.0 * correct_d / total_samples
    consistent_accuracy = 100.0 * consistent_count_pred / non_zero_count_pred
    print('Anatomical Accuracy={:.4f}%'.format(accuracy_a))
    print('Disease Accuracy={:.4f}%'.format(accuracy_d))
    print('Consistent Accuracy={:.4f}%'.format(consistent_accuracy))

    cf_matrix_a = confusion_matrix(y_true_a, y_pred_a)
    cf_matrix_d = confusion_matrix(y_true_d, y_pred_d)
    report_a = classification_report(y_true_a, y_pred_a, digits=4)
    report_d = classification_report(y_true_d, y_pred_d, digits=4)
    print('Anatomical classification results:')
    print(report_a)
    print(cf_matrix_a)

    print('Disease classification results:')
    print(report_d)
    print(cf_matrix_d)


anatomical_classes = {
    'Esophagus': {'label': 0},
    'Squamocolumnar junction': {'label': 1},
    'Fundus': {'label': 2},
    'Gastric body (antegrade)': {'label': 3},
    'Gastric body (retroflex)': {'label': 4},
    'Angulus': {'label': 5},
    'Antrum': {'label': 6},
    'Duodenal bulb': {'label': 7},
    'Descending part of duodenum': {'label': 8}
}

disease_classes = {
    'Normal': {'label': 0},
    'Esophageal_neoplasm': {'label': 1},
    'Esophageal varices': {'label': 2},
    'Gatroesophageal reflux disease': {'label': 3},
    'Gastric neoplasm': {'label': 4},
    'Gastric polyp': {'label': 5},
    'Gastric ulcer': {'label': 6},
    'Gastric varices': {'label': 7},
    'Duodenal diseases(bulb)': {'label': 8},
    'Duodenal diseases(descending)': {'label': 9}
}

anatomical_classname = []
for item in anatomical_classes.keys():
    anatomical_classname.append(item)

disease_classname = []
for item in disease_classes.keys():
    disease_classname.append(item)

anatomical_class_num = len(anatomical_classes)
disease_class_num = len(disease_classes)

h_size = 224
w_size = 224

image_dir = ""
split_dir = ""

pretrained_weight_path = ""

cnn_size = 'b0' #size of EfficientNet
cnn_size = 'xxs' #size of MobileViT

test_dataset = EndoDataset(image_dir, split_dir, 'test', transform=None, mean=[0.5187, 0.2813, 0.2154], std=[0.2786, 0.1975, 0.1759], h_size=h_size, w_size=w_size)
test_loader = DataLoader(test_dataset, batch_size=1, shuffle=True, collate_fn=image_batch_wrapper, pin_memory=True)
device_test = torch.device("cpu")

model = FastUGINet(anatomical_classes=anatomical_class_num, disease_classes=disease_class_num, cnn_size=cnn_size, vit_size=vit_size)
model.load_state_dict(torch.load(pretrained_weight_path))
test_loop_fn_multlabel(test_loader, model, device_test)