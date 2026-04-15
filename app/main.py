from app.hierarchy.models import TreeNode
from app.hierarchy.service import HierarchyService


def print_tree(node: TreeNode, level: int = 0) -> None:
    indent = "  " * level
    print(f"{indent}- [{node.type}] {node.name} ({node.id})")

    for child in node.children:
        print_tree(child, level + 1)


def main() -> None:
    hierarchy_service = HierarchyService()
    root = hierarchy_service.build_tree()
    print_tree(root)


if __name__ == "__main__":
    main()