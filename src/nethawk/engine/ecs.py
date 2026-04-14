from typing import Dict, Type, Any, Set

Entity = int

class ComponentManager:
    """Manages storage and retrieval of components."""
    
    def __init__(self):
        # Stores components as {ComponentType: {EntityID: ComponentInstance}}
        self._components: Dict[Type, Dict[Entity, Any]] = {}

    def add_component(self, entity: Entity, component: Any) -> None:
        component_type = type(component)
        if component_type not in self._components:
            self._components[component_type] = {}
        self._components[component_type][entity] = component

    def remove_component(self, entity: Entity, component_type: Type) -> None:
        if component_type in self._components:
            self._components[component_type].pop(entity, None)

    def remove_all_components(self, entity: Entity) -> None:
        """Removes all components associated with a specific entity."""
        for comp_store in self._components.values():
            comp_store.pop(entity, None)

    def get_component(self, entity: Entity, component_type: Type) -> Any:
        if component_type in self._components:
            return self._components[component_type].get(entity)
        return None

    def has_component(self, entity: Entity, component_type: Type) -> bool:
        return component_type in self._components and entity in self._components[component_type]

    def get_components(self, component_type: Type) -> Dict[Entity, Any]:
        """Returns all entities and their component of a given type."""
        if component_type in self._components:
            return self._components[component_type]
        return {}

    def remove_all_components(self, entity: Entity) -> None:
        """Removes all components associated with the given entity."""
        for comp_store in self._components.values():
            comp_store.pop(entity, None)

class EntityManager:
    """Manages entity creation and destruction."""

    def __init__(self):
        self._next_id: Entity = 0
        self._active_entities: Set[Entity] = set()
        self._free_ids: List[Entity] = []

    def create_entity(self) -> Entity:
        if self._free_ids:
            entity = self._free_ids.pop()
        else:
            if self._next_id >= sys.maxsize:
                raise RuntimeError("Maximum number of entities reached")
            entity = self._next_id
            self._next_id += 1
        self._active_entities.add(entity)
        return entity

    def destroy_entity(self, entity: Entity) -> None:
        if entity in self._active_entities:
            self._active_entities.discard(entity)
            self._free_ids.append(entity)

class World:
    """The central hub for the ECS."""

    def __init__(self):
        self.entity_manager = EntityManager()
        self.component_manager = ComponentManager()
        self._events: List[Any] = []

    def push_event(self, event: Any) -> None:
        self._events.append(event)

    def get_events(self, event_type: Type = None) -> List[Any]:
        if event_type is None:
            return self._events.copy()
        return [e for e in self._events if isinstance(e, event_type)]

    def clear_events(self) -> None:
        self._events.clear()

    def create_entity(self) -> Entity:
        return self.entity_manager.create_entity()

    def destroy_entity(self, entity: Entity) -> None:
        self.entity_manager.destroy_entity(entity)
        for comp_store in self.component_manager._components.values():
             comp_store.pop(entity, None)

    def add_component(self, entity: Entity, component: Any) -> None:
        self.component_manager.add_component(entity, component)

    def remove_component(self, entity: Entity, component_type: Type) -> None:
        self.component_manager.remove_component(entity, component_type)

    def get_component(self, entity: Entity, component_type: Type) -> Any:
        return self.component_manager.get_component(entity, component_type)
    
    def has_component(self, entity: Entity, component_type: Type) -> bool:
        return self.component_manager.has_component(entity, component_type)

    def get_components(self, component_type: Type) -> Dict[Entity, Any]:
        return self.component_manager.get_components(component_type)
