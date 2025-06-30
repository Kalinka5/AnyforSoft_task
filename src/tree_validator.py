"""
Validates the integrity of the partner hierarchy tree.
"""
from typing import List, Dict, Set
from .data_loader import Partner

def validate_hierarchy(partners: List[Partner]) -> None:
    """
    Validates the partner hierarchy for cycles and missing parent references.

    Args:
        partners: A list of Partner objects.

    Raises:
        ValueError: If a cycle is detected or a parent reference is missing.
    """
    partner_ids = {p.id for p in partners}
    adjacency_list = _build_adjacency_list(partners, partner_ids)

    _detect_cycles(adjacency_list, partner_ids)

def _build_adjacency_list(partners: List[Partner], partner_ids: Set[int]) -> Dict[int, List[int]]:
    """Builds an adjacency list representation of the hierarchy."""
    adjacency_list: Dict[int, List[int]] = {pid: [] for pid in partner_ids}
    root_partners = []

    for partner in partners:
        if partner.parent_id is not None:
            if partner.parent_id not in partner_ids:
                raise ValueError(f"Error: Partner {partner.id} has a missing parent with id {partner.parent_id}")
            adjacency_list[partner.parent_id].append(partner.id)
        else:
            root_partners.append(partner.id)
    
    # Add a virtual root to connect all top-level partners for cycle detection
    virtual_root_id = 0
    while virtual_root_id in partner_ids:
        virtual_root_id -=1
        
    adjacency_list[virtual_root_id] = root_partners
    return adjacency_list


def _detect_cycles(adjacency_list: Dict[int, List[int]], partner_ids: Set[int]):
    """
    Detects cycles in the hierarchy using Depth First Search.
    
    Raises:
        ValueError: If a cycle is detected.
    """
    visiting: Set[int] = set()
    visited: Set[int] = set()

    for partner_id in partner_ids:
        if partner_id not in visited:
            path = []
            if _has_cycle_dfs(partner_id, adjacency_list, visiting, visited, path):
                cycle_path_str = " -> ".join(map(str, path))
                raise ValueError(f"Error: Cycle detected in the hierarchy: {cycle_path_str}")


def _has_cycle_dfs(
    node_id: int,
    adjacency_list: Dict[int, List[int]],
    visiting: Set[int],
    visited: Set[int],
    path: List[int]
) -> bool:
    """Recursive DFS helper to find cycles."""
    visiting.add(node_id)
    path.append(node_id)

    if node_id in adjacency_list:
        for child_id in adjacency_list[node_id]:
            if child_id in visiting:
                path.append(child_id)
                return True
            if child_id not in visited:
                if _has_cycle_dfs(child_id, adjacency_list, visiting, visited, path):
                    return True

    visiting.remove(node_id)
    path.pop()
    visited.add(node_id)
    return False
