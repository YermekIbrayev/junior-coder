# How to Check Orchestrator Logs

## Log Files Location

```bash
/opt/vision_model/orchestrator.log         # Main orchestrator log
/opt/vision_model/orchestrator_restart.log  # Last restart log
```

## Quick Commands

### 1. View Recent Logs (Last 50 lines)
```bash
tail -50 /opt/vision_model/orchestrator.log
```

### 2. Follow Logs in Real-Time (like `tail -f`)
```bash
tail -f /opt/vision_model/orchestrator.log
```
Press `Ctrl+C` to stop following

### 3. View All Logs
```bash
cat /opt/vision_model/orchestrator.log
```

### 4. Search Logs for Errors
```bash
grep -i "error\|exception\|traceback" /opt/vision_model/orchestrator.log
```

### 5. Search for Specific Request
```bash
# Find logs related to a specific user
grep "test-user-001" /opt/vision_model/orchestrator.log

# Find all POST requests
grep "POST /v1/chat/completions" /opt/vision_model/orchestrator.log
```

### 6. View Logs with Timestamps
```bash
tail -100 /opt/vision_model/orchestrator.log | grep "INFO\|ERROR"
```

### 7. Check Current Orchestrator Process
```bash
ps aux | grep uvicorn | grep -v grep
```

### 8. View Logs from Background Process
If orchestrator is running in background:
```bash
# Get the shell ID from the startup message, then:
# (Already used in our session: 586d1e)
```

## Log Levels

The orchestrator logs these levels:
- **INFO**: Normal operations (requests, startups, health checks)
- **WARNING**: Non-critical issues (memory errors, fallback usage)
- **ERROR**: Errors that need attention (service failures, exceptions)

## Common Log Patterns

### Successful Request
```
INFO: 127.0.0.1:51372 - "POST /v1/chat/completions HTTP/1.1" 200 OK
```

### Error
```
INFO: 127.0.0.1:46320 - "POST /v1/chat/completions HTTP/1.1" 500 Internal Server Error
```

### Startup
```
✓ Mem0 memory client initialized (collection: agent_memories)
INFO: Application startup complete.
INFO: Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
```

## Useful One-Liners

### Last 10 errors
```bash
grep -i "error" /opt/vision_model/orchestrator.log | tail -10
```

### Count requests by status code
```bash
grep "POST /v1/chat/completions" /opt/vision_model/orchestrator.log | grep -o "[0-9]\{3\} OK\|[0-9]\{3\} Internal" | sort | uniq -c
```

### Show only memory-related logs
```bash
grep -i "memory\|mem0" /opt/vision_model/orchestrator.log
```

### Show sequential thinking activity
```bash
grep -i "thinking\|reasoning" /opt/vision_model/orchestrator.log
```

### Show routing decisions
```bash
grep -i "route\|routing" /opt/vision_model/orchestrator.log
```

## Advanced: Filter by Time Range

### Last 5 minutes
```bash
tail -1000 /opt/vision_model/orchestrator.log | grep "$(date +%H:%M -d '5 minutes ago')"
```

### Specific hour
```bash
grep "05:55" /opt/vision_model/orchestrator.log
```

## Rotate Logs (Manual)

If log file gets too large:
```bash
# Backup current log
mv /opt/vision_model/orchestrator.log /opt/vision_model/orchestrator.log.$(date +%Y%m%d-%H%M%S)

# Restart orchestrator to create new log
kill $(ps aux | grep uvicorn | grep -v grep | awk '{print $2}')
cd /opt/vision_model && ./start_orchestrator.sh > orchestrator.log 2>&1 &
```

## Docker Logs (if using docker-compose)

If you were using docker-compose:
```bash
docker-compose logs -f orchestrator        # Follow logs
docker-compose logs --tail=100 orchestrator # Last 100 lines
docker-compose logs orchestrator | grep ERROR # Errors only
```

## Debug Mode

To enable verbose logging, edit `orchestrator/core/config.py`:
```python
LOG_LEVEL: str = "DEBUG"  # Change from "INFO"
```

Then restart orchestrator.
