FROM python

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app/

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

EXPOSE 55000

# runs the production server
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:55000"]