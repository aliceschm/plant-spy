# Plant Spy

Plant Spy is a backend simulation of an industrial monitoring system inspired by real-world platforms.

The project is designed as a **modular monolith with event-driven communication**, focusing on how different parts of a monitoring system interact through domain events rather than direct service orchestration.

---

## Overview

This system models the lifecycle of industrial monitoring:

- components generate sensor readings
- readings are evaluated for anomalies
- repeated anomalies become alerts
- alerts escalate in severity
- high-severity alerts generate work orders

The goal is to demonstrate:
- event-driven design (without external brokers)
- clear module boundaries
- realistic domain behavior (recurrence, escalation, automation)

---

## Architecture

Plant Spy follows a **modular monolith + in-memory EventBus** approach.

Each module has a single responsibility:

- **Hierarchy** → structure (locations, assets, components)
- **Readings** → ingestion of sensor data
- **Processing** → anomaly detection
- **Alerts** → recurrence tracking and alert lifecycle
- **Work Orders** → operational actions based on alerts

Communication between modules happens via events.

---

## Event Flow

```mermaid
flowchart LR

    R[ReadingRecorded]
    P[Processing]
    A[AnomalyDetected]
    AL[Alerts]
    AC[AlertCreated]
    AS[AlertSeverityChanged]
    WO[WorkOrders]

    R --> P
    P --> A
    A --> AL
    AL --> AC
    AL --> AS
    AC --> WO
    AS --> WO
