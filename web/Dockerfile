FROM python:3.7.6-slim

## make a local directory
RUN mkdir /pygasfrac

# set "pygasfrac" as the working directory from which CMD, RUN, ADD references
WORKDIR /pygasfrac

# copy the local requirements.txt to the /pygasfrac directory
ADD conda_requirements.txt .
ADD pip_requirements.txt .

# install the local requirements.txt
RUN pip install -r conda_requirements.txt
RUN pip install -r pip_requirements.txt

# now copy all the files in this directory to /pygasfrac directory
COPY ./ ./

# Listen to port 5000 at runtime
EXPOSE 5000

# Environment variable that sets default app to be run by Flask
ENV FLASK_APP=app

# Define our command to be run when launching the container
CMD ["flask", "run", "--host", "0.0.0.0"]
