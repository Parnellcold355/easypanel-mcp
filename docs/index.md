---
title: EasyPanel MCP - AI Infrastructure Management
description: Connect AI agents (Claude, GPT, n8n) to EasyPanel for natural language infrastructure management. Deploy Docker services and automate DevOps with AI.
keywords: EasyPanel MCP, AI infrastructure, Docker deployment, Claude AI, GPT DevOps, n8n automation, container orchestration
author: Danny Maaz
---

# 🚀 EasyPanel MCP Server

## _Transforma Prompts en Infraestructura_

<p align="center" markdown>
  <span class="badge badge--primary">Python 3.10+</span>
  <span class="badge badge--success">Cross-Platform</span>
  <span class="badge badge--warning">MCP Protocol</span>
</p>

---

## 👋 ¿Qué es EasyPanel MCP?

**EasyPanel MCP** es un servidor de **Model Context Protocol (MCP)** que permite a agentes de inteligencia artificial interactuar directamente con tu panel **EasyPanel** para gestionar infraestructura, desplegar servicios y administrar contenedores Docker mediante comandos naturales.

### 🎯 ¿Por Qué Usar EasyPanel MCP?

<div class="grid" markdown>

<div class="card" markdown>
#### 🤖 Control Natural por IA
Describe lo que necesitas en lenguaje natural y deja que tu agente de IA se encargue de todo el proceso de despliegue.
</div>

<div class="card" markdown>
#### ⚡ Deployments en Segundos
De idea a producción en minutos. La IA puede crear, configurar y desplegar servicios completos automáticamente.
</div>

<div class="card" markdown>
#### 🔒 Redes Aisladas
Soporte completo para redes internas Docker. Mantén tus servicios sensibles completamente aislados de internet.
</div>

<div class="card" markdown>
#### 📊 Debugging Inteligente
La IA puede analizar logs, diagnosticar problemas y sugerir soluciones en tiempo real.
</div>

<div class="card" markdown>
#### 🔄 Auto-Scaling
Detecta picos de tráfico y escala servicios automáticamente basado en métricas en tiempo real.
</div>

<div class="card" markdown>
#### 🌐 Multi-Plataforma
Funciona en Windows, macOS y Linux. Compatible con Claude Desktop, Cursor, Cline, ChatGPT, n8n, y cualquier cliente MCP.
</div>

</div>

---

## ⚡ Inicio Rápido

### 1. Instalación

```bash
# Clonar repositorio
git clone https://github.com/dannymaaz/easypanel-mcp
cd easypanel-mcp

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configuración

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus credenciales
# EASYPANEL_URL=https://tu-easypanel.com
# EASYPANEL_API_KEY=tu_api_key
```

### 3. Ejecutar

```bash
# Modo stdio (Claude Desktop, etc.)
python src/server.py

# Modo HTTP (n8n, webhooks)
python src/server.py http
```

---

## 💬 Ejemplo de Uso

<div class="admonition tip" markdown>
<p class="admonition-title">Caso Real: Despliegue Completo</p>

**Usuario:** *"Despliega mi API Flask con PostgreSQL en producción"*

**IA:** 
```
🚀 Creando proyecto 'api-flask-prod'
📦 Desplegando servicio 'postgres-db' con imagen postgres:15
🔗 Creando red interna 'api-net' para comunicación segura
⚙️ Configurando servicio 'flask-api' con variables de entorno
✅ ¡Deploy completado! Tu API está disponible en https://api.tudominio.com
```
</div>

---

## 🛠️ Herramientas Disponibles

**30 herramientas** organizadas en **7 categorías** para gestión completa de infraestructura con IA:

| Categoría | Herramientas | Descripción |
|-----------|--------------|-------------|
| 📦 **Servicios** | `list_services`, `get_service`, `create_service`, `update_service`, `delete_service`, `restart_service`, `start_service`, `stop_service`, `deploy_service`, `get_service_logs` | Gestión completa de servicios Docker + logs inteligentes |
| 🚀 **Deployments** | `list_deployments`, `create_deployment`, `get_deployment`, `get_deployment_logs` | Control de deployments y versiones |
| 🌐 **Redes** | `list_networks` (auto-discovery), `create_network`, `delete_network` | Descubrimiento automático de topología |
| 📁 **Proyectos** | `list_projects`, `create_project`, `delete_project`, `get_project` | Organización de recursos |
| 📊 **Monitoring** | `get_system_stats`, `get_service_stats`, `health_check`, `get_server_ip` | Métricas en tiempo real (CPU, RAM, disco) |
| ⚡ **Scaling** | `scale_service`, `auto_scale_service` | Escalado vertical y automático con thresholds |
| 🔒 **Security** | `list_domains`, `create_domain`, `get_public_key` | Dominios y autenticación Git |

