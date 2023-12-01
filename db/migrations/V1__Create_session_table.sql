CREATE TABLE sessions (
    id TEXT PRIMARY KEY,
    initial_requirements TEXT NOT NULL,
    web_pages TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);