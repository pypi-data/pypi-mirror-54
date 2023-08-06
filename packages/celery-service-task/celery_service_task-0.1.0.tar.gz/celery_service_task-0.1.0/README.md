# Celery service task

Classe permettant d'implémenter une tâche pour un worker Celery spécifique

## Usage

```python
# import
from celery_service_task.task import TaskBase

# implémentation d'une tâche simple
class Task(TaskBase):
  def task(self) -> bool:
    print(self.conf) # la configuration est donnée par le worker Celery
    print(self.payload) # le payload est déjà sous forme d'un dictionnaire
    print(self.t_id) # identifiant de la transaction issue du payload



# utilisation de la class créée
t = Task(
    payload={'transaction_id': '123', 'hello': 'world'},
    conf={}
)

t.run_task() # lance la tâche si l'id de transaction n'est pas déjà enregistré 
```

