# Celery service task

Classe permettant d'implémenter une tâche pour un worker Celery spécifique

## Usage

```python
# import
from celery_service_task.task import TaskBase

# implémentation d'une tâche simple
class Task(TaskBase):
  def task(self, payload: Dict[str, Any]) -> bool:
    print(self.conf) # la configuration est donnée par le worker Celery
    print(payload) # le payload est déjà sous forme d'un dictionnaire
    print(payload['transaction_id']) # identifiant de la transaction issue du payload



# Initialisation de la classe avec une configuration
t = Task(conf={'token': 'tk'})

# simulation d'un payload JSON parsé
payload={'transaction_id': '123', 'hello': 'world'}

# lance la tâche si l'id de transaction n'est pas déjà enregistré 
# Ici la tâche se lance
t.run_task(
    payload=payload,
    transaction_id=payload['transaction_id']
)

# Ici la tâche est considérée comme un replica
t.run_task(
    payload=payload,
    transaction_id=payload['transaction_id']
)
```

