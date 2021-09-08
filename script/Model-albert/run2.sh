CUDA_VISIBLE_DEVICES=1 python -u main.py --output_dir EXP/ \
--do_eval --load_model \
--eval_batch_size 2 --bert_model albert-xxlarge-v2 \
--data_dir ./data/data \
--load_path ./output_1_7/model_all