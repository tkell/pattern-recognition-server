FROM tiangolo/uwsgi-nginx-flask:python3.7

LABEL maintainer="Thor Kell <thor@tide-pool.ca>"

COPY ./app /app
WORKDIR /app
RUN pip3 install -r requirements.txt

# Move the base entrypoint to reuse it
#RUN mv /entrypoint.sh /uwsgi-nginx-entrypoint.sh
## Copy the entrypoint that will generate Nginx additional configs
#COPY entrypoint.sh /entrypoint.sh
#RUN chmod +x /entrypoint.sh
#
#ENTRYPOINT ["/entrypoint.sh"]
#
## I think we need this one!  But are we starting the server in this way?
## Run the start script provided by the parent image tiangolo/uwsgi-nginx.
## It will check for an /app/prestart.sh script (e.g. for migrations)
## And then will start Supervisor, which in turn will start Nginx and uWSGI
#CMD ["/start.sh"]
