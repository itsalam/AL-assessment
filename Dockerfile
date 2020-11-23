FROM python:3.7

RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN pip install -r requirements.txt

RUN python -m pytest tests

EXPOSE 5000
CMD ["python", "/app/main.py"]