# Sanku Backend

## Setup

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

Made by [Sankalpa](https://sankalpa.info.np) with ❤️