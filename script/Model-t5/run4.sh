CUDA_VISIBLE_DEVICES=0 python -u main.py --output_dir EXP/ --do_eval --do_train --data_dir ./data --save_model --load_path ../../model --train_batch_size 2 --bert_model t5-large --learning_rate 1e-4 --num_train_epochs 6 --divide_data train4