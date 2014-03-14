
#### Right click → Save to cloud → Permalink on your clipboard!

Are you geek enough to save images on the web to your cloud 
storage account before sharing on Twitter? Cool, I made something
for you. You will install a web server, get a cloud storage from
Azure or AWS S3 and then grab a [Chrome extension][chrome-ext]
to **generate permanent links on the web that could last 20 years!**

This is the web server part of for Permalinker, a Python web 
application exposing an API to upload links. Uses Flask web microframework.

This app is **ready to deploy on Heroku**, however, you can run this
anywhere you'd like if you have your own hosting space.

![](http://i.imgur.com/LY5rUOE.png) 

![](http://i.imgur.com/cmGM926.png)

### Datastores

Supported datastores at the moment:

* [**Windows Azure** Blob Storage Service](http://www.windowsazure.com/en-us/documentation/services/storage/) — [see below][cfg-azure] for configuration
* [**Amazon Web Services** Simple Storage Service (S3)](http://aws.amazon.com/s3/) — [see below][cfg-s3] for configuration

(*hackers, feel free to provide implementations for other cloud storages!*)

### Deploying service to Heroku

Sign up for a free [Heroku account](http://heroku.com) and get
[Heroku Toolbelt](https://toolbelt.heroku.com/) on your machine.

Open a terminal window and navigate to `permalink/` folder you checked out
from Github in the previous step. Create application:

    $ heroku apps:create
    Creating vast-atoll-8883... done, stack is cedar
    http://vast-atoll-8883.herokuapp.com/ | git@heroku.com:vast-atoll-8883.git

Your application URL will be the one above. Push the application package to
Heroku:

    git push heroku master

If the command succeeds with a message like the following your app 
is now deployed to Heroku at specified URL:

    ...
    -----> Compressing... done, 31.5MB
    -----> Launching... done, v3
    http://vast-atoll-8883.herokuapp.com/ deployed to Heroku

If you navigate to the URL you got, you will probably get an application error.
This is because you have not set environment variables for Heroku application.
Here's how to set environment variables for a configuration using Azure Storage:

    heroku config:set STORAGE=azure
    heroku config:set AZURE_CONTAINER=testcontainer
    heroku config:set AZURE_ACCOUNT_NAME=ahmet
    heroku config:set AZURE_ACCOUNT_KEY=00000000000000000000000000

Try navigating to URL again, if you are not seeing "Application Error", you
are good! Otherwise run `heroku logs -t` to see logs and troubleshoot.

### Configuring for Windows Azure 

Make sure you have a Windows Azure account. Read this tutorial on [How to create storage account on Windows Azure](http://www.windowsazure.com/en-us/documentation/articles/storage-create-storage-account/)

At the end, click "Manage Keys" for your subscription. Using the account name and one of account keys, configure your heroku service as follows


    heroku config:set STORAGE=azure
    heroku config:set AZURE_CONTAINER=give-a-container-name
    heroku config:set AZURE_ACCOUNT_NAME=your-account
    heroku config:set AZURE_ACCOUNT_KEY=your-storage-account-key

Please note:

* The blobs uploaded to the container will be public, however people cannot list blobs in that container.
* Container names can be 3 to 64 lowercase letters or numbers or dash (-) char. ([read more](http://msdn.microsoft.com/en-us/library/windowsazure/dd135715.aspx))


### Configuring for AWS S3 

Make sure you have a Amazon Web Services account. Read this tutorial on [Getting your Acccess ID and Secret Access Key](http://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSGettingStartedGuide/AWSCredentials.html).

Configure your heroku service as follows

    heroku config:set STORAGE=s3
    heroku config:set AWS_ACCESS_KEY_ID=your-access-key-id
    heroku config:set AWS_SECRET_ACCESS_KEY=your-secret-access-key
    heroku config:set AWS_S3_BUCKET=pick-a-bucket-name

Please note:

* The **bucket name should be universally unique**. So come up with something creative (e.g I am using `alp-perma`).
* The keys (files) uploaded will be public to anyone. However people cannot list keys in the specified bucket.

--------------------

### Getting the Chrome Extension

After setting up the service, [**install the Google Chrome extension**][chrome-ext].

Go to Options of the extension, put the API base URL as `http://{{your-hostname}}/api/1`. For example if yours is "flying-duck-1234.herokupp.com", put down `http://flying-duck-1234.herokuapp.com/api/1`. 
	
Hit "Save & Close". Browse the web. Find an image. Right click. Hit **Permalink on cloud!**, profit!


![*Link copied! Will it stay there **for another 20 years?** *](http://i.imgur.com/FE0uP3P.png)


--------------------

### Running the service locally for development

(I highly recommend doing this on Linux or Mac OS X environment.)

Make sure you have `pip` installed on your machine (`sudo easy_install pip`).

I recommend using `virtualenvwrapper` to keep dependencies organized

    mkvirtualenv permalinker
    git clone git@github.com:ahmetalpbalkan/permalinker.git
    cd permalinker
    workon permalinker

Install dependencies:

    pip install -r requirements.txt

Set environment variables (example is for Azure Storage, see S3 samples [above][cfg-s3])

    export STORAGE=azure
    export AZURE_CONTAINER=testcontainer
    export AZURE_ACCOUNT_NAME=ahmet
    export AZURE_ACCOUNT_KEY=00000000000000000000000000

Start the web application

    $ python runserver.py
    * Running on http://0.0.0.0:5000/

Navigate to URL shown above.



[chrome-ext]: https://chrome.google.com/webstore/detail/gbojiplhnhbhfhhkjacacijiglpmcpbh
[cfg-azure]: https://github.com/ahmetalpbalkan/permalinker/tree/dev#configuring-for-windows-azure
[cfg-s3]: https://github.com/ahmetalpbalkan/permalinker/tree/dev#configuring-for-aws-s3
