# Get a python image
FROM python:3

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents to into the container at /app
ADD . /app

# Install packages in requirements.txt
RUN pip3 install -Ur requirements.txt

# Make ports open
# EXPOSE 80
# EXPOSE 8080
# EXPOSE 8000
# EXPOSE 5000

# Define env vars
ENV PYTHONPATH /app/src/
ENV FLASK_APP /app/src/flaskapp/pokerdb_flask.py

# App start
# CMD flask run --host=0.0.0.0
CMD gunicorn -w 8 -b 0.0.0.0:$PORT pokerdb_flask:app --chdir src/flaskapp
