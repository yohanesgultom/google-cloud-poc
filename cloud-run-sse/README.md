# Cloud Run SSE

Simple SSE PoC with Google Cloud Run

## Setup

Clone this repo and run following commands:

> Populate $DEVSHELL_PROJECT_ID with your project ID if you are not using Cloud Shell

```
gcloud builds submit --tag gcr.io/$DEVSHELL_PROJECT_ID/cloud-run-sse
gcloud run deploy --image gcr.io/$DEVSHELL_PROJECT_ID/cloud-run-sse --platform managed --allow-unauthenticated
```
Pay attention on the messages in the console as sometimes the build/deploy process prompt for more information (depends on your project's configuration) and need to be retried due to temporary failure (eg. due to network or other issue). When all processes run succesfully, you will see message like this:

```
Service [cloud-run-sse] revision [cloud-run-sse-00001-bov] has been deployed and is serving 100 percent of traffic.                        
Service URL: https://cloud-run-sse-6v5ifmf2ma-uc.a.run.app
```
