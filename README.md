setting up infra

goto infra dir
```bash
cd infra
```

set terraform environment variables
```bash
export TF_VAR_aws_access_key='<aws-access-key>'
export TF_VAR_aws_access_secret='<aws-secret-access-key>'
```

Open bash terminal in a running container
```bash
docker compose exec <coontainer_name> bash
```