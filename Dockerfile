FROM python:3.6


COPY requirements.txt /
RUN pip install -r requirements.txt

ADD . /app
COPY . /app

WORKDIR /app
	
ENV NAME World

ENV PYTHONPATH "${PYTHONPATH}:/elecsim"

CMD ["python", "run/reinforcement_learning/carbon_optimiser.py"]



