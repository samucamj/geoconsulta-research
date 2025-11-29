/**
 * GeoConsulta - Main Application JavaScript
 * Handles map initialization, user interactions, and API communication
 */

class GeoConsulta {
    constructor() {
        this.map = null;
        this.markers = [];
        this.userLocation = null;
        this.searchTimeout = null;
        
        this.init();
    }
    
    init() {
        this.initializeMap();
        this.bindEvents();
        this.loadInitialData();
    }
    
    initializeMap() {
        // Initialize Leaflet map centered on Brasília
        this.map = L.map('map').setView([-15.7942, -47.8822], 12);
        
        // Add OpenStreetMap tiles
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
        }).addTo(this.map);
        
        // Add scale control
        L.control.scale().addTo(this.map);
        
        console.log('✅ Map initialized successfully');
    }
    
    bindEvents() {
        const searchInput = document.getElementById('searchInput');
        const typeFilter = document.getElementById('typeFilter');
        const locationBtn = document.getElementById('locationBtn');
        const clearBtn = document.getElementById('clearSearch');
        
        // Search input with debounce
        searchInput.addEventListener('input', (e) => {
            this.toggleClearButton(e.target.value);
            this.debounceSearch(() => this.performSearch());
        });
        
        // Type filter
        typeFilter.addEventListener('change', () => {
            this.performSearch();
        });
        
        // Location button
        locationBtn.addEventListener('click', () => {
            this.getUserLocation();
        });
        
        // Clear search button
        clearBtn.addEventListener('click', () => {
            searchInput.value = '';
            this.toggleClearButton('');
            this.performSearch();
        });
        
        console.log('✅ Event listeners bound successfully');
    }
    
    toggleClearButton(value) {
        const clearBtn = document.getElementById('clearSearch');
        clearBtn.style.display = value ? 'block' : 'none';
    }
    
    debounceSearch(callback, delay = 300) {
        clearTimeout(this.searchTimeout);
        this.searchTimeout = setTimeout(callback, delay);
    }
    
    async loadInitialData() {
        this.showLoading(true);
        await this.performSearch();
        this.showLoading(false);
    }
    
    async performSearch() {
        const searchTerm = document.getElementById('searchInput').value.trim();
        const selectedType = document.getElementById('typeFilter').value;
        
        const params = new URLSearchParams();
        
        if (searchTerm) {
            params.append('search', searchTerm);
        }
        
        if (selectedType && selectedType !== 'all') {
            params.append('type', selectedType);
        }
        
        // Add proximity search if user location is available
        if (this.userLocation) {
            params.append('lat', this.userLocation.lat);
            params.append('lon', this.userLocation.lng);
            params.append('radius', '5000'); // 5km radius
        }
        
        try {
            const response = await fetch(`/api/establishments?${params}`);
            const data = await response.json();
            
            if (response.ok) {
                this.displayResults(data.establishments);
                this.updateResultsInfo(data.count);
            } else {
                console.error('Search error:', data.error);
                this.showError('Search failed. Please try again.');
            }
        } catch (error) {
            console.error('Network error:', error);
            this.showError('Network error. Please check your connection.');
        }
    }
    
    displayResults(establishments) {
        // Clear existing markers
        this.clearMarkers();
        
        // Add new markers
        establishments.forEach(est => {
            this.addMarker(est);
        });
        
        // Fit map to show all markers if there are results
        if (establishments.length > 0) {
            const group = new L.featureGroup(this.markers);
            this.map.fitBounds(group.getBounds().pad(0.1));
        }
    }
    
    addMarker(establishment) {
        // Use demo coordinates for now (in a real app, these would come from the database)
        const lat = -15.7942 + (Math.random() - 0.5) * 0.1;
        const lng = -47.8822 + (Math.random() - 0.5) * 0.1;
        
        // Choose marker color based on type
        const color = establishment.type === 'pharmacy' ? 'red' : 'blue';
        
        // Create custom icon
        const icon = L.divIcon({
            className: 'custom-marker',
            html: `<div style="background-color: ${color}; width: 20px; height: 20px; border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>`,
            iconSize: [20, 20],
            iconAnchor: [10, 10]
        });
        
        // Create marker
        const marker = L.marker([lat, lng], { icon }).addTo(this.map);
        
        // Create popup content
        const popupContent = `
            <div class="popup-content">
                <div class="popup-title">${establishment.name}</div>
                <div class="popup-type">${this.formatType(establishment.type)}</div>
                <div class="popup-address">${establishment.address || 'Address not available'}</div>
            </div>
        `;
        
        marker.bindPopup(popupContent);
        this.markers.push(marker);
    }
    
    clearMarkers() {
        this.markers.forEach(marker => {
            this.map.removeLayer(marker);
        });
        this.markers = [];
    }
    
    formatType(type) {
        const typeMap = {
            'pharmacy': 'Pharmacy',
            'gas_station': 'Gas Station'
        };
        return typeMap[type] || type;
    }
    
    updateResultsInfo(count) {
        document.getElementById('resultCount').textContent = count;
    }
    
    getUserLocation() {
        const locationBtn = document.getElementById('locationBtn');
        
        if (!navigator.geolocation) {
            this.showError('Geolocation is not supported by this browser.');
            return;
        }
        
        locationBtn.disabled = true;
        locationBtn.innerHTML = '<span class="location-icon">⏳</span> Getting location...';
        
        navigator.geolocation.getCurrentPosition(
            (position) => {
                this.userLocation = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };
                
                // Add user location marker
                this.addUserLocationMarker();
                
                // Perform proximity search
                this.performSearch();
                
                locationBtn.disabled = false;
                locationBtn.innerHTML = '<span class="location-icon">📍</span> My Location';
                
                console.log('✅ User location obtained:', this.userLocation);
            },
            (error) => {
                console.error('Geolocation error:', error);
                this.showError('Unable to get your location. Please try again.');
                
                locationBtn.disabled = false;
                locationBtn.innerHTML = '<span class="location-icon">📍</span> My Location';
            },
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 300000 // 5 minutes
            }
        );
    }
    
    addUserLocationMarker() {
        if (this.userLocationMarker) {
            this.map.removeLayer(this.userLocationMarker);
        }
        
        const icon = L.divIcon({
            className: 'user-location-marker',
            html: '<div style="background-color: #27ae60; width: 15px; height: 15px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>',
            iconSize: [15, 15],
            iconAnchor: [7.5, 7.5]
        });
        
        this.userLocationMarker = L.marker([this.userLocation.lat, this.userLocation.lng], { icon })
            .addTo(this.map)
            .bindPopup('Your Location')
            .openPopup();
        
        // Center map on user location
        this.map.setView([this.userLocation.lat, this.userLocation.lng], 14);
    }
    
    showLoading(show) {
        const loadingIndicator = document.getElementById('loadingIndicator');
        loadingIndicator.style.display = show ? 'block' : 'none';
    }
    
    showError(message) {
        // Simple error display - in a real app, you might want a more sophisticated notification system
        alert(message);
    }
}

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Initializing GeoConsulta application...');
    new GeoConsulta();
});
