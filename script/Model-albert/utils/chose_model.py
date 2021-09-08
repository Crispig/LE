#from model.modeling_bert import BertForCloze
#from model.modeling_roberta import RobertaForCloze
from model.modeling_albert import ALbertForCloze
#from model.modeling_t5 import T5ForCloth
#from tokenization.tokenization_roberta import RobertaTokenizer
#from tokenization.tokenization_bert import BertTokenizer
from tokenization.tokenization_albert import AlbertTokenizer
#from tokenization.tokenization_t5 import T5Tokenizer
'''
pretrain/albert-xxlarge-v2
'''


def chose_model_token(model,args):
    if model == 'bert-base-uncased' or model == 'bert-large-uncased':
        token = BertTokenizer.from_pretrained(
            args.pre_training_path + '/' + args.bert_model + '/' + args.bert_model + '-vocab.txt')
        return token
    elif model == 'roberta-base' or model == 'roberta-large-openai':
        token = RobertaTokenizer.from_pretrained(
            args.pre_training_path + '/' + args.bert_model + '/' + args.bert_model + '-vocab.json')
        return token
    elif model =='albert-base-v1' or model =='albert-xxlarge-v2' or model =='albert-xxlarge-v1':
        token = AlbertTokenizer.from_pretrained(
            args.pre_training_path + '/' + args.bert_model + '/' + args.bert_model + '.model')
        return token
    #elif model =='albert-base-v1' or model =='albert-xxlarge-v2' or model =='albert-xxlarge-v1':
    #    token = AlbertTokenizer.from_pretrained(
    #            './test_v3')
    #    return token

    elif  model =='_t5-small' or model =='t5-large'or model == 't5-base':
        token = T5Tokenizer.from_pretrained(
            args.pre_training_path + '/' + args.bert_model + '/' + args.bert_model + '.model')
        return token



def chose_model_model(model,args):
    if model == 'bert-base-uncased'or model == 'bert-large-uncased':
        model = BertForCloze.from_pretrained(
            args.pre_training_path + '/' + args.bert_model + '/' + 'pytorch_model.bin',
             config=args.pre_training_path + '/' + args.bert_model + '/' + args.bert_model + '-config.json')
        return model
    elif model == 'roberta-base' or model == 'roberta-large-openai':
        model = RobertaForCloze.from_pretrained(
            args.pre_training_path + '/' + args.bert_model + '/' + 'pytorch_model.bin',
            config=args.pre_training_path + '/' + args.bert_model + '/' + args.bert_model + '-config.json')
        return model
    elif model == 'albert-base-v1'or model =='albert-xxlarge-v2' or model =='albert-xxlarge-v1':
        model = ALbertForCloze.from_pretrained(
            args.pre_training_path + '/' + args.bert_model + '/' + 'pytorch_model.bin',
            config=args.pre_training_path + '/' + args.bert_model + '/' + args.bert_model + '-config.json')
        return model
    

    
    elif model =='_t5-small' or model =='t5-large' or model == 't5-base':
        model = T5ForCloth.from_pretrained(
            args.pre_training_path + '/' + args.bert_model + '/' + 'pytorch_model.bin',
            config=args.pre_training_path + '/' + args.bert_model + '/' + args.bert_model + '-config.json')
        return model
