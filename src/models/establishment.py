"""
Database model for establishments using SQLAlchemy and GeoAlchemy2
"""

from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import Geometry
from geoalchemy2.functions import ST_DWithin, ST_GeomFromText
import os

Base = declarative_base()

class Establishment(Base):
    """
    Model representing a geographic establishment (pharmacy, gas station, etc.)
    """
    __tablename__ = 'establishments'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, index=True)
    type = Column(String(50), nullable=False, index=True)
    address = Column(Text)
    geometry = Column(Geometry('POINT', srid=4326), nullable=False, index=True)
    
    def __repr__(self):
        return f"<Establishment(id={self.id}, name='{self.name}', type='{self.type}')>"
    
    def to_dict(self):
        """Convert establishment to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'address': self.address,
            'coordinates': self.get_coordinates()
        }
    
    def get_coordinates(self):
        """Extract latitude and longitude from geometry."""
        # This would typically use ST_X and ST_Y functions
        # For demo purposes, returning placeholder coordinates
        return {'lat': -15.7942, 'lng': -47.8822}

# Database connection setup
def get_db_session():
    """Create and return a database session."""
    database_url = os.environ.get(
        'DATABASE_URL', 
        'postgresql://postgres:password@localhost/geoconsulta'
    )
    
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    return Session()

def create_tables():
    """Create all tables in the database."""
    database_url = os.environ.get(
        'DATABASE_URL', 
        'postgresql://postgres:password@localhost/geoconsulta'
    )
    
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    print("✅ Database tables created successfully")

if __name__ == '__main__':
    create_tables()
