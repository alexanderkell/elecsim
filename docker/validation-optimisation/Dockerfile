FROM python:3.6

COPY requirements.txt /
RUN pip install -r requirements.txt

#ADD . /app
COPY . /app

WORKDIR /app

ENV NAME World

ENV PYTHONPATH "${PYTHONPATH}:/elecsim"
VOLUME [ "my-vol" ]

CMD ["python", "-m", "scoop", "run/validation-optimisation/run_price_fitter_investment/run_GA_price_fitter.py"]
