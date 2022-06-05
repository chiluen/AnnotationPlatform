# Steps in initialize BigTable in GCP

(can be done by console or gcp shell)

## create project and bigtable instance on gcp

1. build project on GCP

2. build BigTable instance in the project\
   [Create an instance  |  Cloud Bigtable Documentation  |  Google Cloud](https://cloud.google.com/bigtable/docs/creating-instance)

   1. select region and zone

   2. select mode for allocation resources (I use automatic here)

## Install gcloud and cbt

[cbt tool overview  |  Cloud Bigtable Documentation  |  Google Cloud](https://cloud.google.com/bigtable/docs/cbt-overview)

## using gcloud in shell

[Initializing the gcloud CLI  |  Google Cloud CLI Documentation](https://cloud.google.com/sdk/docs/initializing)

1. [ ] `gcloud init`

2. [ ] `gcloud auth login yshuang.11041994@gmail.com —no-browser`

   1. [ ] paste back the return output

3. `gcloud config set project PROJECT_ID`

## Enable cbt (starts from here is enough)

[Quickstart: Create an instance and write data with the cbt CLI  |  Cloud Bigtable Documentation  |  Google Cloud](https://cloud.google.com/bigtable/docs/create-instance-write-data-cbt-cli)

1. select project

2. enable bigtable API

3. create service account (IAM)

   1. name

   2. owner

4. click the service account

5. click “keys”

6. add new key

7. download JSON file

8. connect to the instance in the shell/container

   1. prepare `~/.cbtrc`

      ```python
      project = final-annotation-352116
      instance = final-annotation
      ```

   2. export GOOGLE_APPLICATION_CREDENTIALS\=/home/gcp-service-account-file.json

## Create tables and schema

```shell
python3 schema_bigtable.py
```

## Create Account

## Upload file