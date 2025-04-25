from typing import Dict, List, Set


class ViewDependencyResolver:
    def __init__(self, dependency_map: Dict[str, List[str]]):
        self.dependency_map = dependency_map

    def resolve_dependencies(self, view_name: str) -> Set[str]:
        result = set()

        def dfs(view: str):
            for dep in self.dependency_map.get(view, []):
                if dep not in result:
                    result.add(dep)
                    dfs(dep)

        dfs(view_name)
        return result

    def print_dependency_tree(self, view_name: str, indent: int = 0):
        print("  " * indent + f"- {view_name}")
        for dep in self.dependency_map.get(view_name, []):
            self.print_dependency_tree(dep, indent + 1)
