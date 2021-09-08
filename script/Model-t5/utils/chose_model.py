from model.modeling_bert import BertForCloze
from model.modeling_t5 import T5ForCloze

from tokenization.tokenization_bert import BertTokenizer
from tokenization.tokenization_t5 import T5Tokenizer


def chose_model_token(model, args):
    if model == 't5-small' or model == 't5-base' or model == 't5-large':
        token = T5Tokenizer.from_pretrained(
            args.pre_training_path + '/' + args.bert_model + '.model')
        return token


def chose_model_model(model, args):
    if model == 't5-small' or model == 't5-base' or model == 't5-large':
        model = T5ForCloze.from_pretrained(
            args.pre_training_path + '/' + 'pytorch_model.bin',
            config=args.pre_training_path + '/' + args.bert_model + '-config.json')
        print(args.bert_model)
        return model