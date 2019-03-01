FROM python:3.6


COPY requirements.txt /
RUN pip install -r requirements.txt

ADD . /app
COPY . /app

WORKDIR /app
	
ENV NAME World

ENV PYTHONPATH "${PYTHONPATH}:/elecsim"

ENTRYPOINT ["python", "run/timing/batch_run_timer.py"]

CMD ["python", "run/timing/batch_run_timer.py"]



