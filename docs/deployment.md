# Deployment

## API + Workers + MLflow
```
docker compose up -d redis worker api mlflow
```

## Docs
```
mkdocs gh-deploy --force
```

## Docker images (optional)
- You can build and publish CLI/API images and reference in docker-compose.yml for portability.