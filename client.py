"""
Backdoor Criterion Confounder Adjustment Skill Client
Pure Python Standard Library implementation of Pearl's Backdoor Criterion and d-separation.
Determines whether a set of covariates Z is a valid adjustment set for identifying the causal effect
of treatment X on outcome Y without confounding bias.
"""

from typing import Dict, List, Set, Tuple, Optional


class BackdoorCriterionEngine:
    def __init__(self, nodes: List[str], edges: List[Tuple[str, str]]):
        self.nodes = set(nodes)
        self.edges = list(edges)  # (u, v) means u -> v
        self.children: Dict[str, Set[str]] = {n: set() for n in nodes}
        self.parents: Dict[str, Set[str]] = {n: set() for n in nodes}
        for u, v in edges:
            self.children[u].add(v)
            self.parents[v].add(u)

    def get_descendants(self, node: str) -> Set[str]:
        desc = set()
        queue = list(self.children[node])
        while queue:
            curr = queue.pop(0)
            if curr not in desc:
                desc.add(curr)
                queue.extend(self.children[curr])
        return desc

    def find_undirected_paths(self, start: str, end: str, max_depth: int = 6) -> List[List[str]]:
        paths: List[List[str]] = []
        adj: Dict[str, Set[str]] = {n: set() for n in self.nodes}
        for u, v in self.edges:
            adj[u].add(v)
            adj[v].add(u)

        def dfs(curr: str, target: str, visited: List[str]):
            if len(visited) > max_depth:
                return
            if curr == target:
                paths.append(list(visited))
                return
            for nxt in adj[curr]:
                if nxt not in visited:
                    visited.append(nxt)
                    dfs(nxt, target, visited)
                    visited.pop()

        dfs(start, end, [start])
        return paths

    def is_backdoor_path(self, path: List[str]) -> bool:
        if len(path) < 2:
            return False
        # Backdoor path: starts with an arrow pointing into path[0] (treatment)
        return path[1] in self.parents[path[0]]

    def is_path_blocked(self, path: List[str], conditioning_set: Set[str]) -> bool:
        # Check d-separation along path nodes
        for i in range(1, len(path) - 1):
            prev_node, curr, next_node = path[i-1], path[i], path[i+1]
            is_prev_parent = prev_node in self.parents[curr]
            is_next_parent = next_node in self.parents[curr]

            if is_prev_parent and is_next_parent:
                # Collider: prev -> curr <- next
                # Blocked if NEITHER curr NOR any descendant of curr is in conditioning_set
                curr_and_desc = {curr} | self.get_descendants(curr)
                if not (curr_and_desc & conditioning_set):
                    return True
            else:
                # Non-collider: chain or fork
                # Blocked if curr IS in conditioning_set
                if curr in conditioning_set:
                    return True
        return False

    def check_backdoor_criterion(self, treatment: str, outcome: str, candidate_set: Set[str]) -> Tuple[bool, str]:
        # Condition 1: No node in candidate_set is a descendant of treatment
        treatment_desc = self.get_descendants(treatment)
        forbidden = candidate_set & treatment_desc
        if forbidden:
            return False, f"Candidate set contains descendant(s) of treatment: {forbidden}"

        # Find all backdoor paths
        all_paths = self.find_undirected_paths(treatment, outcome)
        backdoor_paths = [p for p in all_paths if self.is_backdoor_path(p)]

        # Condition 2: candidate_set must block every backdoor path
        unblocked = []
        for path in backdoor_paths:
            if not self.is_path_blocked(path, candidate_set):
                unblocked.append(" - ".join(path))

        if unblocked:
            return False, f"Unblocked backdoor path(s): {unblocked}"
        return True, f"Valid adjustment set blocking all {len(backdoor_paths)} backdoor path(s)."
