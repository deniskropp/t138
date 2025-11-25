-- Initial database migration script.
-- This script creates the necessary tables for sessions, artifacts, and agent specifications.

-- Table for Sessions
CREATE TABLE IF NOT EXISTS sessions (
    id UUID PRIMARY KEY,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    status TEXT NOT NULL,
    logs TEXT -- Storing as JSON string or similar for now
);

-- Table for Artifacts
CREATE TABLE IF NOT EXISTS artifacts (
    id UUID PRIMARY KEY,
    session_id UUID NOT NULL,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    data_path TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
);

-- Table for Agent Specifications
CREATE TABLE IF NOT EXISTS agent_specs (
    id UUID PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    role TEXT NOT NULL,
    description TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
