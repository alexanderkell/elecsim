FROM python:3.6

COPY requirements.txt /
RUN pip install -r requirements.txt

#ADD . /app
COPY . /app

WORKDIR /app

ENV NAME World

ENV PYTHONPATH "${PYTHONPATH}:/elecsim"
VOLUME [ "my-vol" ]

CMD ["python", "-m", "scoop", "run/beis_case_study/optimisation/optimiser_for_beis_scenario.py"]
