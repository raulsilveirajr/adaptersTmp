-- DROP TABLE IF EXISTS synkrono.bees_requests;

CREATE TABLE IF NOT EXISTS synkrono.bees_requests (
    id                      SERIAL PRIMARY KEY,
    trace_id                VARCHAR(64),
    vendor                  VARCHAR(32),
    topic                   VARCHAR(64),
    marketplace             VARCHAR(64),
    marketplace_meta        JSONB,
    payload                 JSONB,
    origin_data             JSONB,
    created_at              TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sent                    BOOLEAN DEFAULT FALSE,
    send_at                 TIMESTAMP,
    send_response           JSONB,
    send_error              TEXT,
    processed               BOOLEAN DEFAULT FALSE,
    processed_at            TIMESTAMP,
    processed_response      JSONB,
    processed_error         TEXT
);

CREATE INDEX idx_bees_requests_trace_id ON synkrono.bees_requests (trace_id);
