from app.aws.ecr import ECR

class Container:
    
    def __init__(self):
        pass

    def push(self, app, services):
        ECR().check_and_create([f"{app}/{service}" for service in services])

    def release(self):
        pass
