import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import {
  Fuel,
  Plus,
  Edit,
  Trash2,
  Calendar,
  Gauge,
  TrendingUp,
  ArrowLeft,
  DollarSign,
  Save,
  X
} from 'lucide-react';
import { apiService, FuelRecord, Vehicle } from '../services/apiService';

const FuelRecordsPage: React.FC = () => {
  const { vehicleId } = useParams<{ vehicleId: string }>();
  const navigate = useNavigate();
  const [vehicle, setVehicle] = useState<Vehicle | null>(null);
  const [fuelRecords, setFuelRecords] = useState<FuelRecord[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  const [showEditForm, setShowEditForm] = useState(false);
  const [editingRecord, setEditingRecord] = useState<FuelRecord | null>(null);
  const [formData, setFormData] = useState<Partial<FuelRecord>>({});

  useEffect(() => {
    if (vehicleId) {
      loadVehicle();
      loadFuelRecords();
    }
  }, [vehicleId]);

  const loadVehicle = async () => {
    try {
      const response = await apiService.getVehicle(parseInt(vehicleId!));
      setVehicle(response.vehicle);
    } catch (error) {
      console.error('Failed to load vehicle:', error);
      if (error instanceof Error && error.message.includes('401')) {
        navigate('/');
      }
    }
  };

  const loadFuelRecords = async () => {
    try {
      setIsLoading(true);
      const response = await apiService.getFuelRecords(parseInt(vehicleId!));
      setFuelRecords(response.fuel_records || []);
    } catch (error) {
      console.error('Failed to load fuel records:', error);
      if (error instanceof Error && error.message.includes('401')) {
        navigate('/');
      }
      setFuelRecords([]);
    } finally {
      setIsLoading(false);
    }
  };

  const resetForm = () => {
    setFormData({});
    setShowAddForm(false);
    setShowEditForm(false);
    setEditingRecord(null);
  };

  const getCurrentDateTime = () => {
    const now = new Date();
    const date = now.toISOString().split('T')[0];
    const time = now.toTimeString().split(' ')[0].substring(0, 5);
    return { date, time };
  };

  const handleAddRecord = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const { date, time } = getCurrentDateTime();
      const recordData = {
        ...formData,
        vehicle_id: parseInt(vehicleId!),
        record_date: formData.record_date || date,
        record_time: formData.record_time || time,
      };

      await apiService.addFuelRecord(recordData as FuelRecord);
      await loadFuelRecords();
      resetForm();
    } catch (error) {
      console.error('Failed to add fuel record:', error);
      if (error instanceof Error) {
        alert('Failed to add fuel record: ' + error.message);
      }
    }
  };

  const handleEditClick = (record: FuelRecord) => {
    setEditingRecord(record);
    setFormData(record);
    setShowEditForm(true);
  };

  const handleUpdateRecord = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingRecord) return;

    try {
      await apiService.updateFuelRecord(editingRecord.id!, formData);
      await loadFuelRecords();
      resetForm();
    } catch (error) {
      console.error('Failed to update fuel record:', error);
      if (error instanceof Error) {
        alert('Failed to update fuel record: ' + error.message);
      }
    }
  };

  const handleDeleteRecord = async (recordId: number) => {
    if (!window.confirm('Are you sure you want to delete this fuel record?')) return;

    try {
      await apiService.deleteFuelRecord(recordId);
      await loadFuelRecords();
    } catch (error) {
      console.error('Failed to delete fuel record:', error);
      if (error instanceof Error) {
        alert('Failed to delete fuel record: ' + error.message);
      }
    }
  };

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString();
  };

  const formatCurrency = (amount: number) => {
    return `$${amount.toFixed(2)}`;
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400 mb-4"></div>
          <p className="text-white">Loading fuel records...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      {/* Header */}
      <div className="bg-white/10 backdrop-blur-md border-b border-white/20 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Link to="/vehicles" className="text-gray-300 hover:text-white">
                <ArrowLeft className="w-6 h-6" />
              </Link>
              <div>
                <h1 className="text-2xl font-bold text-white flex items-center">
                  <Fuel className="w-8 h-8 mr-3 text-blue-400" />
                  Fuel Records
                </h1>
                {vehicle && (
                  <p className="text-gray-300 text-sm">{vehicle.display_name}</p>
                )}
              </div>
            </div>
            <button
              onClick={() => setShowAddForm(true)}
              className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white px-6 py-2 rounded-lg flex items-center space-x-2 transition-all duration-200"
            >
              <Plus className="w-5 h-5" />
              <span>Add Fuel Record</span>
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Summary Cards */}
        {fuelRecords.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-300 text-sm">Total Records</p>
                  <p className="text-2xl font-bold text-white">{fuelRecords.length}</p>
                </div>
                <Calendar className="w-8 h-8 text-blue-400" />
              </div>
            </div>
            <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-300 text-sm">Total Distance</p>
                  <p className="text-2xl font-bold text-white">
                    {fuelRecords.reduce((sum, record) => sum + (record.km_driven_since_last || 0), 0).toLocaleString()} km
                  </p>
                </div>
                <Gauge className="w-8 h-8 text-green-400" />
              </div>
            </div>
            <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-300 text-sm">Total Cost</p>
                  <p className="text-2xl font-bold text-white">
                    {formatCurrency(fuelRecords.reduce((sum, record) => sum + (record.total_cost || 0), 0))}
                  </p>
                </div>
                <DollarSign className="w-8 h-8 text-yellow-400" />
              </div>
            </div>
            <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-300 text-sm">Avg Consumption</p>
                  <p className="text-2xl font-bold text-white">
                    {(fuelRecords.reduce((sum, record) => sum + (record.actual_consumption_l_100km || 0), 0) / fuelRecords.filter(r => r.actual_consumption_l_100km).length || 0).toFixed(1)} L/100km
                  </p>
                </div>
                <TrendingUp className="w-8 h-8 text-purple-400" />
              </div>
            </div>
          </div>
        )}

        {/* Fuel Records List */}
        <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
          <h2 className="text-xl font-semibold text-white mb-6">Fuel Records</h2>
          
          {fuelRecords.length === 0 ? (
            <div className="text-center py-12">
              <Fuel className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-300 text-lg mb-2">No fuel records yet</p>
              <p className="text-gray-400">Add your first fuel record to start tracking consumption</p>
            </div>
          ) : (
            <div className="space-y-4">
              {fuelRecords.map((record) => (
                <div key={record.id} className="bg-white/5 border border-white/10 rounded-lg p-4 hover:bg-white/10 transition-all duration-200">
                  <div className="flex items-start justify-between">
                    <div className="flex-1 grid grid-cols-1 md:grid-cols-6 gap-4">
                      <div>
                        <p className="text-gray-300 text-xs uppercase tracking-wide mb-1">Date & Time</p>
                        <p className="text-white font-medium">{formatDate(record.record_date)}</p>
                        <p className="text-gray-400 text-sm">{record.record_time}</p>
                      </div>
                      <div>
                        <p className="text-gray-300 text-xs uppercase tracking-wide mb-1">Location</p>
                        <p className="text-white font-medium">{record.location}</p>
                        <p className="text-gray-400 text-sm capitalize">{record.driving_type}</p>
                      </div>
                      <div>
                        <p className="text-gray-300 text-xs uppercase tracking-wide mb-1">Odometer</p>
                        <p className="text-white font-medium">{record.odo_meter_current_value.toLocaleString()} km</p>
                        {record.km_driven_since_last && (
                          <p className="text-green-400 text-sm">+{record.km_driven_since_last} km</p>
                        )}
                      </div>
                      <div>
                        <p className="text-gray-300 text-xs uppercase tracking-wide mb-1">Tank Level</p>
                        <p className="text-white font-medium">{record.existing_tank_percentage}% → {record.after_refuel_percentage}%</p>
                        {record.calculated_fuel_added && (
                          <p className="text-blue-400 text-sm">+{record.calculated_fuel_added.toFixed(1)}L</p>
                        )}
                      </div>
                      <div>
                        <p className="text-gray-300 text-xs uppercase tracking-wide mb-1">Cost & Price</p>
                        <p className="text-white font-medium">{formatCurrency(record.total_cost || 0)}</p>
                        <p className="text-gray-400 text-sm">${(record.fuel_price / 100).toFixed(3)}/L</p>
                      </div>
                      <div>
                        <p className="text-gray-300 text-xs uppercase tracking-wide mb-1">Consumption</p>
                        {record.actual_consumption_l_100km ? (
                          <p className="text-white font-medium">{record.actual_consumption_l_100km.toFixed(1)} L/100km</p>
                        ) : (
                          <p className="text-gray-400">-</p>
                        )}
                      </div>
                    </div>
                    <div className="flex space-x-2 ml-4">
                      <button
                        onClick={() => handleEditClick(record)}
                        className="text-blue-400 hover:text-blue-300 p-2 hover:bg-white/10 rounded-lg transition-all duration-200"
                      >
                        <Edit className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleDeleteRecord(record.id!)}
                        className="text-red-400 hover:text-red-300 p-2 hover:bg-white/10 rounded-lg transition-all duration-200"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                  {record.notes && (
                    <div className="mt-3 pt-3 border-t border-white/10">
                      <p className="text-gray-300 text-sm">{record.notes}</p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Add Fuel Record Modal */}
      {showAddForm && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-slate-800 rounded-xl border border-white/20 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6 border-b border-white/20">
              <div className="flex items-center justify-between">
                <h3 className="text-xl font-semibold text-white flex items-center">
                  <Plus className="w-6 h-6 mr-2 text-blue-400" />
                  Add Fuel Record
                </h3>
                <button
                  onClick={resetForm}
                  className="text-gray-400 hover:text-white"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>
            </div>
            
            <form onSubmit={handleAddRecord} className="p-6 space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Date</label>
                  <input
                    type="date"
                    required
                    value={formData.record_date || getCurrentDateTime().date}
                    onChange={(e) => setFormData({...formData, record_date: e.target.value})}
                    className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Time</label>
                  <input
                    type="time"
                    required
                    value={formData.record_time || getCurrentDateTime().time}
                    onChange={(e) => setFormData({...formData, record_time: e.target.value})}
                    className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Odometer Reading (km)</label>
                  <input
                    type="number"
                    required
                    value={formData.odo_meter_current_value || ''}
                    onChange={(e) => setFormData({...formData, odo_meter_current_value: parseInt(e.target.value)})}
                    className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder={vehicle?.current_odometer?.toString()}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Location</label>
                  <input
                    type="text"
                    required
                    value={formData.location || ''}
                    onChange={(e) => setFormData({...formData, location: e.target.value})}
                    className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="e.g., Shell Station Downtown"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Tank Before Refuel (%)</label>
                  <input
                    type="number"
                    step="0.1"
                    min="0"
                    max="100"
                    required
                    value={formData.existing_tank_percentage || ''}
                    onChange={(e) => setFormData({...formData, existing_tank_percentage: parseFloat(e.target.value)})}
                    className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="25.0"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Tank After Refuel (%)</label>
                  <input
                    type="number"
                    step="0.1"
                    min="0"
                    max="100"
                    required
                    value={formData.after_refuel_percentage || ''}
                    onChange={(e) => setFormData({...formData, after_refuel_percentage: parseFloat(e.target.value)})}
                    className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="95.0"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Fuel Price (¢/L)</label>
                  <input
                    type="number"
                    step="0.1"
                    required
                    value={formData.fuel_price || ''}
                    onChange={(e) => setFormData({...formData, fuel_price: parseFloat(e.target.value)})}
                    className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="145.9"
                  />
                  <p className="text-xs text-gray-400 mt-1">Price in cents per liter (e.g., 145.9 = $1.459/L)</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Driving Type</label>
                  <select
                    required
                    value={formData.driving_type || ''}
                    onChange={(e) => setFormData({...formData, driving_type: e.target.value as 'city' | 'highway' | 'mix'})}
                    className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">Select driving type</option>
                    <option value="city">City</option>
                    <option value="highway">Highway</option>
                    <option value="mix">Mixed</option>
                  </select>
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">Notes (Optional)</label>
                <textarea
                  value={formData.notes || ''}
                  onChange={(e) => setFormData({...formData, notes: e.target.value})}
                  className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  rows={3}
                  placeholder="Any additional notes about this refuel..."
                />
              </div>

              <div className="flex space-x-4 pt-4">
                <button
                  type="submit"
                  className="flex-1 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white px-6 py-3 rounded-lg flex items-center justify-center space-x-2 transition-all duration-200"
                >
                  <Save className="w-5 h-5" />
                  <span>Add Record</span>
                </button>
                <button
                  type="button"
                  onClick={resetForm}
                  className="px-6 py-3 border border-white/20 text-gray-300 rounded-lg hover:bg-white/10 transition-all duration-200"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Edit Fuel Record Modal */}
      {showEditForm && editingRecord && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-slate-800 rounded-xl border border-white/20 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6 border-b border-white/20">
              <div className="flex items-center justify-between">
                <h3 className="text-xl font-semibold text-white flex items-center">
                  <Edit className="w-6 h-6 mr-2 text-blue-400" />
                  Edit Fuel Record
                </h3>
                <button
                  onClick={resetForm}
                  className="text-gray-400 hover:text-white"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>
            </div>
            
            <form onSubmit={handleUpdateRecord} className="p-6 space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Date</label>
                  <input
                    type="date"
                    required
                    value={formData.record_date || ''}
                    onChange={(e) => setFormData({...formData, record_date: e.target.value})}
                    className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Time</label>
                  <input
                    type="time"
                    required
                    value={formData.record_time || ''}
                    onChange={(e) => setFormData({...formData, record_time: e.target.value})}
                    className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Odometer Reading (km)</label>
                  <input
                    type="number"
                    required
                    value={formData.odo_meter_current_value || ''}
                    onChange={(e) => setFormData({...formData, odo_meter_current_value: parseInt(e.target.value)})}
                    className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Location</label>
                  <input
                    type="text"
                    required
                    value={formData.location || ''}
                    onChange={(e) => setFormData({...formData, location: e.target.value})}
                    className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Tank Before Refuel (%)</label>
                  <input
                    type="number"
                    step="0.1"
                    min="0"
                    max="100"
                    required
                    value={formData.existing_tank_percentage || ''}
                    onChange={(e) => setFormData({...formData, existing_tank_percentage: parseFloat(e.target.value)})}
                    className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Tank After Refuel (%)</label>
                  <input
                    type="number"
                    step="0.1"
                    min="0"
                    max="100"
                    required
                    value={formData.after_refuel_percentage || ''}
                    onChange={(e) => setFormData({...formData, after_refuel_percentage: parseFloat(e.target.value)})}
                    className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Fuel Price (¢/L)</label>
                  <input
                    type="number"
                    step="0.1"
                    required
                    value={formData.fuel_price || ''}
                    onChange={(e) => setFormData({...formData, fuel_price: parseFloat(e.target.value)})}
                    className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <p className="text-xs text-gray-400 mt-1">Price in cents per liter</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Driving Type</label>
                  <select
                    required
                    value={formData.driving_type || ''}
                    onChange={(e) => setFormData({...formData, driving_type: e.target.value as 'city' | 'highway' | 'mix'})}
                    className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">Select driving type</option>
                    <option value="city">City</option>
                    <option value="highway">Highway</option>
                    <option value="mix">Mixed</option>
                  </select>
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">Notes (Optional)</label>
                <textarea
                  value={formData.notes || ''}
                  onChange={(e) => setFormData({...formData, notes: e.target.value})}
                  className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  rows={3}
                />
              </div>

              <div className="flex space-x-4 pt-4">
                <button
                  type="submit"
                  className="flex-1 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white px-6 py-3 rounded-lg flex items-center justify-center space-x-2 transition-all duration-200"
                >
                  <Save className="w-5 h-5" />
                  <span>Update Record</span>
                </button>
                <button
                  type="button"
                  onClick={resetForm}
                  className="px-6 py-3 border border-white/20 text-gray-300 rounded-lg hover:bg-white/10 transition-all duration-200"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default FuelRecordsPage;