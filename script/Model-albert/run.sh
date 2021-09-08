CUDA_VISIBLE_DEVICES=1 python -u main.py --output_dir EXP/ \
--do_eval --do_train --save_model \
--train_batch_size 4 --bert_model albert-xxlarge-v2 \
--learning_rate 9e-6 --num_train_epochs 2 \
--gradient_accumulation_steps 2 \
--data_dir ./data \
--load_path output_1_7/model_all