FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip python3 build-essential curl
COPY . /app
WORKDIR /app 
RUN pip3 install -r requirements.txt
EXPOSE 5000 80
ENTRYPOINT ["python3"]
CMD ["app.py"]
