# code by Tae Hwan Jung(Jeff Jung) @graykode
import numpy as np
import torch
import torch.nn as nn
from torch.autograd import Variable
from AutoBUlidVocabulary import *
from tqdm import tqdm
import os

from .seq2seq import *
import numpy as np   
import math

dtype = torch.FloatTensor
# S: Symbol that shows starting of decoding input
# E: Symbol that shows starting of decoding output
# P: Symbol that will fill in blank sequence if current batch data size is short than time steps

# char_arr = [c for c in 'SEPabcdefghijklmnopqrstuvwxyz']
# print("char_arr",char_arr)
# num_dic = {n: i for i, n in enumerate(char_arr)}
# print("num_dic",num_dic)
# seq_data = [['manqqq', 'womenwww'], ['black', 'white'], ['king', 'queen'], ['girl', 'boy'], ['up', 'down'], ['high', 'low']]


class Ts2s:
  def __init__(self,n_step = 3,n_hidden = 128,epoch=1000,batch_size=20,loss_num=10,path='./'):
    self.n_step = n_step  #文字长度
    self.n_hidden = n_hidden

    self.path=path+'model.pk'
    self.voc_path=path+''
    #每次处理的数据条数
    self.batch_size=batch_size
    #输出loss的次数
    self.loss_num=loss_num
    #训练多少步
    self.epoch=epoch


    # if torch.cuda.is_available():
    #   print("gpu")
    #   self.device='cuda'
    # else:
    #   self.device='cpu'

    self.vocab=GVocab(path=self.voc_path)
    self.num_dic=self.vocab.load()
    self.char_arr=list(self.num_dic)
    self.n_class = len(self.num_dic) #和字典一样 类似分类


    self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    pass 
  def bulid_data(self,seq_data):
    """
    构建数据 字符用空格隔开
    seq_data = [['b 柯 基 犬 是 个 狗 子 吗', '柯基犬'], ['哈士奇喜欢吃肉', '哈士奇'], ['猫咪喜欢吃鱼', '猫咪'], ['毛驴喜欢吃草', '毛驴'], ['牛逼的人', '人'], ['老牛拉车', '老牛']]
    """
    
    self.seq_data=seq_data
    # # vocab=Vocab(file=self.voc_path)

    # # vocab.text_voc_ids('SEP')
    # # print('bulid_voc:')
    # # # new_seq_data=[]
    # # for seq in tqdm(seq_data):
    # #   vocab.text_voc_ids(seq[0])
    # #   vocab.text_voc_ids(seq[1])
    
    # self.num_dic=vocab.load()
    # self.char_arr=list(self.num_dic)
    # # Seq2Seq Parameter
    # self.n_class = len(self.num_dic) #和字典一样 类似分类
    # self.batch_size = len(self.seq_data)
    #设置输入 x 的特征数量
    # self.batch_size = 30000

  def make_batch(self,seq_data):
      """
      构建Tensor
      """
      print('make_batch')

      input_batch, output_batch, target_batch = [], [], []
      # print('make_batch: ')
      for seq in tqdm(seq_data):
          # for i in range(2):
          #     if len(seq[i])>self.n_step:
          #       seq[i]=seq[i][:self.n_step]
          #     else:
          #       seq[i] = seq[i] + 'P' * (self.n_step - len(seq[i]))
          # # print("seq:",seq)
          # input = [self.num_dic[n] for n in seq[0]]
          input=self.vocab.sentence_ids( seq[0],text_len=self.n_step-2)
          # 'S' + seq[1]
          output=self.vocab.sentence_ids( seq[1],text_len=self.n_step-2)
          target=self.vocab.sentence_ids( seq[1],text_len=self.n_step-2)
          # output = [self.num_dic[n] for n in ('S' + seq[1])]
          # target = [self.num_dic[n] for n in (seq[1] + 'E')]
          # print("input",input)
          # print('output',output)
          # print('target',target)

          input_batch.append(np.eye(self.n_class)[input])
          output_batch.append(np.eye(self.n_class)[output])
          target_batch.append(target) # not one-hot

      # make tensor
      return Variable(torch.Tensor(input_batch)).to(self.device), Variable(torch.Tensor(output_batch)).to(self.device), Variable(torch.LongTensor(target_batch)).to(self.device)
      # return Variable(torch.Tensor(input_batch)), Variable(torch.Tensor(output_batch)), Variable(torch.LongTensor(target_batch))
  def train(self):
    # for self.seq_data

    # max_len =math.ceil(float(len(self.seq_data))/20)
    # # min_len =math.ceil(len(self.seq_data)/self.batch_size)
    # ### 向上取整 用空余的数据补全
    # new_len=max_len*self.batch_size
    # pad_lines=[]
    # for i in range(new_len-len(self.seq_data)):
    #   pad_lines.append(['[PAD]','[PAD]'])
    # self.new_seq_data=pad_lines+self.seq_data
    # self.new_seq_data=np.array(self.new_seq_data)

    # self.new_seq_data=self.new_seq_data.reshape((max_len,self.batch_size))
    # # print(new_seq_data)

    self.load()

    # print(self.new_seq_data.tolist())
    if len(self.seq_data)>self.batch_size:
      seq_batch=[]
      for i,seq_one_batch in enumerate(self.seq_data):
        #分批次执行
        # seq_batch=[]

        # i=0
        if i%self.batch_size==0 and i!=0:
          #如果整除批次的话

          self.train_one_batch(seq_batch)
          # print('整除',i)
          # print('seq_batch',seq_batch)
          seq_batch=[]
        else:
          # print("那奶奶",seq_one_batch)
          seq_batch.append(seq_one_batch)
 
        # print('22怒',i)
      # 运行最后一次
      self.train_one_batch(seq_batch)
    else:
      self.train_one_batch(self.seq_data)
      pass
          
  def train_one_batch(self,seq_batch):
    print('运行一个batch')
    # print('self.batch_size',self.batch_size)
    self.criterion = nn.CrossEntropyLoss()
    self.optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
    self.lr_scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(self.optimizer, T_max = (self.epoch // 9) + 1,eta_min=1e-10)
        #运行训练
    input_batch, output_batch, target_batch = self.make_batch(seq_batch)
    ##执行加载模型 没有的话自动创建
    # lr_scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max = (self.epoch // 10) + 1,eta_min=4e-08)
    for epoch in tqdm(range(self.epoch)):

        # self.batch_size = len(self.seq_data)

        # make hidden shape [num_layers * num_directions, batch_size, n_hidden]
        # hidden = Variable(torch.zeros(1, self.batch_size, self.n_hidden)).to(self.device)
        #  full_size = len(self.seq_data)

        hidden = Variable(torch.zeros(1, len(seq_batch), self.n_hidden)).to(self.device)
        self.optimizer.zero_grad()
        # input_batch : [batch_size, max_len(=n_step, time step), n_class]
        # output_batch : [batch_size, max_len+1(=n_step, time step) (becase of 'S' or 'E'), n_class]
        # target_batch : [batch_size, max_len+1(=n_step, time step)], not one-hot
        #训练
        output = self.model(input_batch, hidden, output_batch)
        # output : [max_len+1, batch_size, num_directions(=1) * n_hidden]
        output = output.transpose(0, 1) # [batch_size, max_len+1(=6), num_directions(=1) * n_hidden]
        loss = 0
        acc=0
        for i in range(0, len(target_batch)):
            # output[i] : [max_len+1, num_directions(=1) * n_hidden, target_batch[i] : max_len+1]
            loss += self.criterion(output[i], target_batch[i])
            acc_one=self.compute_loss(output[i], target_batch[i])
            acc+=acc_one
        # loss_num =math.ceil(float(len(self.epoch))/10)
        if (epoch + 1) % self.loss_num  == 0:
            print('Epoch:', '%04d' % (epoch + 1), 'cost =', '{:.6f}'.format(loss),'acc =', '{:.6f}'.format(acc))
            # print('Epoch:', '%04d' % (epoch + 1), 'acc =', '{:.6f}'.format(acc))
        loss.backward()
        # print(loss)


        self.optimizer.step()
        self.lr_scheduler.step(acc)
        torch.save(self.model.state_dict(), self.path)

  def compute_loss(self,predicts , labels  ):
      assert predicts.shape[0] == labels.shape[0]
      acc = torch.sum( torch.eq(labels  , torch.max( predicts , 1 )[1] ).long() ).float()/ float( labels.shape[0] )
      # loss = criterion( predicts , labels )
      return acc 

  def load(self):
    """"
    加载模型
    自动会判断是否是使用cpu
    """
    # 模型转化保存 https://pytorch.org/tutorials/beginner/saving_loading_models.html
    # print("wew")
    # self.model=torch.load( self.path)
    # self.model.eval()
    # vocab=GVocab(file=self.voc_path)
    # self.num_dic=vocab.load()
    # self.char_arr=list(self.num_dic)
    # self.n_class = len(self.num_dic) #和字典一样 类似分类

    self.model = Seq2Seq(n_class=self.n_class,n_hidden=self.n_hidden).to(self.device)    #模型使用了cuda()
    if os.path.exists(self.path):
      self.model.load_state_dict(torch.load(self.path))  
      # model.load_state_dict(torch.load(PATH, map_location="cuda:0"))  # Choose whatever GPU device number you want
      self.model.to(self.device)


    # self.batch_size = len(self.seq_data)
  # Test
  def translate(self,seq_list):
      """
      执行预测
      多个预测 使用空格分割
      seq_list=['你 好','怎 么 样']
      """
      self.load()
      # input_batch, output_batch, _ = self.make_batch([[word, '[PAD]' * len(word)]])
      # input_batch, output_batch, _ = self.make_batch([[word, '' ]])

      input_batch, output_batch, _ = self.make_batch(seq_list)
      # make hidden shape [num_layers * num_directions, batch_size, n_hidden]
      hidden = Variable(torch.zeros(1, 1, self.n_hidden)).to(self.device)
      #加载模型

      output = self.model(input_batch, hidden, output_batch)
      # output : [max_len+1(=6), batch_size(=1), n_class]
      # print("output.data.max(2, keepdim=True)",output.data.max(2, keepdim=True))
      # predict0 = output.data.max(2, keepdim=True)[0] # select n_class dimension
      # decoded0 = [self.char_arr[i] for i in predict0]
      # print(decoded0)



      predict = output.data.max(2, keepdim=True)[1] # select n_class dimension
      decoded = [self.char_arr[i] for i in predict]
      print(decoded)
      try:
        end = decoded.index('[SEP]')
        translated = ''.join(decoded[:end])
      except:
        print("无正确返回")
        translated = ''.join(decoded)
      text=translated.replace('[PAD]', '')
      return text.replace('[CLS]', '')