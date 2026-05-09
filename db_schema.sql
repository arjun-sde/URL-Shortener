CREATE TABLE IF NOT EXISTS urls (
    id BIGINT PRIMARY KEY,
    domain VARCHAR(255) NOT NULL,
    original_url TEXT NOT NULL,
    short_code VARCHAR(64) NOT NULL,
    clicks INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(domain, short_code)
);

CREATE INDEX IF NOT EXISTS ix_urls_domain ON urls(domain);
CREATE INDEX IF NOT EXISTS ix_urls_short_code ON urls(short_code);
