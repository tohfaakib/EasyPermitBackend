FROM python:3.10-slim

LABEL version="0.0.1"

WORKDIR /home/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWEITEBYTECODE 1

RUN apt-get update && apt-get upgrade

COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the port the application will run on
EXPOSE 9000

# Define the command to run your FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["uvicorn", "main:app", "--reload"]
