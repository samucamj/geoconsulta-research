#!/usr/bin/env python3
"""
GeoJSON Data Import Script for GeoConsulta
Imports pharmacy and gas station data from GeoJSON files into PostgreSQL/PostGIS
"""

import json
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import argparse

def load_geojson_file(filepath):
    """Load and parse a GeoJSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ Loaded {filepath} with {len(data.get('features', []))} features")
        return data
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in {filepath}: {e}")
        return None

def extract_establishment_data(feature, establishment_type):
    """Extract establishment data from a GeoJSON feature."""
    properties = feature.get('properties', {})
    geometry = feature.get('geometry', {})
    
    # Extract coordinates
    if geometry.get('type') == 'Point':
        coordinates = geometry.get('coordinates', [])
        if len(coordinates) >= 2:
            lon, lat = coordinates[0], coordinates[1]
        else:
            print(f"⚠️ Invalid coordinates in feature: {coordinates}")
            return None
    else:
        print(f"⚠️ Unsupported geometry type: {geometry.get('type')}")
        return None
    
    # Extract properties (adapt these field names based on your actual GeoJSON structure)
    name = properties.get('name') or properties.get('nome') or properties.get('NAME') or 'Unknown'
    address = properties.get('address') or properties.get('endereco') or properties.get('ADDRESS') or ''
    
    return {
        'name': name,
        'type': establishment_type,
        'address': address,
        'lat': lat,
        'lon': lon
    }

def import_establishments(engine, establishments):
    """Import establishments into the database."""
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Clear existing data (optional - remove if you want to keep existing data)
        session.execute(text("DELETE FROM establishments WHERE type IN ('pharmacy', 'gas_station')"))
        
        # Insert new data
        for est in establishments:
            query = text("""
                INSERT INTO establishments (name, type, address, geometry)
                VALUES (:name, :type, :address, ST_GeomFromText('POINT(:lon :lat)', 4326))
            """)
            
            session.execute(query, {
                'name': est['name'],
                'type': est['type'],
                'address': est['address'],
                'lon': est['lon'],
                'lat': est['lat']
            })
        
        session.commit()
        print(f"✅ Successfully imported {len(establishments)} establishments")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error importing data: {e}")
        raise
    finally:
        session.close()

def main():
    parser = argparse.ArgumentParser(description='Import GeoJSON data into GeoConsulta database')
    parser.add_argument('--pharmacies', help='Path to pharmacies GeoJSON file')
    parser.add_argument('--gas-stations', help='Path to gas stations GeoJSON file')
    parser.add_argument('--db-url', help='Database URL', 
                       default='postgresql://postgres:password@localhost/geoconsulta')
    
    args = parser.parse_args()
    
    # Create database connection
    try:
        engine = create_engine(args.db_url)
        print(f"✅ Connected to database: {args.db_url}")
    except Exception as e:
        print(f"❌ Failed to connect to database: {e}")
        sys.exit(1)
    
    establishments = []
    
    # Import pharmacies
    if args.pharmacies and os.path.exists(args.pharmacies):
        pharmacy_data = load_geojson_file(args.pharmacies)
        if pharmacy_data:
            for feature in pharmacy_data.get('features', []):
                est_data = extract_establishment_data(feature, 'pharmacy')
                if est_data:
                    establishments.append(est_data)
    
    # Import gas stations
    if args.gas_stations and os.path.exists(args.gas_stations):
        gas_station_data = load_geojson_file(args.gas_stations)
        if gas_station_data:
            for feature in gas_station_data.get('features', []):
                est_data = extract_establishment_data(feature, 'gas_station')
                if est_data:
                    establishments.append(est_data)
    
    # Import sample data if no files provided
    if not establishments:
        print("ℹ️ No GeoJSON files provided, using sample data...")
        establishments = [
            {'name': 'Drogasil Centro', 'type': 'pharmacy', 'address': 'Setor Comercial Sul, Brasília-DF', 'lat': -15.7942, 'lon': -47.8822},
            {'name': 'Farmácia Popular', 'type': 'pharmacy', 'address': 'Asa Norte, Brasília-DF', 'lat': -15.7850, 'lon': -47.8750},
            {'name': 'Posto Shell', 'type': 'gas_station', 'address': 'Eixo Monumental, Brasília-DF', 'lat': -15.7980, 'lon': -47.8850},
            {'name': 'Posto Petrobras', 'type': 'gas_station', 'address': 'W3 Norte, Brasília-DF', 'lat': -15.7850, 'lon': -47.8750},
        ]
    
    # Import data
    if establishments:
        import_establishments(engine, establishments)
        print(f"🎉 Import completed! Total establishments: {len(establishments)}")
    else:
        print("❌ No data to import")

if __name__ == '__main__':
    main()
