FROM python:3.9.10-alpine

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY action_monitor.py /app/
WORKDIR /app

ENTRYPOINT [ "python", "action_monitor.py", "-d", "monitored" ]
