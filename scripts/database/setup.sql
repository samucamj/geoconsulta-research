-- GeoConsulta Database Setup Script
-- Creates the necessary tables and indexes for the application

-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;

-- Create establishments table
CREATE TABLE IF NOT EXISTS establishments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    address TEXT,
    geometry GEOMETRY(POINT, 4326) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_establishments_name ON establishments USING btree(name);
CREATE INDEX IF NOT EXISTS idx_establishments_type ON establishments USING btree(type);
CREATE INDEX IF NOT EXISTS idx_establishments_geometry ON establishments USING gist(geometry);

-- Create a function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to automatically update updated_at
DROP TRIGGER IF EXISTS update_establishments_updated_at ON establishments;
CREATE TRIGGER update_establishments_updated_at
    BEFORE UPDATE ON establishments
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data for testing
INSERT INTO establishments (name, type, address, geometry) VALUES
    ('Drogasil Asa Norte', 'pharmacy', 'SQN 202, Bloco A, Brasília-DF', ST_GeomFromText('POINT(-47.8822 -15.7942)', 4326)),
    ('Farmácia São Paulo', 'pharmacy', 'SQS 308, Bloco B, Brasília-DF', ST_GeomFromText('POINT(-47.8900 -15.8000)', 4326)),
    ('Drogaria Pacheco', 'pharmacy', 'Setor Comercial Sul, Brasília-DF', ST_GeomFromText('POINT(-47.8800 -15.7900)', 4326)),
    ('Posto Shell Asa Sul', 'gas_station', 'Eixo Monumental, Brasília-DF', ST_GeomFromText('POINT(-47.8850 -15.7980)', 4326)),
    ('Posto Petrobras', 'gas_station', 'W3 Norte, Brasília-DF', ST_GeomFromText('POINT(-47.8750 -15.7850)', 4326)),
    ('Auto Posto Brasília', 'gas_station', 'Setor de Autarquias Norte, Brasília-DF', ST_GeomFromText('POINT(-47.8820 -15.7920)', 4326)),
    ('Farmácia Rosário', 'pharmacy', 'Taguatinga Centro, Brasília-DF', ST_GeomFromText('POINT(-47.9200 -15.8300)', 4326)),
    ('Posto Ipiranga Taguatinga', 'gas_station', 'Avenida Comercial, Taguatinga-DF', ST_GeomFromText('POINT(-47.9150 -15.8250)', 4326)),
    ('Drogaria Araujo', 'pharmacy', 'Águas Claras, Brasília-DF', ST_GeomFromText('POINT(-47.9400 -15.8400)', 4326)),
    ('Posto BR Águas Claras', 'gas_station', 'Rua das Pitangueiras, Águas Claras-DF', ST_GeomFromText('POINT(-47.9350 -15.8350)', 4326))
ON CONFLICT DO NOTHING;

-- Verify the setup
SELECT 
    'Establishments table created successfully' as status,
    COUNT(*) as sample_records
FROM establishments;

-- Show PostGIS version
SELECT PostGIS_Version() as postgis_version;
