# NS - NASA Data System

Automated NASA data collection and processing on Google Cloud Platform.

## Features

- Collects NASA API data automatically
- Event-driven architecture
- Scheduled data processing
- Cloud-based storage and monitoring

## Setup

```bash
./activate.sh
pip install -e packages/
```

## Deploy

```bash
./scripts/deploy_one.sh
```

## Monitor

```bash
gcloud functions logs read ns-func-apod --region=us-central1
```
