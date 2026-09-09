# GenPark Backdoor Criterion Confounder Adjustment Skill

Graph-theoretic backdoor criterion validator and minimal confounder adjustment set identifier.

Discover more at [GenPark](https://genpark.ai) and the [GenPark MCP Catalog](https://genpark.ai/mcp).

```mermaid
graph LR
    C((Confounder C)) -->|Spurious Path| X[Treatment X]
    C -->|Spurious Path| Y[Outcome Y]
    X -->|True Causal Path| M[Mediator M]
    M -->|True Causal Path| Y
    style C fill:#ffcdd2
    style X fill:#c8e6c9
    style Y fill:#bbdefb
    style M fill:#fff9c4
```

## Features
- Graph-theoretic d-separation checking across arbitrary causal DAGs.
- Automatic descendant prohibition enforcement.
- Detection of unblocked backdoor paths and collider bias.
