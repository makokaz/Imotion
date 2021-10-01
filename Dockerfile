# set base image (host OS)
FROM python:3.8
# FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7

# Set environment variables
ENV STATIC_URL /static
ENV STATIC_PATH /app/static

# set the working directory in the container
WORKDIR /Imotion

# copy the dependencies file to the working directory
COPY artemis/ ./artemis/
COPY setup.py ./

# Install dependencies
RUN pip install -e ./artemis/
RUN pip install -e .
RUN pip install gdown
RUN python -m textblob.download_corpora

# Get model from online folder
RUN gdown https://drive.google.com/uc?id=1MvEBUqFCDflL-Y8TllzYUe_-rivb8bmF \
    && mkdir -p ./server/checkpoints/ \
    && mv best_model.pt ./server/checkpoints/best_model.pt

# Copy all other files over
COPY . .

# command to run on container start
EXPOSE 5000
ENV FLASK_APP=app.py
CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0"]
