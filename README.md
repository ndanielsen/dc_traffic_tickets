DC Traffic Tickets
==============================

Looking at moving violations and parking tickets in DC.

Django with postgres + postgis plus frontend wonderfulness.

Getting Started for Local Development
------------

Set up Docker on your machine by following the [Docker Docs](https://docs.docker.com/machine/get-started/)

Once your local docker-machine is up and running:

Clone the github repo on the command line with:

`git clone git@github.com:ndanielsen/dc_traffic_tickets.git`

Move into the directory with:

`cd dc_traffic_tickets`

Build the docker image with:

'docker-compose -f dev.yml build`

This will take a few minutes...

Start django and postgres server with:

'docker-compose -f dev.yml up -d`

Check that it is running with:

`docker-compose ps`

You should see something like this:

>           Name                          Command               State           Ports          
> ---------------------------------------------------------------------------------------------
>
> dctraffictickets_django_1     /entrypoint.sh python /app ...   Up      0.0.0.0:8000->8000/tcp
>
> dctraffictickets_postgres_1   /docker-entrypoint.sh postgres   Up      5432/tcp  

#### Confirm that it is running locally by:

Take note of the ip for your local machine:

`docker-machine ip default`

Checkout the IP + ':8000' in your browser, or example ** http://192.168.99.100:8000/

#### Let's now get our database set up with:

`docker-compose -f dev.yml run django python manage.py makemigrations`

`docker-compose -f dev.yml run django python manage.py migrate`


#### Now that it's runnings, let's seed the database with sample data. This will load 100k randomly selected parking tickets to the database.

`docker-compose -f dev.yml run django python manage.py load_100k_parking_sample`


#### Let's create a superuser by so that we can checkout the site admin:

`docker-compose -f dev.yml run django python manage.py createsuperuser`

Have a look by navigating to YOUR_IP:8000/admin

#### Now that we've logged into admin, let's check out the rest api

** YOUR_IP:8000/api/v1/

Please note that for api calls the page size response is limited to 500 items, otherwise it would be very slow.

### Where do I get started? (Front end)

You'll notice on the landing page that there are numbered sandboxes pages for dataviz (or anything that you want to try out)

All front end pieces are located at in the dataviz folder.

Sandbox html pagers are located at dc_traffic_tickets/dataviz/templates

CSS and JS assets are located at dc_traffic_tickets/dataviz/static/

All templates inherit from a base template which is located:
dc_traffic_tickets/dc_traffic_tickets/templates/base.html


### Where do I get started? (Back end)

All the major backend pieces are located in dc_traffic_tickets/api/

Want to add an additional requirement?

Add as appropriate to `requirements/`  and to config/settings/ under installed apps (if necessary)

### API query filters

Example call:

http://192.168.99.100:8000/api/v1/parkingviolations/?rp_plate_state=&violation_code=&holiday=1&body_style=&ticket_date_range_start=&ticket_date_range_end=&ticket_single_date=&ticket_day_of_week=2


#### rp_plate_state

Filter by state plate

#### violation_code

Filter by violation code

#### holiday

Self reported holiday (true or false)

### body_style

Vehicle body style

### ticket_date_range_start

query start date

For example all tickets since 2014-02-01

### ticket_date_range_end

query start date

For example all tickets since 2014-03-01


### Both ticket_date_range_start and ticket_date_range_end

Date range in a period of time

ticket_date_range_start=2014-02-01&ticket_date_range_end=2014-03-01


### ticket_day_of_week

Single day of the week (1-7) starting with Monday as 1


### ticket_single_date

Data for one single day such as 2014-03-01
