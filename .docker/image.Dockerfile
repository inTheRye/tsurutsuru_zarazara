FROM python:3.6.5
WORKDIR /app
COPY Pipfile Makefile /app/
RUN make setup
RUN pip install pipenv && pipenv install
ADD ./ /app/
ENTRYPOINT ["make", "prdrun"]

