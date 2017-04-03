# Example of consuming Cloud Pub/Sub message (#GaeStandardPython)

This example was developed using Python and just consume [Cloud Pub/Sub](https://cloud.google.com/pubsub/docs/) msg of same GCP Project.

We are using [Pull Subscriber](https://cloud.google.com/pubsub/docs/pull)



To include some messages in the topic you [can use the GCloud](https://cloud.google.com/pubsub/docs/quickstart-cli):

```
gcloud init
gcloud components install beta
gcloud beta pubsub topics create <topic name>
gcloud beta pubsub subscriptions create --topic <topic name> <subscription name>
gcloud beta pubsub topics publish <topic name> <MSG>
```

**Example**:

```
gcloud init
gcloud components install beta
gcloud beta pubsub topics create myTopic
gcloud beta pubsub subscriptions create --topic myTopic mySubscription
gcloud beta pubsub topics publish myTopic "Hello"
```



## ENVIRONMENT SETUP

### Requirements
* Python 2.7

### Install Google Cloud SDK
Download the latest version of the SDK here: [Google Cloud SDK](https://cloud.google.com/sdk/)
After downloading the file, extract the content and run the **install.sh** script:
```
./google-cloud-sdk/install.sh
```


Then install the App Engine Python component:
```
gcloud components install app-engine-python
```

### Install python dependencies
In the project's root folder:
```
pip install -r requirements.txt -t lib
```

### Local runserver
In the project's root folder:
```
dev_appserver.py app.yaml
```
You should have your server up and running at [localhost:8080](http://localhost:8080).
App Engine admin server is at [localhost:8000](http://localhost:8000).


### Deployment

Then to deploy the application itself:
```
gcloud app deploy --<GCP PROJECT> -v <VERSION NAME> --no-promote app.yaml
```