---

## 🔗 Integraciones

<div class="quick-links" markdown>

[AI Agents (Claude, Cursor, Cline, ChatGPT)](integration/ai-agents.md){: .md-button .md-button--primary }
[Claude Desktop](integration/claude-desktop.md){: .md-button }
[n8n Workflows](integration/n8n.md){: .md-button .md-button--secondary }
[GitHub Actions](integration/github-actions.md){: .md-button .md-button--secondary }

</div>

---

## 📚 Documentación Completa

<div class="grid" markdown>

<div class="card" markdown>
#### 🚀 Getting Started
- [Instalación](getting-started/installation.md)
- [Configuración](getting-started/configuration.md)
- [Quick Start](getting-started/quickstart.md)
</div>

<div class="card" markdown>
#### 🛠️ Tools Reference
- [Overview](tools/overview.md) - 30 herramientas en 7 categorías
- [Services Tools](tools/services.md) - 10 herramientas (create, deploy, logs)
- [Deployments Tools](tools/deployments.md) - 4 herramientas
- [Networks Tools](tools/networks.md) - 3 herramientas (auto-discovery)
- [Projects Tools](tools/projects.md) - 4 herramientas
- [Monitoring Tools](tools/overview.md#monitoring-tools) - 4 herramientas (stats, health)
- [Scaling Tools](tools/overview.md#scaling-tools) - 2 herramientas (auto-scale)
- [Security Tools](tools/overview.md#security-tools) - 3 herramientas (domains, Git)
</div>

<div class="card" markdown>
#### 💡 Examples
- [Basic Examples](examples/basic.md)
- [Advanced Workflows](examples/advanced.md)
- [Real-World Cases](examples/real-world.md)
</div>

<div class="card" markdown>
#### 🚀 Advanced Features
- [Security & Networks](advanced/features.md) - Auth, redes aisladas
- [Deployment Guide](advanced/features.md#deployment-features) - Docker, GitHub, Git
- [Debugging](advanced/features.md#debugging-features) - Logs, diagnóstico
- [Auto-Scaling](advanced/features.md#auto-scaling-features) - Vertical, automático
</div>

<div class="card" markdown>
#### ❓ Support
- [FAQ](faq.md)
- [Troubleshooting](troubleshooting.md)
- [Changelog](changelog.md)
</div>

</div>

---

## 🎯 Casos de Uso

### Agentes de Desarrollo

```
Usuario: "Despliega mi API Flask con PostgreSQL"
IA: 🚀 Deploy completado en 45 segundos
```

### Auto-Scaling Inteligente

```
IA: "Detecto incremento del 300% en tráfico"
IA: 🔄 Escalando servicio 'worker' de 2 a 6 réplicas
```

### Debugging Asistido

```
Usuario: "¿Por qué falla el servicio worker?"
IA: 🔍 Error: ConnectionRefusedError - Redis no está corriendo
```

### Prototipado Rápido

```
Usuario: "Necesito un entorno de staging"
IA: 🎨 Entorno creado: https://staging.myapp.com
```

---

## 🔒 Seguridad y Redes Aisladas

EasyPanel MCP soporta **redes internas Docker** para aislar servicios sensibles:

```yaml
# docker-compose.yml
networks:
  internal-net:
    driver: overlay
    internal: true  # ← Red aislada sin acceso a internet

services:
  api:
    networks:
      - internal-net  # Solo accesible internamente
      - public-net    # Para servicios que necesitan internet
  
  database:
    networks:
      - internal-net  # Base de datos completamente aislada
```

---

## 👤 Autor & Créditos

<p align="center" markdown>
**Danny Maaz**  
_Ingeniero en Sistemas | Creador de EasyPanel MCP_

[🔗 LinkedIn](https://linkedin.com/in/dannymaaz){: target="_blank" rel="noopener" } ·
[💻 GitHub](https://github.com/dannymaaz){: target="_blank" rel="noopener" }
</p>

---

## 💙 Apoya el Proyecto

<p align="center" markdown>
[![Donar con PayPal](https://img.shields.io/badge/Donate-PayPal-00457C?logo=paypal&logoColor=white)](https://www.paypal.me/Creativegt)
</p>

<p align="center" markdown>
_🙏 Cada donación ayuda a mantener el proyecto y agregar nuevas features._
</p>

---

## 📜 Licencia

MIT License con cláusula de atribución. Ver [LICENSE](https://github.com/dannymaaz/easypanel-mcp/blob/main/LICENSE){: target="_blank" rel="noopener" } para detalles.

---

<p align="center" markdown>
**🚀 Construido con ❤️ por Danny Maaz**  
_Transformando prompts en infraestructura, una línea a la vez._
</p>
