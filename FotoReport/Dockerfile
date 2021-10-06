FROM bensuperpc/python3-opencv:amd64-4.5.2

WORKDIR /fotoreport

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt update && apt -y install libsasl2-dev python-dev libldap2-dev libssl-dev
RUN pip install --upgrade pip
COPY ./requirements.txt /fotoreport
RUN pip install -r requirements.txt

# copy project
COPY . /fotoreport

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]