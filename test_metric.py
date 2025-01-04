import sys
sys.path.append('/mnt/3T_disk/chenqi1/chenqi/cold-compress/bertscore')

from bertscore import BERTScore  # 假设您下载的文件名为 bertscore.py

# 创建 BERTScore 实例，指定模型路径和语言
metric = BERTScore(model_type='microsoft/deberta-xlarge-mnli', lang='en')

# 使用 metric 进行评估
predictions = ["The answer is 42."]
references = ["The answer is 42."]
results = metric.compute(predictions=predictions, references=references)
print(results)