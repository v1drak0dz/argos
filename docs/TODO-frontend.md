# Frontend To-Do List

A ordem importa MUITO.
Tem coisa que parece “mais bonita”, mas não destrava o produto.

---

# Fase 1 — Base funcional

## 1. Estrutura JS do dashboard

Criar:

```text id="tw48ae"
/assets/js/
```

Separar:

```text id="u03l4w"
api.js
dashboard.js
jobs.js
sse.js
modals.js
utils.js
```

---

# 2. Consumir GET /jobs

## Objetivo

Popular dashboard dinamicamente.

Hoje:

```text id="fkh2ju"
cards hardcoded
```

Precisa virar:

```javascript id="x0lsju"
fetch("/jobs");
```

---

# 3. Renderização dinâmica de jobs

Criar:

```javascript id="jlwm1r"
renderJobCard(job);
```

Responsável por:

- status
- progress
- worker
- tags
- runtime
- artifacts

---

# 4. Remover HTML hardcoded

Seu HTML atual:

```text id="jlwm8k"
vira template vazio
```

Exemplo:

```html id="7jlwm6"
<div id="jobs-container"></div>
```

---

# 5. Atualização automática inicial

No load:

```javascript id="0njlwm"
window.onload = loadJobs;
```

---

# Fase 2 — SSE realtime

## 6. Conectar SSE por job

Criar:

```javascript id="5jlwm6"
connectJobEvents(jobId);
```

---

# 7. Atualizar progress realtime

Alterar:

- progressbar
- status
- current step

Sem refresh.

---

# 8. Atualizar heartbeat

Mostrar:

- CPU
- memória
- processed items

em tempo real.

---

# 9. Atualizar logs realtime

Adicionar:

```text id="6jlwm5"
live console
```

no modal.

---

# 10. Fechar SSE automaticamente

Quando:

```text id="qjlwm4"
completed | failed
```

senão:

```text id="m0jlwm"
memory leak
```

---

# Fase 3 — Modais

## 11. Modal "New Job"

Campos:

- title
- description
- keywords
- sources
- save_raw
- save_filtered

---

# 12. POST /jobs

Botão:

```text id="jlwm4p"
Run Job
```

precisa:

- validar
- enviar payload
- fechar modal
- atualizar dashboard

---

# 13. Modal de detalhes do job

Abrir:

```http id="6xjlwm"
GET /jobs/:id
```

---

# 14. Mostrar metadata

Exibir:

- title
- keywords
- worker
- runtime
- timestamps
- parâmetros

---

# 15. Modal de artifacts

Mostrar:

- csv
- json
- logs

---

# 16. Download de artifacts

Botão:

```javascript id="jlwm3w"
window.open(...)
```

---

# 17. Preview de artifact

Especialmente:

- logs
- JSON
- CSV

---

# Fase 4 — Dashboard operacional

## 18. Cards de métricas

Hoje:

```text id="4jlwm5"
hardcoded
```

Precisam vir da API:

- running
- queued
- failed
- avg runtime

---

# 19. Queue monitor

Mostrar:

- jobs esperando
- workers disponíveis

---

# 20. Worker monitor

Mostrar:

- worker status
- jobs ativos
- CPU/RAM

---

# 21. Timeline de execução

Visual:

```text id="hjlwm0"
queued → running → completed
```

---

# 22. Activity feed

Mostrar:

- últimos jobs
- failures
- retries
- artifacts gerados

---

# Fase 5 — Busca e filtros

## 23. Search bar funcional

Buscar:

- title
- keywords
- description

---

# 24. Debounce na busca

Senão:

```text id="5jlwm3"
spam de requests
```

---

# 25. Filtro por status

- running
- queued
- failed
- completed

---

# 26. Filtro por source

- amazon
- mercado livre
- etc

---

# 27. Ordenação

- newest
- oldest
- duration
- progress

---

# 28. Paginação

CRÍTICO.

---

# Fase 6 — UX operacional

## 29. Toast notifications

Eventos:

- job started
- completed
- failed

---

## 30. Skeleton loading

Enquanto:

```text id="9jlwm8"
jobs carregam
```

---

# 31. Empty states

Exemplo:

```text id="0qjlwm"
No jobs found
```

---

# 32. Error states

Exemplo:

```text id="3jlwm6"
backend offline
```

---

# 33. Retry visual

Botão:

```text id="9jlwm2"
retry
```

---

# 34. Cancel button

Integração:

```http id="2xjlwm"
POST /jobs/:id/cancel
```

---

# 35. Clone button

Reutilizar config antiga.

---

# Fase 7 — Histórico

## 36. History page

Listagem completa.

---

# 37. Job details page

Não só modal.

---

# 38. Artifact explorer

Quase:

```text id="jlwm0t"
mini github artifacts
```

---

# 39. Log explorer

Com:

- levels
- timestamps
- busca

---

# 40. Execution statistics

Mostrar:

- duração
- throughput
- falhas

---

# Fase 8 — Visualização avançada

## 41. Pipeline visualization

Mostrar:

```text id="4qjlwm"
steps do pipeline
```

---

# 42. Step progress

Exemplo:

```text id="xjlwm1"
scraping ✔
filtering 🔄
saving ⏳
```

---

# 43. Charts

- jobs/day
- failure rate
- avg runtime

---

# 44. Heatmaps

Horários com mais jobs.

---

# Fase 9 — Estrutura frontend

## 45. Componentização JS

Você ainda NÃO precisa React.

Mas precisa:

```text id="6jlwm8"
modularizar
```

---

# 46. Template system

Exemplo:

```javascript id="1jlwm7"
createElement();
```

ou:

```html id="1tjlwm"
template literals
```

---

# 47. Estado global simples

Exemplo:

```javascript id="jlwm5x"
const state = {
  jobs: [],
  workers: [],
};
```

---

# 48. Cache local

Evitar:

```text id="7jlwm2"
refetch completo toda hora
```

---

# 49. Reconexão SSE

Se backend cair:

```text id="h0jlwm"
reconnect
```

---

# 50. Polling fallback

Caso SSE falhe.

---

# O que eu faria AGORA

A sequência certa:

---

# PRIORIDADE 1

## transformar dashboard em dinâmico

- GET /jobs
- render cards
- render tabela

---

# PRIORIDADE 2

## SSE realtime

- progress
- logs
- heartbeat

---

# PRIORIDADE 3

## modal de criação

- POST /jobs

---

# PRIORIDADE 4

## modal de detalhes

- artifacts
- logs
- metadata

---

# PRIORIDADE 5

## busca/filtros/paginação

---

# O erro MAIS perigoso agora

Você provavelmente vai querer:

```text id="9jlwm6"
reescrever tudo em React
```

Muito cedo.

Porque seu problema ainda NÃO é:

```text id="vjlwm1"
complexidade de UI
```

É:

```text id="njlwm7"
comportamento operacional
```

Seu frontend ainda precisa amadurecer:

- fluxo
- estado
- realtime
- sincronização
- UX operacional

Antes de framework.
