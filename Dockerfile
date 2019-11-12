FROM python:3.6


COPY requirements.txt /
RUN pip install -r requirements.txt

ADD . /app
COPY . /app

WORKDIR /app
	
ENV NAME World

ENV PYTHONPATH "${PYTHONPATH}:/elecsim"

#ENTRYPOINT ["python", "test/test_model/test_world.py"]

#CMD ["python", "test/test_model/test_world.py"]
#CMD ["python", "-m", "scoop", "run/beis_case_study/optimisation/optimiser_for_beis_scenario.py"]
CMD ["python", "-m", "scoop", "run/carbon_tax_optimiser/run/carbon_tax_optimiser.py"]



