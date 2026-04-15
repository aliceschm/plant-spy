from app.hierarchy.service import build_hierarchy_tree
from app.hierarchy.tree import TreeNode


def print_tree(node: TreeNode, level: int = 0) -> None:
    indent = "  " * level
    print(f"{indent}- [{node.type}] {node.name} ({node.id})")

    for child in node.children:
        print_tree(child, level + 1)


def main() -> None:
    root = build_hierarchy_tree()
    print_tree(root)


if __name__ == "__main__":
    main()