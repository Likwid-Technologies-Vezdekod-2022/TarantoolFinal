FROM python:3.9


RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY run.sh .

COPY . .

EXPOSE 8081

RUN chmod +x run.sh

CMD ["./run.sh"]