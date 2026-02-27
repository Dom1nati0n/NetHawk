# NetHawk Architecture Guide

## Core Principles

1.  **ECS (Entity Component System):**
    -   **Entities** are just unique integer IDs. They have no data or behavior themselves.
    -   **Components** are pure data structures (dataclasses or numpy arrays) associated with an Entity ID. They contain NO logic.
    -   **Systems** are functions that process entities possessing specific combinations of components. All logic resides here.

2.  **Data-Oriented Design (No OOP):**
    -   Avoid inheritance and polymorphism for game objects.
    -   Focus on data layout and transformations.
    -   Classes should primarily be used for data storage (Components) or structural organization (World, Managers), not for defining game actor behaviors.

3.  **Numpy for Math:**
    -   All mathematical operations (vectors, grids, stats calculations) must use `numpy`.
    -   Positions, velocities, and other numerical attributes should be stored as `numpy` arrays where appropriate for performance and vectorization.

4.  **Modular & Decoupled:**
    -   Systems should be independent of each other.
    -   Communication between systems should happen via data changes (components) or a simple event bus if necessary.

5.  **Frame Independence:**
    -   The game loop must be decoupled from the rendering frame rate.
    -   Use a fixed timestep for simulation logic to ensure deterministic behavior.

## Directory Structure

-   `src/nethawk/engine/`: Core ECS infrastructure (World, Entity Manager).
-   `src/nethawk/components/`: Component definitions (Data only).
-   `src/nethawk/systems/`: System logic (Functions).
-   `tests/`: Unit and integration tests.
