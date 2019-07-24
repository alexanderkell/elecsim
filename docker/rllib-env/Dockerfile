FROM python:3.6

COPY requirements.txt /
RUN pip install -r requirements.txt

ADD . /app
COPY . /app

WORKDIR /app

ENV NAME World

ENV PYTHONPATH "${PYTHONPATH}:/elecsim"

CMD ["python", "-u", "run/reinforcement_learning/investor_strategies/learn_investment_strategy.py"]



