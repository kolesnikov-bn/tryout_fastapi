from typing import Optional, List

from tortoise.exceptions import DoesNotExist, IntegrityError

from src.constants import GroupId
from src.product.models import Group, GroupPDModel, ProductPDModel, Product
from src.product.schemas import GroupSchema, GroupUpdateSchema
from src.repositories import DBRepo


class GroupRepo(DBRepo):
    model = Group
    get_schema = GroupPDModel

    async def create_node(self, schema: GroupSchema) -> Optional[GroupPDModel]:
        if schema.parent is None:
            return self._create_new_root(schema)

        parent = await self._find_parent_node_by_name(schema)
        return await self._create_leaf_node(schema, parent.id)

    async def update_node(
        self, group_id: GroupId, schema: GroupUpdateSchema
    ) -> Optional[GroupPDModel]:
        has_values = any(x for x in schema.dict(exclude_unset=True))
        if has_values is False:
            raise IntegrityError("Required parameters not passed")

        await self._update_node(group_id, schema)

        return await self.get_schema.from_queryset_single(self.model.get(id=group_id))

    async def delete_node(self, group_id: GroupId) -> None:
        entry = await self.model.get(id=group_id).prefetch_related("children")
        await self._move_children_to_new_parent(entry)
        await self.delete(id=group_id)

    async def _create_leaf_node(
        self, schema: GroupSchema, parent_id: GroupId
    ) -> GroupPDModel:
        entry = await self.model.create(name=schema.name, parent_id=parent_id)
        return await self.get_schema.from_tortoise_orm(entry)

    async def _create_new_root(self, schema: GroupSchema) -> GroupPDModel:
        return self.create(schema)

    async def _find_parent_node_by_name(
        self, schema: GroupUpdateSchema
    ) -> GroupPDModel:
        entry = await self.get_obj(name=schema.parent)
        if entry is None:
            raise DoesNotExist(f"Parent node `{schema.parent}` does't exist")

        return await self.get_schema.from_tortoise_orm(entry)

    async def _update_node(self, group_id: GroupId, schema: GroupUpdateSchema) -> None:
        if schema.parent is not None:
            new_parent = await self._find_parent_node_by_name(schema)
            schema.parent_id = new_parent.id

        await self.model.filter(id=group_id).update(
            **schema.dict(exclude_unset=True, exclude={"parent"})
        )

    async def _move_children_to_new_parent(self, entry: Group) -> None:
        async for child in entry.children:
            child.parent = await entry.parent
            await child.save()


class ProductRepo(DBRepo):
    model = Product
    get_schema = ProductPDModel

    async def get_nested_products(self, group_id: GroupId) -> List[Product]:
        return await self.model.filter(group_id=group_id).prefetch_related("group")


group_repo = GroupRepo()
product_repo = ProductRepo()
