#python version
FROM python:3.8.10

#create folder
RUN mkdir -p /var/www/app

RUN apt-get update && apt-get install --no-install-recommends --yes python3
RUN apt-get install -y python3-pip
RUN pip3 install requests
RUN pip3 install gunicorn


#Install dependencies
COPY requirements.txt /var/www/app
WORKDIR /var/www/app
RUN pip3 install  -r requirements.txt
COPY . /var/www/app

# Expose the default port
EXPOSE 5000

#Gunicorn 
CMD [ "gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]




