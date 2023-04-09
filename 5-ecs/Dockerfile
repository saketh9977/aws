FROM python:alpine3.17

RUN mkdir /runtime
WORKDIR /runtime
COPY . .

RUN pip install -r requirements.txt
CMD ["python", "main.py"]
