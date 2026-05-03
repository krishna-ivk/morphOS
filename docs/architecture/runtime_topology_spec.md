# Runtime Topology Specification — The Body Plan

## Purpose

A living organism needs a body to inhabit. This document defines **where
morphOS runs** — which devices, what configurations, how instances
coordinate, and what the minimum viable body looks like at each scale.

---

## Part 1 — Device Classes

### Tier 1: The Laptop (Solo Organism)

```
                    ┌─────────────────────────┐
                    │   Developer's MacBook    │
                    │                          │
                    │  ┌─────────────────────┐ │
                    │  │ morphOS (all-in-one) │ │
                    │  │                      │ │
                    │  │  Orchestrator        │ │
                    │  │  Event Bus (memory)  │ │
                    │  │  5 Agents            │ │
                    │  │  Policy Engine       │ │
                    │  │  CLI + File Watcher  │ │
                    │  │  LLM (ollama local)  │ │
                    │  └─────────────────────┘ │
                    │                          │
                    │  Workspace: ~/projects/  │
                    └─────────────────────────┘
```

| Spec | Minimum | Recommended |
|---|---|---|
| CPU | 4 cores | 8+ cores (Apple Silicon M-series) |
| RAM | 8 GB | 16 GB (ollama needs ~4-8 GB for local LLM) |
| Disk | 10 GB free | 50 GB (for model weights + artifacts) |
| OS | macOS 13+ / Ubuntu 22+ / Windows 11 (WSL2) | macOS (Apple Silicon) |
| Python | 3.11+ | 3.12 |
| Network | Optional | Amplifies capability |
| GPU | None required | Apple Neural Engine / NVIDIA (faster local inference) |

**Organism analogy:** A single-celled organism. Everything runs in one process.
Self-contained, self-sufficient, but limited in scale.

**Best for:** Solo developers, prototyping, offline-first work.

---

### Tier 2: The Home Server / Mac Mini (Dedicated Organism)

```
    ┌───────────────────────────────┐
    │   Mac Mini / Home Server      │
    │                               │
    │  morphOS (daemon)             │
    │  ├── Orchestrator             │
    │  ├── Event Bus (Redis)        │
    │  ├── Agents (parallel)        │
    │  ├── Policy Engine            │
    │  ├── Dashboard (port 3000)    │
    │  ├── API Server (port 8000)   │
    │  └── ollama (local LLM)       │
    │                               │
    │  Always-on, headless          │
    └────────────┬──────────────────┘
                 │ LAN / Tailscale
    ┌────────────┴──────────────────┐
    │   Developer's Laptop          │
    │   (CLI client + browser)      │
    └───────────────────────────────┘
```

| Spec | Minimum | Recommended |
|---|---|---|
| CPU | 4 cores | 8+ cores (M4 Mac Mini) |
| RAM | 16 GB | 32 GB (parallel agents + local LLM) |
| Disk | 50 GB | 256 GB SSD |
| Network | LAN | LAN + Internet (always-on) |
| Always-on | Yes (daemon/systemd/launchd) | Yes |

**Organism analogy:** A small multi-cellular organism. Organs run in parallel.
The developer laptop is a remote appendage — it sends signals, the server does the work.

**Best for:** Solo developers who want 24/7 operation, small teams.

**Key difference from Tier 1:**
- Agents run in **parallel** (not sequential)
- Event bus uses **Redis** (not in-memory)
- Dashboard is always accessible
- Can queue work and process overnight

---

### Tier 3: Cloud Instance / VPS (Remote Organism)

```
    ┌──────────────────────────────────────┐
    │   AWS EC2 / GCP VM / DigitalOcean    │
    │                                       │
    │  Docker Compose                       │
    │  ├── morphos-orchestrator             │
    │  ├── morphos-event-bus (Redis)        │
    │  ├── morphos-api (FastAPI)            │
    │  ├── morphos-dashboard (Next.js)      │
    │  ├── morphos-agents (n workers)       │
    │  ├── morphos-policy-engine            │
    │  └── ollama (or API-only LLM)         │
    │                                       │
    │  Persistent: EBS/disk for memory      │
    └──────────────┬───────────────────────┘
                   │ HTTPS
    ┌──────────────┴───────────────────────┐
    │  Any device with a browser / CLI      │
    │  (laptop, phone, tablet)              │
    └──────────────────────────────────────┘
```

| Spec | Minimum | Recommended |
|---|---|---|
| Instance | t3.medium (2 vCPU, 4 GB) | t3.xlarge (4 vCPU, 16 GB) |
| GPU | None (use API LLMs) | g4dn.xlarge (for local inference) |
| Disk | 30 GB EBS | 100 GB SSD |
| Network | Always on | Always on |
| Container | Docker 24+ | Docker Compose |

