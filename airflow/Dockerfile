FROM apache/airflow:3.0.0

ENV AIRFLOW_HOME=/opt/airflow


WORKDIR $AIRFLOW_HOME

USER $AIRFLOW_UID
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
