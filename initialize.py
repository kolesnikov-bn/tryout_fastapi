from dataclasses import dataclass
from typing import List

from tortoise import Tortoise, run_async

import settings
from src.models import GroupPDModel, Group, Product
from src.product.repo import group_repo, product_repo
from src.product.schemas import GroupSchema, ProductInDBSchema, GroupUpdateSchema

prime_csv_file = settings.BASE_DIR / "init_data.csv"


@dataclass
class CSVItem:
    layer_1: str
    layer_2: str
    layer_3: str
    product: str


def read_csv(csv_file) -> List[CSVItem]:
    data: List[CSVItem] = []
    with open(csv_file, "r") as f:
        rows = f.readlines()
        rows = list(map(lambda x: x.strip(), rows))

        for row in rows:
            row = row.split(",")
            data.append(CSVItem(*row))

    return data


async def fill_primary_group_data(items: List[CSVItem]) -> None:
    layer_schemas = []
    layer_schemas.extend(make_group_schemas(items, "layer_1"))
    layer_schemas.extend(make_group_schemas(items, "layer_2", "layer_1"))
    layer_schemas.extend(make_group_schemas(items, "layer_3", "layer_2"))

    for layer_schema in layer_schemas:
        await group_repo.create_node(layer_schema)


async def fill_primary_product_data(items: List[CSVItem]) -> None:
    layer_schemas = await make_product_schemas(items)

    for layer_schema in layer_schemas:
        await product_repo.create(layer_schema)


async def make_product_schemas(items: List[CSVItem]) -> List[ProductInDBSchema]:
    schemas = []
    for item in items:
        parent = await group_repo._find_parent_node_by_name(
            GroupUpdateSchema(name=item.product, parent=item.layer_3)
        )
        schema = ProductInDBSchema(name=item.product, group_id=parent.id)
        if schema not in schemas:
            schemas.append(schema)

    return schemas


def make_group_schemas(
    items: List[CSVItem], name: str, parent: str = ""
) -> List[GroupSchema]:
    schemas = []
    for item in items:
        name_attr = getattr(item, name)
        try:
            parent_attr = getattr(item, parent)
        except AttributeError:
            parent_attr = None

        schema = GroupSchema(name=name_attr, parent=parent_attr)
        if schema not in schemas:
            schemas.append(schema)

    return schemas


async def main():
    csv_data = read_csv(prime_csv_file)
    await fill_primary_group_data(csv_data)
    await fill_primary_product_data(csv_data)


async def init():
    await Tortoise.init(
        db_url=settings.DATABASE_URI,
        modules={"models": settings.APPS_MODELS},
    )

    await Tortoise.generate_schemas()
    has_groups = await Group.all().exists()
    has_products = await Product.all().exists()
    if has_groups is False and has_products is False:
        await main()
        print("Import is complete")
    else:
        print("data is exists")


if __name__ == "__main__":
    run_async(init())