**Organism analogy:** An organism with organs in separate containers. Each
organ can be scaled, replaced, or restarted independently.

**Best for:** Teams, CI/CD integration, always-online operation.

**Key difference from Tier 2:**
- Each component is a **separate container**
- Agents can scale horizontally (run 4 coding agents in parallel)
- Uses **API-based LLMs** (OpenAI, Anthropic) instead of local ollama
- Accessible from anywhere via HTTPS

---

### Tier 4: Kubernetes Cluster (Colony Organism)

```
    ┌───────────────────────────────────────────┐
    │   Kubernetes Cluster                       │
    │                                            │
    │  Namespace: morphos                        │
    │  ├── Deployment: orchestrator (1 replica)  │
    │  ├── StatefulSet: redis (1 replica)        │
    │  ├── Deployment: api (2 replicas, LB)      │
    │  ├── Deployment: dashboard (2 replicas)    │
    │  ├── Deployment: agents (autoscale 1→10)   │
    │  ├── Deployment: policy-engine (1 replica) │
    │  ├── CronJob: learning-agent (post-run)    │
    │  └── PV: memory + logs + artifacts         │
    │                                            │
    │  Ingress: morphos.company.com              │
    └───────────────────────────────────────────┘
```

| Spec | Minimum | Recommended |
|---|---|---|
| Nodes | 2 (4 vCPU, 16 GB each) | 3+ nodes, autoscaling |
| Agent scaling | 1→4 | 1→10 with HPA |
| Storage | 50 GB PV | 200 GB PV + S3 for artifacts |
| LLM | API only | API + dedicated inference node |
| Monitoring | Built-in | Prometheus + Grafana |

**Organism analogy:** A colony organism (like a Portuguese man-of-war).
Multiple organisms cooperating as one, with specialized members.

**Best for:** Organizations, multi-project, multi-team usage.

---

### Tier 5: Edge + Cloud Hybrid (Distributed Organism)

```
    ┌─────────────┐     ┌─────────────┐     ┌──────────────────┐
    │  Dev Laptop  │     │  Mac Mini    │     │  AWS Cloud       │
    │  (offline)   │     │  (always-on) │     │  (scaled)        │
    │              │     │              │     │                  │
    │  morphOS     │────▶│  morphOS     │────▶│  morphOS         │
    │  (local mode)│◀────│  (hub mode)  │◀────│  (cloud mode)    │
    │              │     │              │     │                  │
    │  Code + test │     │  Orchestrate │     │  Deploy + scan   │
    │  offline     │     │  + learn     │     │  + heavy compute │
    └─────────────┘     └─────────────┘     └──────────────────┘
         Tier 1              Tier 2               Tier 3
```

**Organism analogy:** A networked organism with a central nervous system
(hub) and peripheral limbs (edge devices). The brain lives in the hub;
hands work on the edges; the cloud handles the heavy lifting.

**Best for:** Your current setup (Mac mini + laptop + AWS).

---

## Part 2 — Deployment Modes

### Mode: Solo (Single Process)

```python
# start.py
morphos run --mode solo --workspace ~/projects/myapp
```

- Everything in one Python process
- Event bus: `asyncio.Queue`
- LLM: `ollama` local
- Storage: JSON files
- dashboard: `localhost:3000`

### Mode: Daemon (Background Service)

```bash
# launchd (macOS) or systemd (Linux)
morphos daemon start --port 8000 --workspace ~/projects/
morphos daemon status
morphos daemon stop
```

- Runs as a background service
- Event bus: Redis (local)
- Accessible via CLI from any terminal
- Dashboard on LAN

### Mode: Containerized (Docker Compose)

```yaml
# docker-compose.yml
services:
  orchestrator:
    image: morphos/orchestrator:latest
    depends_on: [redis, policy-engine]
    volumes:
      - ./workspace:/workspace
      - ./memory:/memory

  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data

  api:
    image: morphos/api:latest
    ports: ["8000:8000"]

  dashboard:
    image: morphos/dashboard:latest
    ports: ["3000:3000"]

  agents:
    image: morphos/agent-worker:latest
    deploy:
      replicas: 4
    environment:
      - LLM_PROVIDER=openai
      - LLM_MODEL=gpt-4

  policy-engine:
    image: morphos/policy-engine:latest
    volumes:
      - ./policies:/policies
```

### Mode: Distributed (Multi-Node)

