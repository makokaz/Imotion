# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /Imotion

# copy the dependencies file to the working directory
COPY requirements.txt ./
COPY artemis/ ./artemis/

# Install dependencies
RUN pip install -e ./artemis/
RUN pip install -r requirements.txt
RUN pip install gdown

# Copy all other files over
COPY . .

# Get model from online folder
RUN gdown https://drive.google.com/uc?id=1MvEBUqFCDflL-Y8TllzYUe_-rivb8bmF && mkdir -p ./server/checkpoints/ && mv best_model.pt ./server/checkpoints/best_model.pt

# Install stopwords, textblob
RUN python ./install.py
RUN python -m textblob.download_corpora

# command to run on container start
CMD [ "python", "./app.py" ]
