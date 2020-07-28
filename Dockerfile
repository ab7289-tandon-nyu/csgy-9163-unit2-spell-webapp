FROM python:3.7

RUN mkdir /app

COPY ./requirements.txt /app

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

RUN chmod +x ./app/lib/a.out

EXPOSE 5000

CMD [ "python", "app.py" ]