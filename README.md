# OpenGate API HTTP/MQTT examples

## Quick start

Install Python dependencies using `pip`:

```bash
pip install -r requirements.txt
```

Rename `env_template` to `.env`. This file stores the api key to authorize your requests and messages.

```bash
mv env_template .env
```

## Backup this project

```bash
tar --exclude='.*' --exclude='__pycache__' -cvfz opengate-python-examples.tgz opengate-python-examples
```
