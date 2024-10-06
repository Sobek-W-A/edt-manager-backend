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

# Instruction informs Docker that the container listens on port 80
EXPOSE 8000

# Now we just want to our WORKDIR to be /build/app for simplicity
# We could skip this part and then type
# python -m uvicorn main.app:app ... below
WORKDIR /build/app

# This command runs our uvicorn server
# See Troubleshoots to understand why we need to type in --host 0.0.0.0 and --port 8000
CMD python -m uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

