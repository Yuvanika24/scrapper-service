"""initial schema

Revision ID: bb4f123f7c96
Revises: 
Create Date: 2025-12-07 19:11:07.718618

"""

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'bb4f123f7c96'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    CREATE TABLE IF NOT EXISTS "industries" (
        "ID" SERIAL PRIMARY KEY,
        "NAME" VARCHAR UNIQUE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS "modules" (
        "ID" SERIAL PRIMARY KEY,
        "NAME" VARCHAR UNIQUE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS "industryModules" (
        "ID" SERIAL PRIMARY KEY,
        "INDUSTRY_ID" INTEGER NOT NULL
            REFERENCES "industries"("ID") ON DELETE CASCADE,
        "MODULE_ID" INTEGER NOT NULL
            REFERENCES "modules"("ID") ON DELETE CASCADE,
        UNIQUE ("INDUSTRY_ID", "MODULE_ID")
    );

    CREATE TABLE IF NOT EXISTS "urls" (
        "ID" SERIAL PRIMARY KEY,
        "URL" TEXT UNIQUE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS "industryModuleUrls" (
        "ID" SERIAL PRIMARY KEY,
        "INDUSTRY_MODULE_ID" INTEGER NOT NULL
            REFERENCES "industryModules"("ID") ON DELETE CASCADE,
        "URL_ID" INTEGER NOT NULL
            REFERENCES "urls"("ID") ON DELETE CASCADE,
        UNIQUE ("INDUSTRY_MODULE_ID", "URL_ID")
    );

    CREATE TABLE IF NOT EXISTS "urlParameters" (
        "ID" SERIAL PRIMARY KEY,
        "INDUSTRY_MODULE_URL_ID" INTEGER NOT NULL
            REFERENCES "industryModuleUrls"("ID") ON DELETE CASCADE,
        "PARAM_NAME" VARCHAR NOT NULL,
        "TRANSFORMERS" VARCHAR,
        "DESCRIPTION" TEXT,
        "CSS_PATH" TEXT
    );

    CREATE TABLE IF NOT EXISTS "signatures" (
        "ID" SERIAL PRIMARY KEY,
        "INDUSTRY_MODULE_URL_ID" INTEGER NOT NULL
            REFERENCES "industryModuleUrls"("ID") ON DELETE CASCADE,
        "SIGNATURE" VARCHAR,
        "LAST_CHECKED" TIMESTAMP,
        "LAST_UPDATED" TIMESTAMP,
        UNIQUE ("INDUSTRY_MODULE_URL_ID")
    );

    CREATE TABLE IF NOT EXISTS "industryModuleKeywords" (
        "ID" SERIAL PRIMARY KEY,
        "INDUSTRY_MODULE_ID" INTEGER NOT NULL
            REFERENCES "industryModules"("ID") ON DELETE CASCADE,
        "KEYWORD" VARCHAR NOT NULL,
        UNIQUE ("INDUSTRY_MODULE_ID", "KEYWORD")
    );
    """)


def downgrade():
    op.execute("""
    DROP TABLE IF EXISTS "industryModuleKeywords";
    DROP TABLE IF EXISTS "signatures";
    DROP TABLE IF EXISTS "urlParameters";
    DROP TABLE IF EXISTS "industryModuleUrls";
    DROP TABLE IF EXISTS "urls";
    DROP TABLE IF EXISTS "industryModules";
    DROP TABLE IF EXISTS "modules";
    DROP TABLE IF EXISTS "industries";
    """)