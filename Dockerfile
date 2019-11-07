FROM python
COPY bot.py /app/bot.py
COPY requirements.txt /app
RUN pip install -r /app/requirements.txt
ENTRYPOINT python /app/bot.py