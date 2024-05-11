from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "product" ADD "img" VARCHAR(255);
        ALTER TABLE "product" DROP COLUMN "available";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "product" ADD "available" INT NOT NULL  DEFAULT 1;
        ALTER TABLE "product" DROP COLUMN "img";"""
