# ============================
#            Buider
# ============================
FROM python:3.10-slim AS builder

# setup environment variable  
ENV DockerHOME=/home/app/webapp
# set work directory  
RUN mkdir -p $DockerHOME  
# where your code lives  
WORKDIR $DockerHOME

# Install build dependencies
RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
	gcc libpq-dev postgresql-client \
	python3-dev default-libmysqlclient-dev nano \
	&& apt autoremove \
	&& apt clean \
	&& rm -rf /var/lib/apt/lists/*

# copy whole project to your docker home directory.
COPY ./docs/requirements.txt $DockerHOME

# install dependencies  
RUN pip install --upgrade pip  
# run this command to install all dependencies  
RUN pip install -r requirements.txt  


# ============================
#          Runtime Stage
# ============================
FROM python:3.10-slim

# setup environment variable  
ENV DockerHOME=/home/app/webapp
# set work directory  
RUN mkdir -p $DockerHOME  
# where your code lives  
WORKDIR $DockerHOME

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

# Install build dependencies
RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
	libpq-dev default-libmysqlclient-dev \
	&& apt autoremove \
	&& apt clean \
	&& rm -rf /var/lib/apt/lists/*

# Copy from the builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy the application code
COPY ./project $DockerHOME
COPY ./docs/requirements.txt $DockerHOME

# port where the Django app runs  
# EXPOSE 8000

# start server  
# CMD python manage.py runserver 0000:8000