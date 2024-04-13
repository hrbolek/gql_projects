
### Basic functional tests
```bash
pytest --cov-report term-missing --cov=src tests --log-cli-level=INFO -x
```

### Tests for integration
```bash
pytest tests/test_integration --log-cli-level=INFO -x
```

```bash
uvicorn main:app --env-file environment.txt --port 8000 --reload
```

### Thanks
to https://github.com/Spana21/gql_projects