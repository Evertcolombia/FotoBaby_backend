from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user_type" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "added_on" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "added_by" VARCHAR(255) NOT NULL,
    "changed_on" TIMESTAMPTZ,
    "changed_by" VARCHAR(255),
    "user_type_name" VARCHAR(255) NOT NULL
);
COMMENT ON TABLE "user_type" IS 'represents the user_type table.';
CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "added_on" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "added_by" VARCHAR(255) NOT NULL,
    "changed_on" TIMESTAMPTZ,
    "changed_by" VARCHAR(255),
    "first_name" VARCHAR(255),
    "second_name" VARCHAR(255),
    "email" VARCHAR(50)  UNIQUE,
    "adress" VARCHAR(255),
    "phone_number" VARCHAR(255),
    "hashed_password" VARCHAR(255),
    "is_active" BOOL NOT NULL  DEFAULT True,
    "is_superuser" BOOL NOT NULL  DEFAULT False,
    "user_type_id" INT REFERENCES "user_type" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "users" IS 'represents the user base abstract class.';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
