"""
API routes for establishment queries and operations
"""

from flask import Blueprint, request, jsonify
from models.establishment import Establishment, get_db_session
from geoalchemy2.functions import ST_DWithin, ST_GeomFromText
from sqlalchemy import func, or_

establishments_bp = Blueprint('establishments', __name__)

@establishments_bp.route('/establishments', methods=['GET'])
def get_establishments():
    """
    Get establishments based on query parameters.
    
    Query parameters:
    - search: Search by name (optional)
    - type: Filter by establishment type (optional)
    - lat, lon: Coordinates for proximity search (optional)
    - radius: Search radius in meters (default: 1000)
    """
    try:
        session = get_db_session()
        
        # Start with base query
        query = session.query(Establishment)
        
        # Apply filters based on parameters
        search_term = request.args.get('search', '').strip()
        establishment_type = request.args.get('type', '').strip()
        latitude = request.args.get('lat')
        longitude = request.args.get('lon')
        radius = int(request.args.get('radius', 1000))  # Default 1km
        
        # Text search filter
        if search_term:
            query = query.filter(
                Establishment.name.ilike(f'%{search_term}%')
            )
        
        # Type filter
        if establishment_type and establishment_type.lower() != 'all':
            query = query.filter(
                Establishment.type == establishment_type
            )
        
        # Proximity search filter
        if latitude and longitude:
            try:
                lat = float(latitude)
                lon = float(longitude)
                
                # Create point geometry for user location
                user_point = ST_GeomFromText(f'POINT({lon} {lat})', 4326)
                
                # Filter by distance using ST_DWithin
                query = query.filter(
                    ST_DWithin(Establishment.geometry, user_point, radius)
                )
                
            except (ValueError, TypeError):
                return jsonify({'error': 'Invalid coordinates provided'}), 400
        
        # Execute query and limit results
        establishments = query.limit(100).all()
        
        # Convert to JSON-serializable format
        results = [est.to_dict() for est in establishments]
        
        session.close()
        
        return jsonify({
            'establishments': results,
            'count': len(results),
            'filters': {
                'search': search_term,
                'type': establishment_type,
                'proximity': {
                    'lat': latitude,
                    'lon': longitude,
                    'radius': radius
                } if latitude and longitude else None
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@establishments_bp.route('/establishments/<int:establishment_id>', methods=['GET'])
def get_establishment(establishment_id):
    """Get a specific establishment by ID."""
    try:
        session = get_db_session()
        
        establishment = session.query(Establishment).filter(
            Establishment.id == establishment_id
        ).first()
        
        if not establishment:
            return jsonify({'error': 'Establishment not found'}), 404
        
        result = establishment.to_dict()
        session.close()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@establishments_bp.route('/establishments/types', methods=['GET'])
def get_establishment_types():
    """Get all available establishment types."""
    try:
        session = get_db_session()
        
        types = session.query(Establishment.type).distinct().all()
        type_list = [t[0] for t in types]
        
        session.close()
        
        return jsonify({
            'types': type_list,
            'count': len(type_list)
        })
        
    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@establishments_bp.route('/establishments/stats', methods=['GET'])
def get_establishment_stats():
    """Get statistics about establishments."""
    try:
        session = get_db_session()
        
        # Count by type
        type_counts = session.query(
            Establishment.type,
            func.count(Establishment.id).label('count')
        ).group_by(Establishment.type).all()
        
        # Total count
        total_count = session.query(Establishment).count()
        
        session.close()
        
        return jsonify({
            'total': total_count,
            'by_type': {t[0]: t[1] for t in type_counts}
        })
        
    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
