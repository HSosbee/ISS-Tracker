FROM ubuntu:20.04

RUN mkdir /app
WORKDIR /app
COPY . /app
RUN apt-get update && \
	apt-get upgrade -y && \
	apt-get install -y python3 && \
	apt-get install -y python3-pip

RUN pip3 install -r /app/requirements.txt

ENTRYPOINT ["python3"]
CMD ["iss_tracker.py"]
