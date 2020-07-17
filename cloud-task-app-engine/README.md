# cloud-task-app-engine

Simple PoC to create API server in App Engine that submits a Cloud Task invoking `cloud-run-firestore` HTTP `POST /logs` endpoint (Cloud Run). Endpoints:
* `GET /`: display hello world message
* `POST /submit-task`: submit Cloud Task that invoke `cloud-run-firestore` HTTP `POST /logs`

> This project assume [cloud-run-firestore](../cloud-run-firestore) already deployed properly as a Cloud Run instance

Running in local (Linux):

```
export GOOGLE_APPLICATION_CREDENTIALS=$(pwd)/serviceAccount.json 
pip install -r requirements.txt
python main.py
```

Setup and deploy:

```
pip install -r requirements.txt
gcloud app create
gcloud tasks queues create cloud-run-queue
gcloud app deploy
```