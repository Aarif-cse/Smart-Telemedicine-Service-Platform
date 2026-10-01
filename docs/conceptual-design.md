# Conceptual Design (Initial)

> Initial idea only. It will be refined in Review 2.

## Entity Relationships (Graph view)

```mermaid
graph LR
    P[Patient] -- books --> A[Appointment]
    A -- with --> D[Doctor]
    D -- works at --> H[Hospital]
    P -- consults --> D
    P -- registered at --> H
```

## Where Each Structure Could Fit
- **Trees (BST / AVL):** store and search patient and doctor records by ID.
- **Graph:** represent how patients, doctors, hospitals and appointments are connected (one patient to many doctors, one doctor to many patients).
- **Heap:** order urgent appointments by priority.
