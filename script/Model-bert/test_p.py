from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse

import numpy as np
# from utils.chose_model import chose_model_token
import fnmatch
import json
import os
import torch
import random
# import numba as nb

def to_device(L, device):
    if (type(L) != list):
        return L.to(device)
    else:
        ret = []
        for item in L:
            ret.append(to_device(item, device))
        return ret


def pretraining_and_saving_tokenization(data_dir):
    files = []
    for root, dir_names, file_names in os.walk(data_dir):
        for filename in fnmatch.filter(file_names, '*.json'):
            files.append(os.path.join(root, filename))
    return files


def get_json_file_list(data_dir):
    files = []
    for root, dir_names, file_names in os.walk(data_dir):
        for filename in fnmatch.filter(file_names, '*.json'):
            files.append(os.path.join(root, filename))
    return files


def tokenize_ops(ops, tokenizer):
    ret = []
    for i in range(4):
        ret.append(tokenizer.tokenize(ops[i]))
    return ret


class ClothSample(object):
    def __init__(self):
        self.article = None
        self.ph = []
        self.ops = []
        self.ans = []
        self.high = 0

    def convert_tokens_to_ids(self, tokenizer):
        self.article = tokenizer.convert_tokens_to_ids(self.article)
        self.article = torch.Tensor(self.article)
        for i in range(len(self.ops)):
            for k in range(4):
                self.ops[i][k] = tokenizer.convert_tokens_to_ids(self.ops[i][k])
                self.ops[i][k] = torch.Tensor(self.ops[i][k])
        self.ph = torch.Tensor(self.ph)
        self.ans = torch.Tensor(self.ans)


class Loader(object):
    def __init__(self, sample_list,cache_size=2, batch_size=1, device='cpu'):
        self.data = sample_list
        self.cache_size = cache_size
        self.batch_size = batch_size
        self.data_num = len(self.data)
        self.device = device

    def _batchify(self, data_set, data_batch):
        max_article_length = 0
        max_option_length = 0
        max_ops_num = 0
        bsz = len(data_batch)
        for idx in data_batch:
            data = data_set[idx]
            max_article_length = max(max_article_length, data.article.size(0))
            for ops in data.ops:
                for op in ops:
                    max_option_length = max(max_option_length, op.size(0))
            max_ops_num = max(max_ops_num, len(data.ops))
        articles = torch.zeros(bsz, max_article_length).long()
        articles_mask = torch.ones(articles.size())
        options = torch.zeros(bsz, max_ops_num, 4, max_option_length).long()
        options_mask = torch.ones(options.size())
        answers = torch.zeros(bsz, max_ops_num).long()
        mask = torch.zeros(answers.size())
        question_pos = torch.zeros(answers.size()).long()
        # high_mask = torch.zeros(bsz) #indicate the sample belong to high school set
        for i, idx in enumerate(data_batch):
            data = data_set[idx]
            articles[i, :data.article.size(0)] = data.article
            articles_mask[i, data.article.size(0):] = 0
            for q, ops in enumerate(data.ops):
                for k, op in enumerate(ops):
                    options[i, q, k, :op.size(0)] = op
                    options_mask[i, q, k, op.size(0):] = 0
            for q, ans in enumerate(data.ans):
                answers[i, q] = ans
                mask[i, q] = 1
            for q, pos in enumerate(data.ph):
                question_pos[i, q] = pos
            # high_mask[i] = data.high
        inp = [articles, articles_mask, options, options_mask, question_pos, mask]
        tgt = answers
        return inp, tgt

    def data_iter(self, shuffle=True):
        if (shuffle == True):
            random.shuffle(self.data)
        seqlen = torch.zeros(self.data_num)
        for i in range(self.data_num):
            seqlen[i] = self.data[i].article.size(0)
        cache_start = 0
        while (cache_start < self.data_num):
            cache_end = min(cache_start + self.cache_size, self.data_num)
            cache_data = self.data[cache_start:cache_end]
            seql = seqlen[cache_start:cache_end]
            _, indices = torch.sort(seql, descending=True)
            batch_start = 0
            while (batch_start + cache_start < cache_end):
                batch_end = min(batch_start + self.batch_size, cache_end - cache_start)
                data_batch = indices[batch_start:batch_end]
                inp, tgt = self._batchify(cache_data, data_batch)
                inp = to_device(inp, self.device)
                tgt = to_device(tgt, self.device)
                yield inp, tgt
                batch_start += self.batch_size
            cache_start += self.cache_size




