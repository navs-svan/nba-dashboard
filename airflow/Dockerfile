FROM apache/airflow:3.0.0

ENV AIRFLOW_HOME=/opt/airflow

WORKDIR $AIRFLOW_HOME

USER root

RUN apt-get update && apt-get install -y git && apt-get clean

USER $AIRFLOW_UID

COPY requirements.txt constraints.txt ./ 

RUN pip install --upgrade pip && \
    pip install --no-cache-dir --use-feature=fast-deps -r requirements.txt -c constraints.txt