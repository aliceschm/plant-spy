from app.hierarchy.models import (
    Asset,
    Component,
    Location,
    TreeNode,
    NODE_TYPE_ASSET,
    NODE_TYPE_COMPONENT,
    NODE_TYPE_LOCATION,
    NODE_TYPE_ROOT,
)


class AssetTree:
    def __init__(
        self,
        locations: list[Location],
        assets: list[Asset],
        components: list[Component],
    ):
        self.root = TreeNode(
            id="root",
            name="Root",
            type=NODE_TYPE_ROOT,
            children=[],
        )
        self.locations = locations if locations is not None else []
        self.assets = assets if assets is not None else []
        self.components = components if components is not None else []

        self.nodes_by_id: dict[str, TreeNode] = {}
        self.parent_by_id: dict[str, str] = {}

    def build_tree(self) -> TreeNode:
        self.root.children = []
        nodes_by_id: dict[str, TreeNode] = {}
        parent_by_id: dict[str, str] = {}

        for location in self.locations:
            node = TreeNode(
                id=location.id,
                name=location.name,
                type=NODE_TYPE_LOCATION,
                children=[],
                parent_id=location.parent_id or "",
            )
            nodes_by_id[node.id] = node
            parent_by_id[node.id] = location.parent_id or ""

        for asset in self.assets:
            parent_id = asset.parent_id or asset.location_id or ""

            node = TreeNode(
                id=asset.id,
                name=asset.name,
                type=NODE_TYPE_ASSET,
                children=[],
                location_id=asset.location_id or "",
                parent_id=asset.parent_id or "",
            )
            nodes_by_id[node.id] = node
            parent_by_id[node.id] = parent_id

        for component in self.components:
            node = TreeNode(
                id=component.id,
                name=component.name,
                type=NODE_TYPE_COMPONENT,
                children=[],
                sensor_type=component.sensor_type,
                status=component.status,
                parent_id=component.parent_id or "",
            )
            nodes_by_id[node.id] = node
            parent_by_id[node.id] = component.parent_id or ""

        self.nodes_by_id = nodes_by_id
        self.parent_by_id = parent_by_id

        self._attach_nodes(nodes_by_id, parent_by_id)

        return self.root

    def find_node_by_id(self, node_id: str) -> TreeNode | None:
        if not node_id:
            return None

        if node_id == self.root.id:
            return self.root

        return self.nodes_by_id.get(node_id)

    def get_path(self, node_id: str) -> list[TreeNode]:
        if not node_id:
            return []

        target_node = self.find_node_by_id(node_id)

        if target_node is None:
            return []

        path = [target_node]
        current_id = node_id

        while current_id != self.root.id:
            parent_id = self.parent_by_id.get(current_id, "")

            if not parent_id:
                return []

            parent_node = self.find_node_by_id(parent_id)
            if parent_node is None:
                return []

            path.append(parent_node)
            current_id = parent_id

        path.reverse()
        return path

    def _attach_nodes(
        self,
        nodes_by_id: dict[str, TreeNode],
        parent_by_id: dict[str, str],
    ) -> None:
        for node_id, node in nodes_by_id.items():
            parent_id = parent_by_id.get(node_id, "")

            if not parent_id:
                self.root.children.append(node)
                parent_by_id[node_id] = self.root.id
                continue

            parent_node = nodes_by_id.get(parent_id)

            if parent_node is None:
                self.root.children.append(node)
                parent_by_id[node_id] = self.root.id
                continue

            if not self._is_valid_parent(node, parent_node):
                self.root.children.append(node)
                parent_by_id[node_id] = self.root.id
                continue

            if self._creates_cycle(node_id, parent_id, parent_by_id):
                self.root.children.append(node)
                parent_by_id[node_id] = self.root.id
                continue

            parent_node.children.append(node)
            parent_by_id[node_id] = parent_node.id

    def _is_valid_parent(self, child: TreeNode, parent: TreeNode) -> bool:
        if child.type == NODE_TYPE_LOCATION:
            return parent.type in {NODE_TYPE_ROOT, NODE_TYPE_LOCATION}

        if child.type == NODE_TYPE_ASSET:
            return parent.type in {NODE_TYPE_LOCATION, NODE_TYPE_ASSET}

        if child.type == NODE_TYPE_COMPONENT:
            return parent.type in {NODE_TYPE_LOCATION, NODE_TYPE_ASSET}

        return False

    def _creates_cycle(
        self,
        node_id: str,
        parent_id: str,
        parent_by_id: dict[str, str],
    ) -> bool:
        visited = set()
        current_id = parent_id

        while current_id:
            if current_id == node_id:
                return True

            if current_id in visited:
                return True

            visited.add(current_id)
            current_id = parent_by_id.get(current_id, "")

        return False