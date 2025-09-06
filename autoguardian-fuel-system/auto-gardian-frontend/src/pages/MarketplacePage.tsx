import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Car,
  Search,
  Filter,
  MapPin,
  Calendar,
  Fuel,
  Settings,
  MessageCircle,
  Heart,
  Eye,
  ArrowLeft,
  ChevronDown,
  X
} from 'lucide-react';
import { apiService, VehicleSale } from '../services/apiService';

const MarketplacePage: React.FC = () => {
  const navigate = useNavigate();
  const [vehicles, setVehicles] = useState<VehicleSale[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [showFilters, setShowFilters] = useState(false);
  const [filters, setFilters] = useState({
    make: '',
    priceRange: 'all',
    fuelType: '',
    yearRange: 'all',
    transmission: ''
  });

  useEffect(() => {
    loadMarketplace();
  }, []);

  const loadMarketplace = async () => {
    try {
      setIsLoading(true);
      const response = await apiService.getVehicleSales({ limit: 50 });
      console.log('Marketplace vehicles:', response);
      setVehicles(response.vehicle_sales || []);
    } catch (error) {
      console.error('Failed to load marketplace:', error);
      setVehicles([]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleVehicleClick = (vehicleId: number) => {
    navigate(`/marketplace/${vehicleId}`);
  };

  const filteredVehicles = vehicles.filter(vehicle => {
    const matchesSearch = !searchTerm || 
      vehicle.vehicle?.vehicle_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      vehicle.vehicle?.make?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      vehicle.vehicle?.model?.toLowerCase().includes(searchTerm.toLowerCase());

    const matchesMake = !filters.make || vehicle.vehicle?.make === filters.make;
    const matchesFuelType = !filters.fuelType || vehicle.vehicle?.fuel_type === filters.fuelType;
    const matchesTransmission = !filters.transmission || vehicle.vehicle?.transmission === filters.transmission;

    let matchesPrice = true;
    if (filters.priceRange !== 'all') {
      const price = vehicle.selling_price;
      switch (filters.priceRange) {
        case 'under-500k': matchesPrice = price < 500000; break;
        case '500k-1m': matchesPrice = price >= 500000 && price < 1000000; break;
        case '1m-2m': matchesPrice = price >= 1000000 && price < 2000000; break;
        case 'over-2m': matchesPrice = price >= 2000000; break;
      }
    }

    let matchesYear = true;
    if (filters.yearRange !== 'all' && vehicle.vehicle?.year) {
      const year = vehicle.vehicle.year;
      const currentYear = new Date().getFullYear();
      switch (filters.yearRange) {
        case 'new': matchesYear = year >= currentYear - 2; break;
        case 'recent': matchesYear = year >= currentYear - 5 && year < currentYear - 2; break;
        case 'older': matchesYear = year < currentYear - 5; break;
      }
    }

    return matchesSearch && matchesMake && matchesFuelType && matchesTransmission && matchesPrice && matchesYear;
  });

  const uniqueMakes = Array.from(new Set(vehicles.map(v => v.vehicle?.make).filter(Boolean)));
  const uniqueFuelTypes = Array.from(new Set(vehicles.map(v => v.vehicle?.fuel_type).filter(Boolean)));

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('en-LK', {
      style: 'currency',
      currency: 'LKR',
      minimumFractionDigits: 0
    }).format(price);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400 mb-4"></div>
          <p className="text-white">Loading marketplace...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      {/* Header */}
      <div className="bg-white/10 backdrop-blur-md border-b border-white/20 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => navigate('/dashboard')}
                className="flex items-center space-x-2 text-gray-300 hover:text-white transition-colors"
              >
                <ArrowLeft size={20} />
                <span>Back to Dashboard</span>
              </button>
              <div className="h-6 w-px bg-white/20"></div>
              <h1 className="text-2xl font-bold text-white">Vehicle Marketplace</h1>
            </div>
            <div className="text-sm text-gray-300">
              {filteredVehicles.length} vehicles available
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Search and Filters */}
        <div className="mb-8 space-y-4">
          {/* Search Bar */}
          <div className="relative">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
            <input
              type="text"
              placeholder="Search by make, model, or vehicle name..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-12 pr-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* Filter Toggle */}
          <div className="flex justify-between items-center">
            <button
              onClick={() => setShowFilters(!showFilters)}
              className="flex items-center space-x-2 bg-white/10 hover:bg-white/20 px-4 py-2 rounded-lg transition-colors text-white"
            >
              <Filter size={16} />
              <span>Filters</span>
              <ChevronDown className={`transform transition-transform ${showFilters ? 'rotate-180' : ''}`} size={16} />
            </button>

            {Object.values(filters).some(f => f && f !== 'all') && (
              <button
                onClick={() => setFilters({
                  make: '',
                  priceRange: 'all',
                  fuelType: '',
                  yearRange: 'all',
                  transmission: ''
                })}
                className="flex items-center space-x-2 text-red-400 hover:text-red-300 transition-colors"
              >
                <X size={16} />
                <span>Clear Filters</span>
              </button>
            )}
          </div>

          {/* Filter Panel */}
          {showFilters && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 p-4 bg-white/5 rounded-xl border border-white/20">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Make</label>
                <select
                  value={filters.make}
                  onChange={(e) => setFilters({...filters, make: e.target.value})}
                  className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white"
                >
                  <option value="">All Makes</option>
                  {uniqueMakes.map(make => (
                    <option key={make} value={make}>{make}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Price Range</label>
                <select
                  value={filters.priceRange}
                  onChange={(e) => setFilters({...filters, priceRange: e.target.value})}
                  className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white"
                >
                  <option value="all">All Prices</option>
                  <option value="under-500k">Under Rs. 500,000</option>
                  <option value="500k-1m">Rs. 500K - 1M</option>
                  <option value="1m-2m">Rs. 1M - 2M</option>
                  <option value="over-2m">Over Rs. 2M</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Fuel Type</label>
                <select
                  value={filters.fuelType}
                  onChange={(e) => setFilters({...filters, fuelType: e.target.value})}
                  className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white"
                >
                  <option value="">All Fuel Types</option>
                  {uniqueFuelTypes.map(fuel => (
                    <option key={fuel} value={fuel}>{fuel}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Year</label>
                <select
                  value={filters.yearRange}
                  onChange={(e) => setFilters({...filters, yearRange: e.target.value})}
                  className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white"
                >
                  <option value="all">All Years</option>
                  <option value="new">2022 & Newer</option>
                  <option value="recent">2019 - 2021</option>
                  <option value="older">Before 2019</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Transmission</label>
                <select
                  value={filters.transmission}
                  onChange={(e) => setFilters({...filters, transmission: e.target.value})}
                  className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white"
                >
                  <option value="">All Types</option>
                  <option value="Automatic">Automatic</option>
                  <option value="Manual">Manual</option>
                  <option value="CVT">CVT</option>
                </select>
              </div>
            </div>
          )}
        </div>

        {/* Vehicle Grid */}
        {filteredVehicles.length > 0 ? (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {filteredVehicles.map((vehicleSale) => (
              <div
                key={vehicleSale.id}
                onClick={() => handleVehicleClick(vehicleSale.id)}
                className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-4 hover:bg-white/15 transition-all duration-200 cursor-pointer group"
              >
                {/* Vehicle Image Placeholder */}
                <div className="bg-gradient-to-br from-blue-600/20 to-purple-600/20 rounded-lg h-48 mb-4 flex items-center justify-center">
                  <Car className="text-blue-400 group-hover:text-blue-300 transition-colors" size={48} />
                </div>

                {/* Vehicle Info */}
                <div className="space-y-3">
                  <div>
                    <h3 className="text-lg font-semibold text-white group-hover:text-blue-300 transition-colors">
                      {vehicleSale.vehicle?.year} {vehicleSale.vehicle?.make} {vehicleSale.vehicle?.model}
                    </h3>
                    <p className="text-gray-400 text-sm">{vehicleSale.vehicle?.vehicle_name}</p>
                  </div>

                  {/* Price */}
                  <div className="text-2xl font-bold text-green-400">
                    {formatPrice(vehicleSale.selling_price)}
                  </div>

                  {/* Features */}
                  {vehicleSale.features && vehicleSale.features.length > 0 && (
                    <div className="flex flex-wrap gap-1">
                      {vehicleSale.features.slice(0, 2).map((feature, index) => (
                        <span
                          key={index}
                          className="px-2 py-1 bg-blue-600/20 text-blue-300 text-xs rounded-full"
                        >
                          {feature}
                        </span>
                      ))}
                      {vehicleSale.features.length > 2 && (
                        <span className="px-2 py-1 bg-gray-600/20 text-gray-300 text-xs rounded-full">
                          +{vehicleSale.features.length - 2} more
                        </span>
                      )}
                    </div>
                  )}

                  {/* Vehicle Details */}
                  <div className="grid grid-cols-2 gap-2 text-sm">
                    <div className="flex items-center space-x-1 text-gray-400">
                      <Fuel size={14} />
                      <span>{vehicleSale.vehicle?.fuel_type}</span>
                    </div>
                    <div className="flex items-center space-x-1 text-gray-400">
                      <Settings size={14} />
                      <span>{vehicleSale.vehicle?.transmission}</span>
                    </div>
                    <div className="flex items-center space-x-1 text-gray-400">
                      <Calendar size={14} />
                      <span>{vehicleSale.vehicle?.year}</span>
                    </div>
                    <div className="flex items-center space-x-1 text-gray-400">
                      <MapPin size={14} />
                      <span>{vehicleSale.seller?.location || 'Colombo'}</span>
                    </div>
                  </div>

                  {/* Action Buttons */}
                  <div className="flex space-x-2 pt-2">
                    <button className="flex-1 flex items-center justify-center space-x-1 bg-blue-600/20 hover:bg-blue-600/30 text-blue-400 py-2 px-3 rounded-lg transition-colors text-sm">
                      <Eye size={14} />
                      <span>View Details</span>
                    </button>
                    <button className="flex items-center justify-center space-x-1 bg-green-600/20 hover:bg-green-600/30 text-green-400 py-2 px-3 rounded-lg transition-colors text-sm">
                      <MessageCircle size={14} />
                      <span>Chat</span>
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-16">
            <div className="bg-white/5 backdrop-blur-md border border-white/20 rounded-2xl p-12 max-w-md mx-auto">
              <Search size={64} className="mx-auto mb-6 text-gray-400 opacity-50" />
              <h2 className="text-2xl font-semibold text-white mb-4">No vehicles found</h2>
              <p className="text-gray-300 mb-6">
                {searchTerm || Object.values(filters).some(f => f && f !== 'all') 
                  ? 'Try adjusting your search or filters'
                  : 'No vehicles are currently listed for sale'}
              </p>
              {(searchTerm || Object.values(filters).some(f => f && f !== 'all')) && (
                <button
                  onClick={() => {
                    setSearchTerm('');
                    setFilters({
                      make: '',
                      priceRange: 'all',
                      fuelType: '',
                      yearRange: 'all',
                      transmission: ''
                    });
                  }}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg transition-colors duration-200"
                >
                  Clear Search & Filters
                </button>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default MarketplacePage;