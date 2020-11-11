# Cloud Run SSE

Simple SSE PoC with Google Cloud Run.

> Basically it will deploy a flask server with a single html page (in root path). When you access the cloud run URL, you will see a page with Start and Clear button. When opened, this page will automatically listen to "/listen" endpoint. When you click Start button, it will call "/start" endpoint that will trigger a thread that push message to all listeners. So you will see messages printed in the page. The Clear button is just to clear the printed messages.

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

Open the `Service URL` in browser that support `EventSource` (SSE client) to see it in action