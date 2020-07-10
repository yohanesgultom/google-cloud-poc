# Cloud Run Firestore App

Simple PoC with Google Cloud Run + Firestore App

Dependencies:
* Python >= 3.7
* (Optional) Firebase Emulato

Setup:
1. Install dependencies `pip install -r requirements.txt`
2. Setup environment variables:
   1. Production: `GOOGLE_APPLICATION_CREDENTIALS=serviceAccount.json`
   2. Emulator: `FIRESTORE_EMULATOR_HOSTlocalhost:8000 FIRESTORE_PROJECT_ID=asomas`
3. Run api server `python main.py`

Linux example:

```
GOOGLE_APPLICATION_CREDENTIALS=serviceAccount.json python main.py
FIRESTORE_EMULATOR_HOSTlocalhost:8000 FIRESTORE_PROJECT_ID=asomas python main.py
```