# Cloud Run Firestore App

Simple PoC with Google Cloud Run + Firestore App

Dependencies:
* Python >= 3.7
* (Optional) Firebase Emulator

Setup:
1. Install dependencies `pip install -r requirements.txt`
2. Setup environment variables:
   1. Production: `GOOGLE_APPLICATION_CREDENTIALS=serviceAccount.json`
   2. Emulator: `FIRESTORE_EMULATOR_HOST=localhost:8000 FIRESTORE_PROJECT_ID=asomas`
3. Run api server `python main.py`

Linux example:
```
FIRESTORE_EMULATOR_HOST=localhost:8000 FIRESTORE_PROJECT_ID=asomas python main.py
```

Gunicorn example:
```
FIRESTORE_EMULATOR_HOST=localhost:8000 FIRESTORE_PROJECT_ID=asomas gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
```

Run using docker (put service account JSON `serviceAccount.json` in same directory before build):
```
docker build -t cloud-run-firestore .
docker run -e GOOGLE_APPLICATION_CREDENTIALS=serviceAccount.json -e PORT=8080 -p 8080:8080 cloud-run-firestore
```

Deploying on Cloud Run (from Cloud Shell):
```
gcloud builds submit --tag gcr.io/$DEVSHELL_PROJECT_ID/cloud-run-firestore
gcloud run deploy --image gcr.io/$DEVSHELL_PROJECT_ID/cloud-run-firestore --platform managed
```