FROM python:3.6

WORKDIR /run/reinforcement_learning/

ADD . /run/reinforcement_learning/

RUN pip install -r requirements.txt

ENV NAME World

CMD ["python", "/run/reinforcement_learning/carbon_optimiser.py"]



