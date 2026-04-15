from app.hierarchy.repository import load_assets, load_components, load_locations
from app.hierarchy.tree import AssetTree
from app.hierarchy.models import TreeNode


class HierarchyService:
    def build_tree(self) -> TreeNode:
        locations = load_locations()
        assets = load_assets()
        components = load_components()

        tree = AssetTree(locations, assets, components)
        return tree.build_tree()