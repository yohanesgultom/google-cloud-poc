# app-engine-microservices

Simple microservices with [Google Standard App Engine](https://cloud.google.com/appengine) and [API Gateway](https://cloud.google.com/api-gateway) 

> Google API Gateway is still in **beta**. Use it with precaution

## Prerequisites

* [Google Cloud Project](https://cloud.google.com/free)
* [Bash shell](https://en.wikipedia.org/wiki/Bash_(Unix_shell)) 
* [gcloud](https://cloud.google.com/sdk/gcloud) >= 320
* Google App Engine enabled (default app deployed)
* Google PubSub enabled
* [sed](https://www.gnu.org/software/sed/manual/sed.html) (optional, to replace all Swagger/OpenAPI 2.0 spec file)

## Overview

There are 3 microservices available: 

* **alpha**: Flask-based. Has a `POST /action` endpoint that accepts `url` field invoke `HTTP GET` to it

* **beta**: Flask-based. Has a `POST /action` endpoint that accepts `url` field invoke `HTTP GET` to it. Used to test internal communication between services (alpha-beta) using plain HTTP calls

* **gamma**: Django-based. Test PubSub communication between services (in this case between its own endpoints)

## Deploy

### App Engine

Deploy each services from their subdirectory:

```
cd alpha-service
gcloud app deploy
cd ../beta-service
gcloud app deploy
cd ../gamma-service
gcloud app deploy
```

### API Gateway

Generate Swagger/OpenAPI 2.0 spec `openapi2-spec.yaml` from `openapi2-spec.template.yaml` by replacing `{PROJECT_ID}` with your project id (example below uses `sed`, but feel free to use other tools):

```
export PROJECT_ID=your-project-id
cd gateway-api
sed "s/{PROJECT_ID}/$PROJECT_ID/g" openapi2-spec.template.yaml > openapi2-spec.yaml 
```

Enable required services (if you haven't):

```
gcloud services enable apigateway.googleapis.com
gcloud services enable servicemanagement.googleapis.com
gcloud services enable servicecontrol.googleapis.com
```


Create API Gateway instance:

```
export API_ID="$PROJECT_ID-api"
gcloud components install beta --quiet
gcloud beta api-gateway apis create $API_ID --project=$PROJECT_ID
```

Create config instance from spec `openapi2-spec.yaml` (using default App Engine service account):

```
export NEW_CONFIG_ID="$API_ID-config-$(date +"%Y%m%d%H%M%S")"
gcloud beta api-gateway api-configs create $NEW_CONFIG_ID --api=$API_ID --openapi-spec=openapi2-spec.yaml --project=$PROJECT_ID --backend-auth-service-account=$PROJECT_ID@appspot.gserviceaccount.com
```

Enable service:

```
export SERVICE_ID=$(gcloud beta api-gateway apis describe $API_ID --project=$PROJECT_ID | grep -Po '(?<=managedService: ).*')
gcloud services enable $SERVICE_ID
```

Finally, create the gateway using the deployed config:

```
export GATEWAY_ID="$API_ID-gateway"
export PROJECT_LOCATION=us-central1 
gcloud beta api-gateway gateways create $GATEWAY_ID --api=$API_ID --api-config=$NEW_CONFIG_ID --location=$PROJECT_LOCATION --project=$PROJECT_ID
```

Get the Gateway URL (`defaultHostname`):

```
export GATEWAY_URL=$(gcloud beta api-gateway gateways describe $GATEWAY_ID --location=$PROJECT_LOCATION --project=$PROJECT_ID | grep -Po '(?<=defaultHostname: ).*$') 
```

Access one of the path defined to test it:

```
curl https://$GATEWAY_URL/alpha
```

### PubSub

The `gamma` service can be used to test PubSub service. In order to use it, we need to create `hello` topic, create `gamma-action-hello` subscription, and grant access to a PubSub service account `service-${PROJECT_ID}@gcp-sa-pubsub.iam.gserviceaccount.com` to generate OIDC token:

```
export PROJECT_ID=your-project-id
export PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID | grep -Po "(?<=projectNumber: ')\d+(?=')")


gcloud pubsub topics create hello

gcloud pubsub subscriptions create gamma-action-hello --topic=hello --push-auth-service-account=$PROJECT_ID@appspot.gserviceaccount.com --push-endpoint=https://gamma-dot-$PROJECT_ID.appspot.com/action -expiration-period=never

gcloud projects add-iam-policy-binding ${PROJECT_ID} --member="serviceAccount:service-${PROJECT_NUMBER}@gcp-sa-pubsub.iam.gserviceaccount.com" --role='roles/iam.serviceAccountTokenCreator'
```

> Actually the usage of `push-auth-service` and granting `roles/iam.serviceAccountTokenCreator` are optional for this case. It will only be required when pushing to a secure endpoint which is actually very common in real-world application 

Once done, endpoints can be used:

**Publish message**

This endpoint will publish "hello world!" to `hello` topic:

```
curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" -d '{"message": "hello world!"}' "https://$GATEWAY_URL/gamma/publish"
```

**List messages**

This endpoint will display list of messages captured by `POST /action` which is triggered by `gamma-action-hello` subscription. You used find "hello world" after few seconds:

```
curl -i -X GET -H "Accept:application/json" "https://$GATEWAY_URL/gamma/messages"
```

## References

* https://cloud.google.com/api-gateway/docs/quickstart