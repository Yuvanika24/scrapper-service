
# --- URLs with parameters ---

def get_urls_with_params():
    return """
    SELECT 
        "industryModuleUrls"."ID" AS industry_module_url_id,
        "industries"."NAME" AS industry_name,
        "modules"."NAME" AS module_name,
        "urls"."URL" AS url,
        "urlParameters"."PARAM_NAME" AS param_name,
        "urlParameters"."CSS_PATH" AS css_path,
        "urlParameters"."TRANSFORMERS" AS transformers
    FROM "industryModuleUrls"
    JOIN "industryModules"
        ON "industryModuleUrls"."INDUSTRY_MODULE_ID" = "industryModules"."ID"
    JOIN "industries"
        ON "industryModules"."INDUSTRY_ID" = "industries"."ID"
    JOIN "modules"
        ON "industryModules"."MODULE_ID" = "modules"."ID"
    JOIN "urls"
        ON "industryModuleUrls"."URL_ID" = "urls"."ID"
    LEFT JOIN "urlParameters"
        ON "urlParameters"."INDUSTRY_MODULE_URL_ID" = "industryModuleUrls"."ID"
    WHERE "industries"."NAME" = %s 
      AND "modules"."NAME" = %s
    """

# --- Signature queries ---

def get_latest_dom_signature():
    return """
    SELECT "SIGNATURE" AS signature FROM "signatures"
    WHERE "INDUSTRY_MODULE_URL_ID" = %s
    ORDER BY "LAST_CHECKED" DESC
    LIMIT 1
    """

def save_dom_signature():
    return """
    INSERT INTO "signatures" ("INDUSTRY_MODULE_URL_ID", "SIGNATURE", "LAST_CHECKED", "LAST_UPDATED")
    VALUES (%s, %s, %s, %s)
    ON CONFLICT ("INDUSTRY_MODULE_URL_ID")
    DO UPDATE SET "SIGNATURE" = EXCLUDED."SIGNATURE", "LAST_CHECKED" = EXCLUDED."LAST_CHECKED";
    """

def update_last_checked():
    return """
    UPDATE "signatures" SET "LAST_CHECKED" = %s
    WHERE "INDUSTRY_MODULE_URL_ID" = %s
    """

def get_industry_module_id():
    return """
    SELECT im."ID" AS id
    FROM "industryModules" im
    JOIN "industries" i ON im."INDUSTRY_ID" = i."ID"
    JOIN "modules" m ON im."MODULE_ID" = m."ID"
    WHERE i."NAME" = %s AND m."NAME" = %s
    """
# --- Keywords queries ---

def get_keywords_for_industry_module():
    return """
    SELECT "KEYWORD" AS keyword FROM "industryModuleKeywords"
    WHERE "INDUSTRY_MODULE_ID" = %s
    """
# --- target urls ---

def get_targetted_urls():
    return """
    SELECT u."URL" AS url
    FROM "industryModules" im
    JOIN "industries" i ON i."ID" = im."INDUSTRY_ID"
    JOIN "modules" m ON m."ID" = im."MODULE_ID"
    JOIN "industryModuleUrls" imu ON imu."INDUSTRY_MODULE_ID" = im."ID"
    JOIN "urls" u ON u."ID" = imu."URL_ID"
    WHERE i."NAME" = %s
      AND m."NAME" = %s
    """


