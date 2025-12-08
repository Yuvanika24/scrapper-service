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
    CREATE TABLE IF NOT EXISTS Industries (
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR UNIQUE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Modules (
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR UNIQUE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS IndustryModules (
        ID SERIAL PRIMARY KEY,
        INDUSTRY_ID INTEGER NOT NULL REFERENCES Industries(ID) ON DELETE CASCADE,
        MODULE_ID INTEGER NOT NULL REFERENCES Modules(ID) ON DELETE CASCADE,
        UNIQUE (INDUSTRY_ID, MODULE_ID)
    );

    CREATE TABLE IF NOT EXISTS Urls (
        ID SERIAL PRIMARY KEY,
        URL TEXT UNIQUE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS IndustryModuleUrls (
        ID SERIAL PRIMARY KEY,
        INDUSTRY_MODULE_ID INTEGER NOT NULL REFERENCES IndustryModules(ID) ON DELETE CASCADE,
        URL_ID INTEGER NOT NULL REFERENCES Urls(ID) ON DELETE CASCADE,
        UNIQUE (INDUSTRY_MODULE_ID, URL_ID)
    );

    CREATE TABLE IF NOT EXISTS UrlParameters (
        ID SERIAL PRIMARY KEY,
        INDUSTRY_MODULE_URL_ID INTEGER NOT NULL REFERENCES IndustryModuleUrls(ID) ON DELETE CASCADE,
        PARAM_NAME VARCHAR NOT NULL,
        TRANSFORMERS VARCHAR,
        DESCRIPTION TEXT,
        CSS_PATH TEXT
    );

    CREATE TABLE IF NOT EXISTS Signatures (
        ID SERIAL PRIMARY KEY,
        INDUSTRY_MODULE_URL_ID INTEGER NOT NULL REFERENCES IndustryModuleUrls(ID) ON DELETE CASCADE,
        SIGNATURE VARCHAR,
        LAST_CHECKED TIMESTAMP,
        LAST_UPDATED TIMESTAMP
    );
    """)



def downgrade():
    op.execute("""
    DROP TABLE IF EXISTS Signatures;
    DROP TABLE IF EXISTS UrlParameters;
    DROP TABLE IF EXISTS IndustryModuleUrls;
    DROP TABLE IF EXISTS Urls;
    DROP TABLE IF EXISTS IndustryModules;
    DROP TABLE IF EXISTS Modules;
    DROP TABLE IF EXISTS Industries;
    """)

