# DockerHubのイメージ
FROM python:3.12.4-slim
# 作業ディレクトリの指定
WORKDIR /workspace
# ローカルのファイルをコンテナ内にコピー
COPY requirements.txt ${pwd}
# 必要なパッケージをインストール
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV PYTHONPATH=/workspace/src
