## permalinker: Right click → Save to cloud → Permalink on your clipboard!

This is web server part of for Permalinker. This is a Python web
application exposing an API to upload links.

This app is ready to deploy to Heroku, however, you can run
anywhere if you'd like.

### Datastores

Available datastores are:

* [Azure Blob Storage Service](http://www.windowsazure.com/en-us/documentation/services/storage/)


### Running locally on development environment

Make sure you have `pip` installed on your machine (`sudo easy_install pip`).

I recommend using `virtualenvwrapper` to keep dependencies organized

    mkvirtualenv permalinker
    git clone git@github.com:ahmetalpbalkan/permalinker.git
    cd permalinker
    workon permalinker

Install dependencies:

    pip install -r requirements.txt

Set environment variables (example for Azure Storage:)

    export STORAGE=azure
    export AZURE_CONTAINER=testcontainer
    export AZURE_ACCOUNT_NAME=ahmet
    export AZURE_ACCOUNT_KEY=00000000000000000000000000

Start the web application

    $ python runserver.py
    * Running on http://0.0.0.0:5000/

Navigate to URL shown above.

### Deploying a Permalink server to Heroku

Sign up for a free [Heroku account](http://heroku.com) and get
[Heroku Toolbelt](https://toolbelt.heroku.com/) on your machine.

Open a terminal window and navigate to `permalink/` folder you checked out
from Github in the previous step. Create application:

    $ heroku apps:create
    Creating vast-atoll-8883... done, stack is cedar
    http://vast-atoll-8883.herokuapp.com/ | git@heroku.com:vast-atoll-8883.git

Your application URL will be the one above. Push the application package to
Heroku: