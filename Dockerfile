#######################
# Base settings
#######################

# set base image (host OS)
FROM python:3.8
# FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7

# Set environment variables
ENV STATIC_URL /static
ENV STATIC_PATH /app/static

#######################
# Install dependencies
#######################

# set the working directory in the container
WORKDIR /Imotion

# Get model from online folder first
RUN pip install gdown
RUN gdown https://drive.google.com/uc?id=1MvEBUqFCDflL-Y8TllzYUe_-rivb8bmF \
    && mkdir -p ./server/checkpoints/ \
    && mv best_model.pt ./server/checkpoints/best_model.pt

# install artemis dependencies first
COPY artemis/ ./artemis/
RUN pip install -e ./artemis/

# install Imotion dependencies
COPY setup.py ./
RUN pip install -e .

# Install corpora
RUN python -m textblob.download_corpora

# Cold run the files, because some packages load additional model data
# COPY app/ ./app/
COPY server/ ./server/
RUN python -m server.image_captioning

# Copy all other files over
COPY . .

#######################
# Expose program
#######################

# command to run on container start
EXPOSE 5000
ENV FLASK_APP=app.py
CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0"]
