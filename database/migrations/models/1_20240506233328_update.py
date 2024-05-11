from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "queue";
        
        CREATE TABLE IF NOT EXISTS "queue" (
            "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            "date" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
            "is_active" INT NOT NULL  DEFAULT 1,
            "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
            "product_type_id" INT NOT NULL REFERENCES "product" ("id") ON DELETE CASCADE
        );
        
        ALTER TABLE "subscription" ADD "img" VARCHAR(255) NOT NULL;
        ALTER TABLE "subscription" DROP COLUMN "bin_img";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "queue";
        
        CREATE TABLE IF NOT EXISTS "queue" (
            "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            "date" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
            "is_active" INT NOT NULL  DEFAULT 1,
            "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
        );
        
        ALTER TABLE "subscription" ADD "bin_img" BLOB NOT NULL;
        ALTER TABLE "subscription" DROP COLUMN "img";"""
