FROM python:alpine3.10

COPY . /tmp

WORKDIR /tmp

RUN pip install pipenv

# Because of setuptools_scm in setup.py
RUN apk add --no-cache git

# Use the Pipfile.lock ONLY
RUN pipenv install --ignore-pipfile

# Run the application inside the virtualenv
CMD ["pipenv", "run", "python" , "app/run.py"]
