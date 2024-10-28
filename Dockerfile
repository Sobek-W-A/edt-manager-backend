# A Dockerfile is a text document that contains all the commands
# a user could call on the command line to assemble an image.

# Our Debian with python is now installed.
# Imagine we have folders /sys, /tmp, /bin etc. there
# like we would install this system on our laptop.

FROM python:3.12

# We create folder named build for our stuff.
RUN mkdir build

# Basic WORKDIR is just /
# Now we just want to our WORKDIR to be /build
WORKDIR /build

# OK, now we pip install our requirements
COPY ./app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# We copy our files (files from .dockerignore are ignored)
# to the WORKDIR
COPY ./app ./app

# Instruction informs Docker that the container listens on port 8000
EXPOSE 8000

# Adding a wait command to wait for other containers to start.
ENV WAIT_VERSION 2.11.0
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

# This command runs our uvicorn server
CMD python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
