import pandas as pd
import numpy as np
import torch
from kobert_transformers import get_tokenizer
from transformers import BertModel
from sklearn.linear_model import LogisticRegression
import joblib  # 가중치 저장/불러오기용

# 1. 데이터 준비 (꼭 라벨 데이터 필요: 0=부정, 1=긍정 등)
comments_df = pd.read_table('dev/model/data/ratings_train.txt')  # comment, label 
comments_df = comments_df.dropna(subset=['document'])
comments_df = comments_df[comments_df['document'].apply(lambda x: isinstance(x, str))]

comments = comments_df['document'].tolist()
labels = comments_df['label'].tolist()

# 2. KoBERT 토크나이저 & 임베딩모델 불러오기
tokenizer = get_tokenizer()
model = BertModel.from_pretrained('monologg/kobert')

# 3. [CLS] 임베딩 추출 함수
def get_cls_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        cls_emb = outputs.last_hidden_state[:, 0, :].squeeze().numpy()
    return cls_emb

# 4. 전체 데이터 임베딩 생성
embeddings = np.stack([get_cls_embedding(text) for text in comments])

# 5. 분류기 학습
clf = LogisticRegression(max_iter=1000)
clf.fit(embeddings, labels)

# 6. 분류기 가중치 저장
joblib.dump(clf, "kobert_lr_sentiment.pkl")
print("분류기 가중치가 kobert_lr_sentiment.pkl로 저장되었습니다.")
