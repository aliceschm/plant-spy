from app.hierarchy.models import Component, TreeNode
from app.hierarchy.repository import load_assets, load_components, load_locations
from app.hierarchy.tree import AssetTree


class HierarchyService:
    def _build_asset_tree(self) -> AssetTree:
        locations = load_locations()
        assets = load_assets()
        components = load_components()

        tree = AssetTree(locations, assets, components)
        tree.build_tree()
        return tree

    def build_tree(self) -> TreeNode:
        return self._build_asset_tree().root

    def load_components(self) -> list[Component]:
        return load_components()

    def get_path_for_node(self, node_id: str) -> list[TreeNode]:
        tree = self._build_asset_tree()
        return tree.get_path(node_id)

    def get_path_names_for_node(self, node_id: str) -> list[str]:
        path = self.get_path_for_node(node_id)
        return [node.name for node in path]

    def get_path_string_for_node(self, node_id: str) -> str:
        path_names = self.get_path_names_for_node(node_id)
        return " > ".join(path_names)
    
    def get_subtree_nodes(self, node_id: str) -> list[TreeNode]:
        tree = self._build_asset_tree()
        root_node = tree.find_node_by_id(node_id)

        if root_node is None:
            return []

        result = []

        def dfs(node: TreeNode):
            result.append(node)
            for child in node.children:
                dfs(child)

        dfs(root_node)
        return result
    
    def get_component_ids_in_subtree(self, node_id: str) -> list[str]:
        nodes = self.get_subtree_nodes(node_id)

        return [
            node.id
            for node in nodes
            if node.type == "component"
        ]