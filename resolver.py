from typing import Dict, List, Set


class ViewDependencyResolver:
    def __init__(self, dependency_map: Dict[str, List[str]]):
        """
        初始化，儲存關聯依賴。
        """

        self.dependency_map = dependency_map

    def resolve_dependencies(self, view_name: str) -> Set[str]:
        """
        使用 dfs 尋找關聯。
        """

        result = set()

        def dfs(view: str):
            for dep in self.dependency_map.get(view, []):
                if dep not in result:
                    result.add(dep)
                    dfs(dep)

        dfs(view_name)
        return result
