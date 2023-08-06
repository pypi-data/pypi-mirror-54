# code by Tae Hwan Jung(Jeff Jung) @graykode
import numpy as np
import torch
import torch.nn as nn
from torch.autograd import Variable
from AutoBUlidVocabulary import *
from tqdm import tqdm
import os

dtype = torch.FloatTensor

# Model
class Seq2Seq(nn.Module):
    def __init__(self,n_class=10,n_hidden=128):
        super(Seq2Seq, self).__init__()
        

        self.enc_cell = nn.RNN(input_size=n_class, hidden_size=n_hidden, dropout=0.5)  #模型使用了cuda()
        self.dec_cell = nn.RNN(input_size=n_class, hidden_size=n_hidden, dropout=0.5) #模型使用了cuda()
        self.fc = nn.Linear(n_hidden, n_class)

    def forward(self, enc_input, enc_hidden, dec_input):
        enc_input = enc_input.transpose(0, 1) # enc_input: [max_len(=n_step, time step), batch_size, n_class]
        dec_input = dec_input.transpose(0, 1) # dec_input: [max_len(=n_step, time step), batch_size, n_class]

        # enc_states : [num_layers(=1) * num_directions(=1), batch_size, n_hidden]
        _, enc_states = self.enc_cell(enc_input, enc_hidden)
        # outputs : [max_len+1(=6), batch_size, num_directions(=1) * n_hidden(=128)]
        outputs, _ = self.dec_cell(dec_input, enc_states)

        model = self.fc(outputs) # model : [max_len+1(=6), batch_size, n_class]
        return model
