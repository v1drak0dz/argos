# Backend To-Do List

A ordem abaixo é importante.
Tem coisa que parece “mais legal”, mas não é prioridade arquitetural.

---

# Fase 1 — Core operacional

## 1. Listagem de jobs

### Endpoint

```http
GET /jobs
```

### Precisa retornar:

- id
- title
- status
- progress
- current_step
- created_at
- finished_at
- worker_id
- artifact_count

### Objetivo

Popular dashboard principal.

---

## 2. Paginação

### Query params

```http
GET /jobs?page=1&limit=20
```

### Problema que resolve

Sem isso:

```text
1000 jobs = frontend morre
```

---

## 3. Busca textual

### Query params

```http
GET /jobs?search=amazon
```

### Buscar em:

- title
- description
- keywords_json

### Objetivo

Transformar jobs em entidades pesquisáveis.

---

## 4. Filtros

### Exemplos

```http
GET /jobs?status=running
GET /jobs?type=scrape
GET /jobs?keyword=gpu
```

### Objetivo

Dashboard operacional real.

---

## 5. Ordenação

### Exemplos

```http
GET /jobs?sort=created_at:desc
GET /jobs?sort=progress:asc
```

---

# Fase 2 — Controle operacional

## 6. Cancelamento de jobs

### Endpoint

```http
POST /jobs/<id>/cancel
```

### Backend precisa:

- marcar status = cancelled
- sinalizar worker
- interromper pipeline

### Isso exige:

```python
threading.Event()
```

---

## 7. Retry job

### Endpoint

```http
POST /jobs/<id>/retry
```

### Fluxo

- pega parâmetros antigos
- cria novo job
- reaproveita config

---

## 8. Clone job

### Endpoint

```http
POST /jobs/<id>/clone
```

### Objetivo

Criar novo draft baseado no antigo.

Muito útil.

---

## 9. Delete job

### Endpoint

```http
DELETE /jobs/<id>
```

### Deve:

- remover artifacts
- remover logs
- remover registros

---

# Fase 3 — Artifacts

## 10. Artifact metadata endpoint

### Endpoint

```http
GET /artifacts/<id>
```

### Retorna:

- nome
- tamanho
- tipo
- criado_em

---

## 11. Preview de artifact

### Endpoint

```http
GET /artifacts/<id>/preview
```

### Exemplo

- preview JSON
- primeiras linhas CSV
- logs recentes

---

## 12. ZIP download

### Endpoint

```http
GET /jobs/<id>/download
```

### Gera:

```text
job_145.zip
```

Com:

- csv
- json
- logs

---

## 13. Cleanup automático

### Problema

Artifacts infinitos.

### Solução

Policy:

```text
delete after X days
```

---

# Fase 4 — Logs e observabilidade

## 14. Logs paginados

### Endpoint

```http
GET /jobs/<id>/logs?page=1
```

---

## 15. Levels de log reais

### Adicionar:

- INFO
- WARNING
- ERROR
- DEBUG

---

## 16. Heartbeat real

Hoje:

```python
fake values
```

### Ideal

Usar:

```python
psutil
```

Pra:

- CPU
- RAM
- threads
- IO

---

## 17. Duração do job

### Calcular:

```text
finished_at - started_at
```

Muito importante pro dashboard.

---

## 18. Metrics endpoint

### Endpoint

```http
GET /metrics
```

### Retorna:

- running jobs
- queued jobs
- completed today
- failed today
- avg duration

---

# Fase 5 — Pipeline engine

## 19. Pipeline real por steps

Hoje:

```python
run_pipeline()
```

### Evoluir para:

```python
steps = [
  scrape_step,
  filter_step,
  save_step
]
```

---

## 20. Step registry

### Objetivo

Pipelines dinâmicos.

Exemplo:

```json
{
  "pipeline": ["scrape", "filter", "export_csv"]
}
```

---

## 21. Plugin architecture

Permitir:

```text
novos scrapers sem alterar core
```

---

## 22. Worker capabilities

Exemplo:

```text
worker-1 suporta playwright
worker-2 suporta selenium
```

---

# Fase 6 — Robustez

## 23. Persistência da fila

Hoje:

```text
restart = perde fila
```

### Solução

Reidratar jobs queued/running no startup.

---

## 24. Recovery de jobs interrompidos

No startup:

```text
running -> failed/recoverable
```

---

## 25. Timeout de jobs

### Exemplo

```text
max_duration = 10min
```

---

## 26. Retry automático

### Exemplo

```text
retry_count < 3
```

---

## 27. Dead jobs detection

Detectar:

```text
worker travado
```

---

# Fase 7 — Segurança

## 28. API keys

---

## 29. Auth

---

## 30. Rate limiting

---

## 31. Path sanitization

CRÍTICO em:

```python
send_file()
```

---

# Fase 8 — Performance

## 32. Trocar queue.Queue

Por:

```text
Redis
```

MAS:

```text
não agora
```

---

## 33. Trocar SQLite

Somente quando:

```text
concorrência REAL
```

---

## 34. Async workers

Hoje:

```text
threads
```

Depois:

```text
asyncio
multiprocessing
```

---

# Fase 9 — Features de produto

## 35. Job templates

Salvar configs reutilizáveis.

---

## 36. Schedules

### Exemplo

```text
run every day at 9am
```

---

## 37. Favorites

---

## 38. Tags reais

Tabela separada.

---

## 39. Dashboard analytics

- success rate
- avg duration
- most used source
- artifact growth

---

# O que eu faria AGORA

A prioridade correta seria:

## PRIORIDADE 1

- GET /jobs
- paginação
- busca
- filtros

---

## PRIORIDADE 2

- cancelamento
- retry
- clone

---

## PRIORIDADE 3

- preview artifacts
- zip download

---

## PRIORIDADE 4

- persistência/recovery da fila

---

# O erro MAIS perigoso agora

Você provavelmente vai querer:

```text
microservices
redis
rabbitmq
docker swarm
kubernetes
```

Muito cedo.

Seu gargalo HOJE:

```text
não é infraestrutura
```

É:

```text
maturidade operacional do produto
```

Você ainda está construindo:

- lifecycle
- UX operacional
- observabilidade
- persistência
- controle

Essas coisas valem MUITO mais agora do que escalar infra.
