from glove import getSentencesAndLabels
import lstm
from torch.utils.data import TensorDataset, DataLoader
from torch import tensor
import lightning as L

fpath = "/Users/pc/Desktop/danmakuAnalysis.nosync/"#路径头

sentences, labels = getSentencesAndLabels()
lstmNLP = lstm.nnLSTM(5,200,1,2)
sentences = tensor(sentences)
labels = tensor(labels)
print(sentences.shape)
print(labels.shape)
trainSet = TensorDataset(sentences, labels)
trainSetLoader = DataLoader(dataset=trainSet)
trainer = L.Trainer(max_epochs=50,default_root_dir=fpath[:-1])
trainer.fit(model=lstmNLP, train_dataloaders=trainSetLoader)
'''
tensorboard --logdir=lightning_logs/
'''