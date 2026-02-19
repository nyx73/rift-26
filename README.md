# 🔐 RIFT-26  
## 💸 MONEY MULING DETECTION CHALLENGE
**Graph-Based Financial Crime Detection Engine**

---

## 🧠 Overview

RIFT-26 is a full-stack financial crime detection platform built for identifying complex financial fraud using graph analytics and network intelligence.

It combines:

- ⚙️ FastAPI backend for high-performance fraud analysis  
- 🌐 React frontend for interactive visualization  
- 🕸 Graph algorithms for detecting fraud rings and anomalies  

The system detects structured financial crimes such as fraud rings, smurfing chains, shell accounts, and velocity anomalies within transaction networks.

---

# ⚙️ Backend – Fraud Detection Engine (FastAPI)

https://rift-26-backend.onrender.com/

## 📂 CSV Processing
- Parses transaction datasets
- Builds directed transaction graph
- Automatic schema validation

## 🕸 Graph-Based Pattern Detection

Detects:

- 🔁 **Cycle Rings** (Strongly Connected Components)
- 🪙 **Smurfing Patterns** (Money splitting behavior)
- 🏢 **Shell Accounts** (High out-degree, low in-degree)
- ⚡ **Velocity Anomalies** (High-frequency transaction bursts)

## 📊 Risk Scoring Engine
Each suspicious cluster is evaluated using:

- Structural connectivity
- Transaction density
- Temporal proximity
- Node centrality metrics
- Composite risk scoring

# 🌐 Frontend – Interactive Intelligence Dashboard

https://rift-26-frontend.onrender.com/


## 📤 CSV Upload Component

- Drag & drop file upload  
- Real-time processing spinner  
- Execution time display  
---
## 🕸 Interactive Graph Visualization 

- 🔵 **Blue Nodes** → Normal accounts  
- 🔴 **Red Nodes** → Suspicious accounts  
- 🔁 Cycle highlights  
- 🖱 Hover tooltips with account metrics  
- 🔍 Zoom & pan controls  
- ⚡ Real-time rendering  

---

## 📋 Fraud Rings Table

- Sortable columns  
- Risk score heat indicators  
- Cluster size metrics  
- JSON export functionality  
- Summary statistics  

---

## 🧪 Example Fraud Pattern

ACC1001 → ACC1002 → ACC1003 → ACC1001

### System Detects:

- Strongly connected component  
- High internal transaction density  
- Short time interval  
- Elevated risk score  


## Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
## 🏆 Built For

**RIFT 2026 – Money Muling Detection Challenge**


© 2026 RIFT PUNE

