import yaml
from extractor import fetch_dependencies
from resolver import ViewDependencyResolver

def main():
    # 取得 immediate 依賴 map
    dependency_map = fetch_dependencies()

    # 展開遞迴依賴
    resolver = ViewDependencyResolver(dependency_map)
    resolved_dependency_map = {
        view: sorted(list(resolver.resolve_dependencies(view)))
        for view in dependency_map
    }

    # 輸出 flatten 遞迴依賴結構
    with open("views.yaml", "w") as f:
        yaml.dump({"views": resolved_dependency_map}, f, sort_keys=True, allow_unicode=True)

    print("✅ Flatten view dependency map exported to 'views.yaml'")


if __name__ == "__main__":
    main()
