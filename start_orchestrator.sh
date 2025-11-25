#!/usr/bin/env bash
cd /opt/vision_model
source venv/bin/activate
cd orchestrator
uvicorn main:app --host 0.0.0.0 --port 8080

