import torch.nn as nn
from torchvision.models import efficientnet_b0, efficientnet_b4, efficientnet_b5, efficientnet_b1, efficientnet_b2, efficientnet_b3, efficientnet_b6, efficientnet_b7
from timm.models.mobilevit import mobilevit_xs, mobilevit_s, mobilevit_xxs


class FastUGINet(nn.Module):
    def __init__(
            self,
            anatomical_classes,
            disease_classes,
            a_dropout=0.1,
            d_dropout=0.1,
            cnn_size='b0',
            vit_size='xxs'):
        super().__init__()

        if cnn_size == 'b0':
            basemodel1 = efficientnet_b0(pretrained=True)
            self.conv_in = 80
            self.upsampling_scale = 2

        if cnn_size == 'b1':
            basemodel1 = efficientnet_b1(pretrained=True)
            self.conv_in = 80
            self.upsampling_scale = 2

        if cnn_size == 'b2':
            basemodel1 = efficientnet_b2(pretrained=True)
            self.conv_in = 88
            self.upsampling_scale = 2

        if cnn_size == 'b3':
            basemodel1 = efficientnet_b3(pretrained=True)
            self.conv_in = 96
            self.upsampling_scale = 2

        if cnn_size == 'b4':
            basemodel1 = efficientnet_b4(pretrained=True)
            self.conv_in = 112
            self.upsampling_scale = 2

        if cnn_size == 'b5':
            basemodel1 = efficientnet_b5(pretrained=True)
            self.conv_in = 128
            self.upsampling_scale = 2

        if cnn_size == 'b6':
            basemodel1 = efficientnet_b6(pretrained=True)
            self.conv_in = 144
            self.upsampling_scale = 2

        if cnn_size == 'b7':
            basemodel1 = efficientnet_b7(pretrained=True)
            self.conv_in = 160
            self.upsampling_scale = 2


        if vit_size == 'xxs':
            basemodel2 = mobilevit_xxs(pretrained=True)
            self.vit_in = 48
            self.in_features = 320

        if vit_size == 'xs':
            basemodel2 = mobilevit_xs(pretrained=True)
            self.vit_in = 64
            self.in_features = 384


        if vit_size == 's':
            basemodel2 = mobilevit_s(pretrained=True)
            self.vit_in = 96
            self.in_features = 640

        conv1 = basemodel1.features[0]
        block1 = basemodel1.features[1]
        block2 = basemodel1.features[2]
        block3 = basemodel1.features[3]
        block4 = basemodel1.features[4]
        conv = nn.Conv2d(in_channels=self.conv_in, out_channels=self.vit_in, kernel_size=1)  # 1, 96, 14, 14)
        upsample = nn.Upsample(scale_factor=self.upsampling_scale, mode='bilinear')
        stages3 = basemodel2.stages[3]
        stages4 = basemodel2.stages[4]
        final_conv = basemodel2.final_conv
        self.backbone = nn.Sequential(conv1, block1, block2, block3, block4,
                                      conv, upsample, stages3, stages4, final_conv)

        self.anatomical_classification_head = nn.Sequential(
            nn.AdaptiveAvgPool2d(output_size=1),
            nn.Flatten(),
            nn.Linear(in_features=self.in_features, out_features=self.in_features // 2),
            nn.BatchNorm1d(self.in_features // 2),
            nn.ReLU(),
            nn.Dropout(p=a_dropout),
            nn.Linear(in_features=self.in_features // 2, out_features=self.in_features // 4),
            nn.BatchNorm1d(self.in_features // 4),
            nn.ReLU(),
            nn.Dropout(p=a_dropout),
            nn.Linear(in_features=self.in_features // 4, out_features=anatomical_classes),
        )
        self.disease_classification_head = nn.Sequential(
            nn.AdaptiveAvgPool2d(output_size=1),
            nn.Flatten(),
            nn.Linear(in_features=self.in_features, out_features=self.in_features // 2),
            nn.BatchNorm1d(self.in_features // 2),
            nn.ReLU(),
            nn.Dropout(p=d_dropout),
            nn.Linear(in_features=self.in_features // 2, out_features=self.in_features // 4),
            nn.BatchNorm1d(self.in_features // 4),
            nn.ReLU(),
            nn.Dropout(p=d_dropout),
            nn.Linear(in_features=self.in_features // 4, out_features=disease_classes),
        )

    def forward(self, x):
        x = self.backbone(x)
        anatomical_output = self.anatomical_classification_head(x)
        disease_output = self.disease_classification_head(x)

        return anatomical_output, disease_output
