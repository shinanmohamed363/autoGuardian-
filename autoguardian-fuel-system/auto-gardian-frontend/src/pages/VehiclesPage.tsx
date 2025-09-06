import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Car,
  Plus,
  Fuel,
  Settings,
  TrendingUp,
  AlertTriangle,
  LogOut,
  Edit,
  Trash2,
  Activity,
  X,
  Save,
  Brain,
  DollarSign,
  Tag
} from 'lucide-react';
import { apiService, Vehicle } from '../services/apiService';

const VehiclesPage: React.FC = () => {
  const user = JSON.parse(localStorage.getItem('user') || '{}');
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  const [showEditForm, setShowEditForm] = useState(false);
  const [showSellForm, setShowSellForm] = useState(false);
  const [editingVehicle, setEditingVehicle] = useState<Vehicle | null>(null);
  const [sellingVehicle, setSellingVehicle] = useState<Vehicle | null>(null);
  const [formData, setFormData] = useState<Partial<Vehicle>>({});
  const [sellFormData, setSellFormData] = useState({
    selling_price: '',
    minimum_price: '',
    features: [] as string[],
    description: '',
    newFeature: ''
  });

  useEffect(() => {
    loadVehicles();
  }, []);

  const loadVehicles = async () => {
    try {
      setIsLoading(true);
      
      // Debug: Check if token exists
      const token = localStorage.getItem('access_token');
      console.log('Access Token exists:', !!token);
      console.log('Token preview:', token ? token.substring(0, 20) + '...' : 'No token');
      
      const response = await apiService.getVehicles();
      console.log('Vehicles response:', response);
      setVehicles(response.vehicles || []);
    } catch (error) {
      console.error('Failed to load vehicles:', error);
      
      // If unauthorized, redirect to login
      if (error instanceof Error && error.message.includes('401')) {
        console.log('Unauthorized - redirecting to login');
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        window.location.href = '/';
        return;
      }
      
      setVehicles([]);
    } finally {
      setIsLoading(false);
    }
  };

  const resetForm = () => {
    setFormData({});
    setShowAddForm(false);
    setShowEditForm(false);
    setEditingVehicle(null);
  };

  const resetSellForm = () => {
    setSellFormData({
      selling_price: '',
      minimum_price: '',
      features: [],
      description: '',
      newFeature: ''
    });
    setShowSellForm(false);
    setSellingVehicle(null);
  };

  const handleSellClick = (vehicle: Vehicle) => {
    setSellingVehicle(vehicle);
    setShowSellForm(true);
  };

  const addFeature = () => {
    if (sellFormData.newFeature.trim()) {
      setSellFormData(prev => ({
        ...prev,
        features: [...prev.features, prev.newFeature.trim()],
        newFeature: ''
      }));
    }
  };

  const removeFeature = (index: number) => {
    setSellFormData(prev => ({
      ...prev,
      features: prev.features.filter((_, i) => i !== index)
    }));
  };

  const handleSellSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!sellingVehicle) return;

    try {
      const selling_price = parseFloat(sellFormData.selling_price);
      const minimum_price = parseFloat(sellFormData.minimum_price);

      if (selling_price <= 0 || minimum_price <= 0) {
        alert('Please enter valid prices');
        return;
      }

      if (minimum_price > selling_price) {
        alert('Minimum price cannot be higher than selling price');
        return;
      }

      const saleData = {
        vehicle_id: sellingVehicle.id!,
        selling_price,
        minimum_price,
        features: sellFormData.features,
        description: sellFormData.description
      };

      await apiService.createVehicleSale(saleData);
      alert('Vehicle listed for sale successfully!');
      resetSellForm();
      await loadVehicles(); // Refresh vehicle list
    } catch (error) {
      console.error('Failed to list vehicle for sale:', error);
      if (error instanceof Error) {
        alert('Failed to list vehicle: ' + error.message);
      } else {
        alert('Failed to list vehicle for sale');
      }
    }
  };

  const handleAddVehicle = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      // Set defaults for optional fields
      const vehicleData = {
        ...formData,
        starting_odometer_value: formData.starting_odometer_value || 0,
        odo_meter_when_buy_vehicle: formData.odo_meter_when_buy_vehicle || formData.starting_odometer_value || 0,
        initial_tank_percentage: formData.initial_tank_percentage || 100.0
      };
      
      console.log('Adding vehicle with data:', vehicleData);
      const response = await apiService.registerVehicle(vehicleData as Vehicle);
      console.log('Add vehicle response:', response);
      await loadVehicles();
      resetForm();
    } catch (error) {
      console.error('Failed to add vehicle:', error);
      if (error instanceof Error && error.message.includes('401')) {
        alert('Session expired. Please log in again.');
        window.location.href = '/';
      } else if (error instanceof Error) {
        alert('Failed to add vehicle: ' + error.message);
      } else {
        alert('Failed to add vehicle. Please try again.');
      }
    }
  };

  const handleEditClick = (vehicle: Vehicle) => {
    setEditingVehicle(vehicle);
    setFormData(vehicle);
    setShowEditForm(true);
  };

  const handleUpdateVehicle = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingVehicle) return;
    
    try {
      await apiService.updateVehicle(editingVehicle.id!, formData);
      await loadVehicles();
      resetForm();
    } catch (error) {
      console.error('Failed to update vehicle:', error);
    }
  };

  const handleDeleteVehicle = async (vehicleId: number) => {
    if (!window.confirm('Are you sure you want to delete this vehicle?')) return;
    
    try {
      await apiService.deleteVehicle(vehicleId);
      await loadVehicles();
    } catch (error) {
      console.error('Failed to delete vehicle:', error);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    window.location.href = '/';
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400 mb-4"></div>
          <p className="text-white">Loading your vehicles...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      {/* Navigation */}
      <nav className="bg-white/10 backdrop-blur-md border-b border-white/20 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-8">
              <div className="text-2xl font-bold text-white">AutoGuardian</div>
              <div className="hidden md:flex space-x-6">
                <Link to="/dashboard" className="text-gray-300 hover:text-white transition-colors">Dashboard</Link>
                <Link to="/vehicles" className="text-white hover:text-blue-300 transition-colors">Vehicles</Link>
                <Link to="/analytics" className="text-gray-300 hover:text-white transition-colors">Analytics</Link>
                <Link to="/recommendations" className="text-gray-300 hover:text-white transition-colors">AI Insights</Link>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-gray-300">Welcome, {user.first_name}!</span>
              <button
                onClick={handleLogout}
                className="flex items-center space-x-2 bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg transition-colors duration-200"
              >
                <LogOut size={16} />
                <span>Logout</span>
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold text-white mb-2">My Vehicles</h1>
            <p className="text-xl text-gray-300">Manage your vehicle fleet and track performance</p>
          </div>
          <button
            onClick={() => setShowAddForm(true)}
            className="flex items-center space-x-2 bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg transition-colors duration-200"
          >
            <Plus size={20} />
            <span>Add Vehicle</span>
          </button>
        </div>

        {/* Vehicles Grid */}
        {vehicles.length > 0 ? (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {vehicles.map((vehicle) => (
              <div key={vehicle.id} className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6 hover:bg-white/15 transition-all duration-200">
                <div className="flex justify-between items-start mb-4">
                  <div className="bg-blue-600/20 p-3 rounded-lg">
                    <Car className="text-blue-400" size={32} />
                  </div>
                  <div className="flex space-x-2">
                    <button 
                      onClick={() => handleSellClick(vehicle)}
                      className="p-2 bg-green-600/20 hover:bg-green-600/30 rounded-lg transition-colors"
                      title="List for sale"
                    >
                      <DollarSign className="text-green-400" size={16} />
                    </button>
                    <button 
                      onClick={() => handleEditClick(vehicle)}
                      className="p-2 bg-white/10 hover:bg-white/20 rounded-lg transition-colors"
                    >
                      <Edit className="text-gray-300" size={16} />
                    </button>
                    <button 
                      onClick={() => handleDeleteVehicle(vehicle.id!)}
                      className="p-2 bg-red-600/20 hover:bg-red-600/30 rounded-lg transition-colors"
                    >
                      <Trash2 className="text-red-400" size={16} />
                    </button>
                  </div>
                </div>

                <h3 className="text-xl font-semibold text-white mb-2">{vehicle.vehicle_name}</h3>
                <p className="text-gray-300 mb-4">{vehicle.year} {vehicle.make} {vehicle.model}</p>

                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div className="bg-white/5 rounded-lg p-3">
                    <p className="text-gray-400 text-xs">Engine</p>
                    <p className="text-white font-semibold">{vehicle.engine_size}L</p>
                  </div>
                  <div className="bg-white/5 rounded-lg p-3">
                    <p className="text-gray-400 text-xs">Fuel Type</p>
                    <p className="text-white font-semibold">{vehicle.fuel_type}</p>
                  </div>
                  <div className="bg-white/5 rounded-lg p-3">
                    <p className="text-gray-400 text-xs">Tank Capacity</p>
                    <p className="text-white font-semibold">{vehicle.tank_capacity}L</p>
                  </div>
                  <div className="bg-white/5 rounded-lg p-3">
                    <p className="text-gray-400 text-xs">Class</p>
                    <p className="text-white font-semibold">{vehicle.vehicle_class}</p>
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-2">
                  <Link
                    to={`/fuel-records/${vehicle.id}`}
                    className="flex items-center justify-center space-x-1 bg-green-600/20 hover:bg-green-600/30 text-green-400 py-2 px-2 rounded-lg transition-colors text-xs"
                  >
                    <Fuel size={14} />
                    <span>Fuel</span>
                  </Link>
                  <Link
                    to={`/ai-insights/${vehicle.id}`}
                    className="flex items-center justify-center space-x-1 bg-purple-600/20 hover:bg-purple-600/30 text-purple-400 py-2 px-2 rounded-lg transition-colors text-xs"
                  >
                    <Brain size={14} />
                    <span>AI Insights</span>
                  </Link>
                  <Link
                    to={`/vehicle/${vehicle.id}/analytics`}
                    className="flex items-center justify-center space-x-1 bg-blue-600/20 hover:bg-blue-600/30 text-blue-400 py-2 px-2 rounded-lg transition-colors text-xs"
                  >
                    <TrendingUp size={14} />
                    <span>Analytics</span>
                  </Link>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-16">
            <div className="bg-white/5 backdrop-blur-md border border-white/20 rounded-2xl p-12 max-w-md mx-auto">
              <Car size={64} className="mx-auto mb-6 text-gray-400 opacity-50" />
              <h2 className="text-2xl font-semibold text-white mb-4">No Vehicles Yet</h2>
              <p className="text-gray-300 mb-6">Start by adding your first vehicle to begin tracking fuel efficiency and getting AI insights.</p>
              <button
                onClick={() => setShowAddForm(true)}
                className="flex items-center space-x-2 bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg transition-colors duration-200 mx-auto"
              >
                <Plus size={20} />
                <span>Add Your First Vehicle</span>
              </button>
            </div>
          </div>
        )}

        {/* Quick Stats */}
        <div className="mt-12 grid md:grid-cols-4 gap-6">
          <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Total Vehicles</p>
                <p className="text-2xl font-bold text-white">{vehicles.length}</p>
              </div>
              <Car className="text-blue-400" size={24} />
            </div>
          </div>

          <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Active Vehicles</p>
                <p className="text-2xl font-bold text-white">{vehicles.length}</p>
              </div>
              <Activity className="text-green-400" size={24} />
            </div>
          </div>

          <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Alerts</p>
                <p className="text-2xl font-bold text-white">0</p>
              </div>
              <AlertTriangle className="text-yellow-400" size={24} />
            </div>
          </div>

          <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Maintenance Due</p>
                <p className="text-2xl font-bold text-white">0</p>
              </div>
              <Settings className="text-purple-400" size={24} />
            </div>
          </div>
        </div>

        {/* Add Vehicle Modal */}
        {showAddForm && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
            <div className="bg-slate-800 border border-white/20 rounded-xl p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-white">Add New Vehicle</h2>
                <button onClick={resetForm} className="text-gray-400 hover:text-white">
                  <X size={24} />
                </button>
              </div>
              
              <form onSubmit={handleAddVehicle} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {/* Vehicle ID is auto-generated, no need for input field */}
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-1">Vehicle Name</label>
                    <input
                      type="text"
                      required
                      value={formData.vehicle_name || ''}
                      onChange={(e) => setFormData({...formData, vehicle_name: e.target.value})}
                      className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400"
                      placeholder="e.g. My Daily Driver"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-1">Make</label>
                    <input
                      type="text"
                      required
                      value={formData.make || ''}
                      onChange={(e) => setFormData({...formData, make: e.target.value})}
                      className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400"
                      placeholder="e.g. Toyota"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-1">Model</label>
                    <input
                      type="text"
                      required
                      value={formData.model || ''}
                      onChange={(e) => setFormData({...formData, model: e.target.value})}
                      className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400"
                      placeholder="e.g. Camry"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-1">Year</label>
                    <input
                      type="number"
                      required
                      min="1900"
                      max="2025"
                      value={formData.year || ''}
                      onChange={(e) => setFormData({...formData, year: parseInt(e.target.value)})}
                      className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400"
                      placeholder="2020"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-1">Vehicle Class</label>
                    <input
                      type="text"
                      required
                      value={formData.vehicle_class || ''}
                      onChange={(e) => setFormData({...formData, vehicle_class: e.target.value})}
                      className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400"
                      placeholder="e.g. Mid-size"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-1">Engine Size (L)</label>
                    <input
                      type="number"
                      step="0.1"
                      required
                      value={formData.engine_size || ''}
                      onChange={(e) => setFormData({...formData, engine_size: parseFloat(e.target.value)})}
                      className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400"
                      placeholder="2.5"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-1">Cylinders</label>
                    <input
                      type="number"
                      required
                      min="1"
                      max="16"
                      value={formData.cylinders || ''}
                      onChange={(e) => setFormData({...formData, cylinders: parseInt(e.target.value)})}
                      className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400"
                      placeholder="4"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-1">Transmission</label>
                    <select
                      required
                      value={formData.transmission || ''}
                      onChange={(e) => setFormData({...formData, transmission: e.target.value})}
                      className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white"
                    >
                      <option value="">Select transmission</option>
                      <option value="Manual">Manual</option>
                      <option value="Automatic">Automatic</option>
                      <option value="CVT">CVT</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-1">Fuel Type</label>
                    <select
                      required
                      value={formData.fuel_type || ''}
                      onChange={(e) => setFormData({...formData, fuel_type: e.target.value})}
                      className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white"
                    >
                      <option value="">Select fuel type</option>
                      <option value="Regular Gasoline">Regular Gasoline</option>
                      <option value="Premium Gasoline">Premium Gasoline</option>
                      <option value="Diesel">Diesel</option>
                      <option value="Hybrid">Hybrid</option>
                      <option value="Electric">Electric</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-1">Tank Capacity (L)</label>
                    <input
                      type="number"
                      step="0.1"
                      required
                      value={formData.tank_capacity || ''}
                      onChange={(e) => setFormData({...formData, tank_capacity: parseFloat(e.target.value)})}
                      className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400"
                      placeholder="50"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-1">Full Tank Capacity (L)</label>
                    <input
                      type="number"
                      step="0.1"
                      required
                      value={formData.full_tank_capacity || formData.tank_capacity || ''}
                      onChange={(e) => setFormData({...formData, full_tank_capacity: parseFloat(e.target.value)})}
                      className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400"
                      placeholder="50"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-1">Starting Odometer</label>
                    <input
                      type="number"
                      value={formData.starting_odometer_value || ''}
                      onChange={(e) => setFormData({...formData, starting_odometer_value: parseInt(e.target.value)})}
                      className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400"
                      placeholder="0"
                    />
                  </div>
                </div>
                
                <div className="flex space-x-4 pt-4">
                  <button
                    type="submit"
                    className="flex-1 flex items-center justify-center space-x-2 bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg transition-colors"
                  >
                    <Save size={16} />
                    <span>Add Vehicle</span>
                  </button>
                  <button
                    type="button"
                    onClick={resetForm}
                    className="flex-1 bg-gray-600 hover:bg-gray-700 text-white py-2 px-4 rounded-lg transition-colors"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Edit Vehicle Modal */}
        {showEditForm && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
            <div className="bg-slate-800 border border-white/20 rounded-xl p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-white">Edit Vehicle</h2>
                <button onClick={resetForm} className="text-gray-400 hover:text-white">
                  <X size={24} />
                </button>
              </div>
              
              <form onSubmit={handleUpdateVehicle} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-1">Vehicle Name</label>
                    <input
                      type="text"
                      required
                      value={formData.vehicle_name || ''}
                      onChange={(e) => setFormData({...formData, vehicle_name: e.target.value})}
                      className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400"
                      placeholder="e.g. My Daily Driver"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-1">Make</label>
                    <input
                      type="text"
                      required
                      value={formData.make || ''}
                      onChange={(e) => setFormData({...formData, make: e.target.value})}
                      className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400"
                      placeholder="e.g. Toyota"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-1">Model</label>
                    <input
                      type="text"
                      required
                      value={formData.model || ''}
                      onChange={(e) => setFormData({...formData, model: e.target.value})}
                      className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400"
                      placeholder="e.g. Camry"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-1">Year</label>
                    <input
                      type="number"
                      required
                      min="1900"
                      max="2025"
                      value={formData.year || ''}
                      onChange={(e) => setFormData({...formData, year: parseInt(e.target.value)})}
                      className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400"
                      placeholder="2020"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-1">Vehicle Class</label>
                    <input
                      type="text"
                      required
                      value={formData.vehicle_class || ''}
                      onChange={(e) => setFormData({...formData, vehicle_class: e.target.value})}
                      className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400"
                      placeholder="e.g. Mid-size"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-1">Engine Size (L)</label>
                    <input
                      type="number"
                      step="0.1"
                      required
                      value={formData.engine_size || ''}
                      onChange={(e) => setFormData({...formData, engine_size: parseFloat(e.target.value)})}
                      className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400"
                      placeholder="2.5"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-1">Cylinders</label>
                    <input
                      type="number"
                      required
                      min="1"
                      max="16"
                      value={formData.cylinders || ''}
                      onChange={(e) => setFormData({...formData, cylinders: parseInt(e.target.value)})}
                      className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400"
                      placeholder="4"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-1">Transmission</label>
                    <select
                      required
                      value={formData.transmission || ''}
                      onChange={(e) => setFormData({...formData, transmission: e.target.value})}
                      className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white"
                    >
                      <option value="">Select transmission</option>
                      <option value="Manual">Manual</option>
                      <option value="Automatic">Automatic</option>
                      <option value="CVT">CVT</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-1">Fuel Type</label>
                    <select
                      required
                      value={formData.fuel_type || ''}
                      onChange={(e) => setFormData({...formData, fuel_type: e.target.value})}
                      className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white"
                    >
                      <option value="">Select fuel type</option>
                      <option value="Regular Gasoline">Regular Gasoline</option>
                      <option value="Premium Gasoline">Premium Gasoline</option>
                      <option value="Diesel">Diesel</option>
                      <option value="Hybrid">Hybrid</option>
                      <option value="Electric">Electric</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-1">Tank Capacity (L)</label>
                    <input
                      type="number"
                      step="0.1"
                      required
                      value={formData.tank_capacity || ''}
                      onChange={(e) => setFormData({...formData, tank_capacity: parseFloat(e.target.value)})}
                      className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400"
                      placeholder="50"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-1">Full Tank Capacity (L)</label>
                    <input
                      type="number"
                      step="0.1"
                      required
                      value={formData.full_tank_capacity || formData.tank_capacity || ''}
                      onChange={(e) => setFormData({...formData, full_tank_capacity: parseFloat(e.target.value)})}
                      className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400"
                      placeholder="50"
                    />
                  </div>
                </div>
                
                <div className="flex space-x-4 pt-4">
                  <button
                    type="submit"
                    className="flex-1 flex items-center justify-center space-x-2 bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg transition-colors"
                  >
                    <Save size={16} />
                    <span>Update Vehicle</span>
                  </button>
                  <button
                    type="button"
                    onClick={resetForm}
                    className="flex-1 bg-gray-600 hover:bg-gray-700 text-white py-2 px-4 rounded-lg transition-colors"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Sell Vehicle Modal */}
        {showSellForm && sellingVehicle && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
            <div className="bg-slate-800 border border-white/20 rounded-xl p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-white">List Vehicle for Sale</h2>
                <button onClick={resetSellForm} className="text-gray-400 hover:text-white">
                  <X size={24} />
                </button>
              </div>
              
              <div className="mb-4 p-4 bg-white/5 rounded-lg">
                <p className="text-gray-300 text-sm mb-1">Selected Vehicle</p>
                <p className="text-white font-semibold">{sellingVehicle.year} {sellingVehicle.make} {sellingVehicle.model}</p>
                <p className="text-gray-400 text-sm">{sellingVehicle.vehicle_name}</p>
              </div>
              
              <form onSubmit={handleSellSubmit} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-1">
                      Selling Price (Rs.) <span className="text-red-400">*</span>
                    </label>
                    <input
                      type="number"
                      required
                      min="0"
                      step="1000"
                      value={sellFormData.selling_price}
                      onChange={(e) => setSellFormData({...sellFormData, selling_price: e.target.value})}
                      className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400"
                      placeholder="e.g. 1200000"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-1">
                      Minimum Price (Rs.) <span className="text-red-400">*</span>
                    </label>
                    <input
                      type="number"
                      required
                      min="0"
                      step="1000"
                      value={sellFormData.minimum_price}
                      onChange={(e) => setSellFormData({...sellFormData, minimum_price: e.target.value})}
                      className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400"
                      placeholder="e.g. 1000000"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Additional Features & Improvements</label>
                  <div className="flex space-x-2 mb-2">
                    <input
                      type="text"
                      value={sellFormData.newFeature}
                      onChange={(e) => setSellFormData({...sellFormData, newFeature: e.target.value})}
                      className="flex-1 px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400"
                      placeholder="e.g. New tires, Brand new condition, New engine oil"
                      onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addFeature())}
                    />
                    <button
                      type="button"
                      onClick={addFeature}
                      className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
                    >
                      <Plus size={16} />
                    </button>
                  </div>
                  
                  {sellFormData.features.length > 0 && (
                    <div className="space-y-2">
                      {sellFormData.features.map((feature, index) => (
                        <div key={index} className="flex items-center space-x-2 bg-white/5 p-2 rounded-lg">
                          <Tag className="text-blue-400" size={14} />
                          <span className="text-white flex-1">{feature}</span>
                          <button
                            type="button"
                            onClick={() => removeFeature(index)}
                            className="p-1 bg-red-600/20 hover:bg-red-600/30 rounded transition-colors"
                          >
                            <X className="text-red-400" size={12} />
                          </button>
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Description (Optional)</label>
                  <textarea
                    value={sellFormData.description}
                    onChange={(e) => setSellFormData({...sellFormData, description: e.target.value})}
                    rows={3}
                    className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400"
                    placeholder="Additional details about your vehicle..."
                  />
                </div>

                <div className="bg-blue-600/10 p-4 rounded-lg">
                  <h4 className="text-blue-300 font-medium mb-2">💡 Selling Tips:</h4>
                  <ul className="text-sm text-gray-300 space-y-1">
                    <li>• Set a competitive selling price based on market value</li>
                    <li>• Your minimum price won't be shown publicly</li>
                    <li>• Add features like "New tires", "Recent service", "Accident-free"</li>
                    <li>• Buyers can negotiate through our AI-powered chat system</li>
                  </ul>
                </div>
                
                <div className="flex space-x-4 pt-4">
                  <button
                    type="submit"
                    className="flex-1 flex items-center justify-center space-x-2 bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded-lg transition-colors"
                  >
                    <DollarSign size={16} />
                    <span>List for Sale</span>
                  </button>
                  <button
                    type="button"
                    onClick={resetSellForm}
                    className="flex-1 bg-gray-600 hover:bg-gray-700 text-white py-2 px-4 rounded-lg transition-colors"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default VehiclesPage;