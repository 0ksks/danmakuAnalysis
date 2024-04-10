import torch
import torch.nn as nn
from torch.optim import Adam
import lightning as L

class nnLSTM(L.LightningModule):
    def __init__(self,wordVecLen,sentenceLen,hiddenSize,classification):#wordVecLen：词向量长度；sentenceLen：句子长度；hiddenSize：隐藏层输出维度；classification：分类个数
        super().__init__()
        self.hidden = (torch.randn(1,2,1))
        self.training_step_outputs = []
        self.lstm = nn.LSTM(input_size=wordVecLen,hidden_size=hiddenSize,batch_first=True)
        self.linear = nn.Linear(sentenceLen,classification)

    def forward(self, input):
        hidden = self.hidden
        out, hidden = self.lstm(input)
        out = out.view(len(input),-1)
        pred = self.linear(out)
        return pred[-1]
    
    def configure_optimizers(self):
        return Adam(self.parameters(),lr=0.1)

    def training_step(self, batch, batchIdx):
        inputI, labelI = batch
        pred = self.forward(inputI)
        cri = torch.tensor(list(map(float,[labelI,1-labelI])))
        crossEntropyLoss = nn.CrossEntropyLoss()
        loss = crossEntropyLoss(pred,cri)
        self.training_step_outputs.append(loss)
        return loss
    
    def on_train_epoch_end(self):
        epoch_mean = torch.stack(self.training_step_outputs).mean()
        self.log("training_epoch_mean", epoch_mean)
        self.training_step_outputs.clear()