```yaml
# Each node runs a subset of components
# Hub node (Mac Mini):
morphos hub start --redis-url redis://localhost:6379

# Edge node (Laptop):
morphos edge join --hub morphos-hub.local:8000 --role coding

# Cloud node (AWS):
morphos cloud join --hub morphos-hub.tailnet:8000 --role deploy,scan
```

---

## Part 3 — Resource Allocation by Device

### LLM Inference Strategy

| Device | Local LLM | API LLM | Strategy |
|---|---|---|---|
| Laptop (8GB) | `phi-3-mini` (3.8B) | Fallback to API | Small model for speed, API for quality |
| Laptop (16GB+) | `llama3-8b`, `codellama-13b` | Fallback to API | Good local quality |
| Mac Mini (32GB) | `llama3-70b-q4`, `deepseek-coder-33b` | Optional | Full local inference |
| Cloud (no GPU) | None | OpenAI / Anthropic / Gemini | API only |
| Cloud (GPU) | `llama3-70b`, `codestral` | Fallback | Best of both worlds |

### Agent Parallelism by Device

| Device | Max Parallel Agents | Why |
|---|---|---|
| Laptop | 1-2 | RAM and CPU constrained |
| Mac Mini (16GB) | 2-4 | Good for sequential pipelines |
| Mac Mini (32GB+) | 4-8 | Real parallelism |
| Cloud (t3.xlarge) | 4-8 | CPU-limited |
| Cloud (k8s, autoscale) | 10-20 | Horizontal scaling |

### Storage Strategy

| Device | Event Logs | Memory | Artifacts |
|---|---|---|---|
| Laptop | NDJSON files (local) | JSON file | Local filesystem |
| Mac Mini | NDJSON → SQLite | SQLite | Local + periodic cloud backup |
| Cloud (single) | SQLite | SQLite | EBS volume |
| Cloud (k8s) | PostgreSQL | PostgreSQL | S3/GCS |

---

## Part 4 — Network Topology

### Intra-Organism Communication

```
Within single device:      asyncio.Queue (zero latency)
Within LAN (hub+edge):     Redis Streams over TCP (sub-ms)
Across internet:           HTTPS/WebSocket + Redis pub/sub (<100ms)
```

### Inter-Organism Communication (Multi-Instance)

When multiple morphOS instances cooperate:

```
morphOS-A (Mac Mini)  ◀──HTTPS──▶  morphOS-B (AWS)
       │                                  │
       └──── shared Redis (Upstash) ──────┘
```

Shared via event bus:
- `pattern.discovered` — capability store entries
- `workflow.delegated` — tasks too big for one instance
- `capability.sync` — merge learned knowledge across instances

**NOT shared** (stays local):
- Raw source code
- Secrets and credentials
- Policy files (each instance has its own immune system)

---

## Part 5 — Minimum Viable Setup per Use Case

| Use Case | Device | LLM | Setup Time |
|---|---|---|---|
| **Try it out** | Any laptop | ollama + `phi-3-mini` | 10 min |
| **Daily coding assistant** | MacBook (16GB+) | ollama + `llama3-8b` | 30 min |
| **24/7 autonomous dev** | Mac Mini (32GB) | ollama + `deepseek-coder-33b` | 1 hour |
| **Team deployment** | Cloud VM + Docker | OpenAI API | 2 hours |
| **Enterprise** | Kubernetes cluster | API + dedicated inference | 1 day |
| **Your setup** | Mac Mini + Laptop + AWS | ollama (local) + API (cloud) | 2 hours |

---

## Part 6 — Your Current Infrastructure

Based on your SkyForce command centre and earlier conversations:

```
┌─────────────────────────────┐
│  Mac Mini (always-on hub)   │
│  morphOS daemon mode        │
│  ollama (local LLM)         │
│  Redis (event bus)          │
│  Dashboard (port 3000)      │
│  Memory + capability store  │
├─────────────────────────────┤
│  ▲ Tailscale / LAN          │
│  ▼                          │
├─────────────────────────────┤
│  MacBook (edge)             │
│  CLI client                 │
│  File watcher (workspace)   │
│  Local coding + testing     │
├─────────────────────────────┤
│  ▲ Internet                 │
│  ▼                          │
├─────────────────────────────┤
│  AWS (cloud)                │
│  Heavy compute agents       │
│  Deployment pipeline        │
│  Vulnerability scanning     │
│  Hermes integration         │
└─────────────────────────────┘
```

**Recommended starting point:** Tier 2 (Mac Mini daemon) as the hub,
with your MacBook as the CLI edge client. Add AWS cloud mode when you
need deployment and heavy scanning.
