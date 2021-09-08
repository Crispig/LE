from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
from utils.chose_model import chose_model_token
import fnmatch
import json
import os
import torch
import random

all_ops_sum = []

def to_device(L, device):
    if (type(L) != list):
        return L.to(device)
    else: 
        ret = []
        for item in L:
            ret.append(to_device(item, device))
        return ret


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
        #tokenizer.add_tokens([ops[i]])
        #ret.append(['▁'+ops[i].lower()])
    return ret


class ClothSample(object):
    def __init__(self):
        self.article = None
        self.ph = []
        self.ops = []
        self.ans = []

    def convert_tokens_to_ids(self, tokenizer):
        self.article = torch.Tensor(tokenizer.encode(self.article,max_length=512))
        for i in range(len(self.ops)):
            for k in range(4):
                self.ops[i][k] = tokenizer.convert_tokens_to_ids(self.ops[i][k])
                self.ops[i][k] = torch.Tensor(self.ops[i][k])
        self.ph = torch.Tensor(self.ph)
        self.ans = torch.Tensor(self.ans)


class Loader(object):
    def __init__(self, data_dir, data_file, cache_size, batch_size, device='cpu'):
        #self.tokenizer = BertTokenizer.from_pretrained(args.bert_model)
        self.data_dir = os.path.join(data_dir, data_file)
        print('loading {}'.format(self.data_dir))
        self.data = torch.load(self.data_dir)
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
            max_ops_num  = max(max_ops_num, len(data.ops))
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
                    options[i,q,k,:op.size(0)] = op
                    options_mask[i,q,k, op.size(0):] = 0
            for q, ans in enumerate(data.ans):
                answers[i,q] = ans
                mask[i,q] = 1
            for q, pos in enumerate(data.ph):
                question_pos[i,q] = pos
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


class Preprocessor:

    def __init__(self, args):

        self.tokenizer = chose_model_token(args.bert_model, args)
        self.data_dir = args.data_dir
        file_list = get_json_file_list(args.data_dir)
        self.data = []
        #m = np.array(all_ops_sum)
        #np.save('demo.npy', m)
        for file_name in file_list:
            data = json.loads(open(file_name, 'r').read())
            self.data.append(data)

        self.data_objs = []
        for sample in self.data:
            self.data_objs += self._create_sample(sample)
        for i in range(len(self.data_objs)):
            self.data_objs[i].convert_tokens_to_ids(self.tokenizer)
        torch.save(self.data_objs, args.save_name)
        #tokenizer.save_pretrained('./pre_trianing'+args.bert_model+'/'+args.bert_model+'.model')

    # make input-dataset from raw json dataset
    def _create_sample(self, data):
        cnt = 0
        # get article
        article = self.tokenizer.tokenize(data['article'])
        # 判断文章是否大于 512
        if (len(article) <= 512):
            sample = ClothSample()
            sample.article = article
            for p in range(len(article)):
                if (sample.article[p] == '_'):
                    sample.article[p] = '[MASK]'
                    sample.ph.append(p)
                    ops = tokenize_ops(data['options'][cnt], self.tokenizer)
                    sample.ops.append(ops)
                    sample.ans.append(ord(data['answers'][cnt]) - ord('A'))
                    cnt += 1
            return [sample]
        else:
            first_sample = ClothSample()
            second_sample = ClothSample()
            second_s = len(article) - 512
            for p in range(len(article)):
                if (article[p] == '_'):
                    article[p] = '[MASK]'
                    ops = tokenize_ops(data['options'][cnt], self.tokenizer)
                    if (p < 512):
                        first_sample.ph.append(p)
                        first_sample.ops.append(ops)
                        # 
                        first_sample.ans.append(ord(data['answers'][cnt]) - ord('A'))
                    else:
                        second_sample.ph.append(p - second_s)
                        second_sample.ops.append(ops)
                        second_sample.ans.append(ord(data['answers'][cnt]) - ord('A'))
                    cnt += 1                    
            first_sample.article = article[:512]
            second_sample.article = article[-512:]
            if (len(second_sample.ans) == 0):
                return [first_sample]
            else:
                return [first_sample, second_sample]



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='bert cloth')

    parser.add_argument("--bert_model",
                        default='albert-xxlarge-v2',
                        type=str,
                        help="type of bert model")
    args = parser.parse_args()

    data_collections = ['train', 'dev']
    for item in data_collections:    
        args.data_dir = './ELE/{}'.format(item)
        args.pre_training_path = './pre_training'
        args.pre = args.post = 0
        args.save_name = './data/{}-{}.pt'.format(item,args.bert_model)
        data = Preprocessor(args)
        
