# Low-level DB queries for scraper application.

def get_urls_with_params():
    return """
    SELECT 
        industry_module_urls.id AS industry_module_url_id,
        industries.name AS industry_name,
        modules.name AS module_name,
        urls.url AS url,
        url_parameters.param_name,
        url_parameters.css_path,
        url_parameters.transformers
    FROM industry_module_urls
    JOIN industry_modules
        ON industry_module_urls.industry_module_id = industry_modules.id
    JOIN industries
        ON industry_modules.industry_id = industries.id
    JOIN modules
        ON industry_modules.module_id = modules.id
    JOIN urls
        ON industry_module_urls.url_id = urls.id
    LEFT JOIN url_parameters
        ON url_parameters.industry_module_url_id = industry_module_urls.id
    """

def get_latest_dom_signature():
    return """
    SELECT signature FROM signatures
    WHERE industry_module_url_id = %s
    ORDER BY last_checked DESC
    LIMIT 1
    """

def save_dom_signature():
    return """
    INSERT INTO signatures (industry_module_url_id, signature, last_checked, last_updated)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (industry_module_url_id)
    DO UPDATE SET signature = EXCLUDED.signature, last_checked = EXCLUDED.last_checked;
    """

def update_last_checked():
    return """
    UPDATE signatures
    SET last_checked = %s
    WHERE industry_module_url_id = %s
    """