if __name__ == "__main__":
    from tokenization.tokenization_bert import BertTokenizer
    import logging
    model_name = 'bert-base-uncased'
    model1 = torch.load('../../model/'+model_name+'-1.bin', map_location=torch.device('cpu'))
    model2 = torch.load('../../model/'+model_name+'-2.bin', map_location=torch.device('cpu'))
    model3 = torch.load('../../model/'+model_name+'-3.bin', map_location=torch.device('cpu'))
    model4 = torch.load('../../model/'+model_name+'-4.bin', map_location=torch.device('cpu'))
    if isinstance(model1, torch.nn.DataParallel):
         model1 = model1.module
    if isinstance(model2, torch.nn.DataParallel):
         model2 = model2.module
    if isinstance(model3, torch.nn.DataParallel):
         model3 = model3.module
    if isinstance(model4, torch.nn.DataParallel):
         model4 = model4.module
    model1.eval()
    model2.eval()
    model3.eval()
    model4.eval()
    f1 = open('../result/test-bert-base-uncased-1.txt','w')
    f2 = open('../result/test-bert-base-uncased-2.txt','w')
    f3 = open('../result/test-bert-base-uncased-3.txt','w')
    f4 = open('../result/test-bert-base-uncased-4.txt','w')
    ft = open('../result/test-bert-base-uncased-tgt.txt','w')

    tokenizer = BertTokenizer.from_pretrained('./' + model_name + '/' + 'vocab.txt')
    def eval(file='./ELE/test/test0056.json'):
        second_num = 0
        data = json.loads(open(file, 'r').read())

        article = tokenizer.tokenize(data['article'])

        sample_list = []
        cnt = 0
        ops_sum = []
        ops_sum_token = []


        if (len(article) <= 512):
            sample = ClothSample()
            sample.article = article

            for p in range(len(article)):
                if (sample.article[p] == '_'):
                    sample.article[p] = '[MASK]'
                    sample.ph.append(p)
                    ops = tokenize_ops(data['options'][cnt], tokenizer)
                    sample.ops.append(ops)
                    ops_sum_token.append(ops)
                    ops_sum.append(data['options'][cnt])
                    sample.ans.append(0)
                    cnt += 1
            #print(sample.article)
            sample.convert_tokens_to_ids(tokenizer)
            sample_list.append(sample)
        else:
            first_sample = ClothSample()
            second_sample = ClothSample()
            second_s = len(article) - 512
            ops_sum.append(data['options'][cnt])
            for p in range(len(article)):
                if (article[p] == '_'):
                    article[p] = '[MASK]'
                    ops = tokenize_ops(data['options'][cnt], tokenizer)
                    ops_sum.append(data['options'][cnt])
                    if (p < 512):
                        first_sample.ph.append(p)
                        first_sample.ops.append(ops)
                        ops_sum_token.append(ops)
                        ops_sum.append(data['options'][cnt])
                        first_sample.ans.append(0)
                        #global second_num
                        second_num += 1
                    else:
                        second_sample.ph.append(p - second_s)
                        second_sample.ops.append(ops)
                        ops_sum_token.append(ops)
                        ops_sum.append(data['options'][cnt])
                        second_sample.ans.append(0)
                    cnt += 1
            if (len(second_sample.ans) == 0):
                first_sample.article = article[:512]
                first_sample.convert_tokens_to_ids(tokenizer)
                sample_list.append(first_sample)
            else:
                first_sample.article = article[:512]
                second_sample.article = article[-512:]
                first_sample.convert_tokens_to_ids(tokenizer)
                second_sample.convert_tokens_to_ids(tokenizer)
                sample_list.append(first_sample)
                sample_list.append(second_sample)

       
        # num=0
        for k in range(len(sample_list)):
            load = Loader([sample_list[k]])
            for inp, tgt in load.data_iter():
                print("***** Running Answer Generation *****:",file)

                loss1,acc1,out1 = model1(inp,tgt)
                loss2,acc2,out2 = model2(inp,tgt)
                loss3,acc3,out3 = model3(inp,tgt)
                loss4,acc4,out4 = model4(inp,tgt)

                print(out1.detach().numpy().tolist(),file=f1)
                print(out2.detach().numpy().tolist(),file=f2)
                print(out3.detach().numpy().tolist(),file=f3)
                print(out4.detach().numpy().tolist(),file=f4)
                print(file,':',tgt.detach().numpy()[0],file=ft)

                # print(torch.argmax(out1, 1).tolist())


                tgt = tgt.squeeze(0).tolist()


    files = get_json_file_list('./ELE/test')
    num=0
    for fi in files:
        eval(fi)
        num+=1
    print(num)
    #eval()
    #eval('dev0001.json')

