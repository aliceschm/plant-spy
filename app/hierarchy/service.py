from app.hierarchy.models import Component, TreeNode
from app.hierarchy.repository import load_assets, load_components, load_locations
from app.hierarchy.tree import AssetTree


class HierarchyService:
    def build_tree(self) -> TreeNode:
        locations = load_locations()
        assets = load_assets()
        components = load_components()

        tree = AssetTree(locations, assets, components)
        return tree.build_tree()

    def load_components(self) -> list[Component]:
        return load_components()