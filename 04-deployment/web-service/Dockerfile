FROM python:3.11-slim

RUN pip install -U pip
RUN pip install pipenv 

WORKDIR /app

COPY [ "Pipfile", "Pipfile.lock", "./" ]

# Install the dependencies from Pipfile.lock
RUN pipenv install --system --deploy --ignore-pipfile --verbose

COPY [ "predict.py", "lin_reg.bin", "./" ]

EXPOSE 9696

# If gunicorn is installed production
# ENTRYPOINT [ "gunicorn", "--bind=0.0.0.0:9696", "predict:app" ]

# running on flask development
# Set environment variables
ENV FLASK_APP=predict.py
ENV FLASK_ENV=development

# Run the Flask development server
ENTRYPOINT ["flask", "run", "--host=0.0.0.0", "--port=9696"]