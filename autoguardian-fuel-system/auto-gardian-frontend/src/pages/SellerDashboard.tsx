import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  Car,
  MessageCircle,
  DollarSign,
  Eye,
  EyeOff,
  Calendar,
  User,
  Mail,
  Phone,
  CheckCircle,
  XCircle,
  Clock,
  ArrowLeft,
  Edit,
  Trash2,
  Plus
} from 'lucide-react';
import { apiService, VehicleSale, Negotiation } from '../services/apiService';

const SellerDashboard: React.FC = () => {
  const navigate = useNavigate();
  const [vehicleSales, setVehicleSales] = useState<VehicleSale[]>([]);
  const [selectedSale, setSelectedSale] = useState<VehicleSale | null>(null);
  const [negotiations, setNegotiations] = useState<Negotiation[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'sales' | 'negotiations'>('sales');

  useEffect(() => {
    loadSellerData();
  }, []);

  const loadSellerData = async () => {
    try {
      setIsLoading(true);
      const salesResponse = await apiService.getMyVehicleSales();
      console.log('My vehicle sales:', salesResponse);
      setVehicleSales(salesResponse.vehicle_sales || []);
    } catch (error) {
      console.error('Failed to load seller data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadNegotiations = async (saleId: number) => {
    try {
      const response = await apiService.getSaleNegotiations(saleId);
      console.log('Negotiations for sale:', response);
      setNegotiations(response.negotiations || []);
    } catch (error) {
      console.error('Failed to load negotiations:', error);
      setNegotiations([]);
    }
  };

  const handleAcceptNegotiation = async (negotiationId: number) => {
    if (!window.confirm('Accept this offer? This will mark the vehicle as sold.')) return;
    
    try {
      await apiService.acceptNegotiation(negotiationId);
      alert('Offer accepted! The vehicle has been marked as sold.');
      loadSellerData();
      if (selectedSale) {
        loadNegotiations(selectedSale.id);
      }
    } catch (error) {
      console.error('Failed to accept negotiation:', error);
      alert('Failed to accept offer');
    }
  };

  const handleRejectNegotiation = async (negotiationId: number) => {
    if (!window.confirm('Reject this offer?')) return;
    
    try {
      await apiService.rejectNegotiation(negotiationId);
      alert('Offer rejected');
      if (selectedSale) {
        loadNegotiations(selectedSale.id);
      }
    } catch (error) {
      console.error('Failed to reject negotiation:', error);
      alert('Failed to reject offer');
    }
  };

  const handleDeleteSale = async (saleId: number) => {
    if (!window.confirm('Remove this vehicle from sale?')) return;
    
    try {
      await apiService.deleteVehicleSale(saleId);
      alert('Vehicle removed from sale');
      loadSellerData();
      if (selectedSale?.id === saleId) {
        setSelectedSale(null);
        setNegotiations([]);
      }
    } catch (error) {
      console.error('Failed to delete sale:', error);
      alert('Failed to remove vehicle from sale');
    }
  };

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('en-LK', {
      style: 'currency',
      currency: 'LKR',
      minimumFractionDigits: 0
    }).format(price);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending': return 'text-yellow-400 bg-yellow-400/20';
      case 'accepted': return 'text-green-400 bg-green-400/20';
      case 'rejected': return 'text-red-400 bg-red-400/20';
      default: return 'text-gray-400 bg-gray-400/20';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'pending': return <Clock size={16} />;
      case 'accepted': return <CheckCircle size={16} />;
      case 'rejected': return <XCircle size={16} />;
      default: return <Clock size={16} />;
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400 mb-4"></div>
          <p className="text-white">Loading seller dashboard...</p>
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
              <h1 className="text-2xl font-bold text-white">Seller Dashboard</h1>
            </div>
            <Link
              to="/vehicles"
              className="flex items-center space-x-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
            >
              <Plus size={16} />
              <span>List New Vehicle</span>
            </Link>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Summary Stats */}
        <div className="grid md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Active Listings</p>
                <p className="text-2xl font-bold text-white">
                  {vehicleSales.filter(sale => sale.is_active && !sale.is_sold).length}
                </p>
              </div>
              <Car className="text-blue-400" size={24} />
            </div>
          </div>

          <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Total Negotiations</p>
                <p className="text-2xl font-bold text-white">
                  {vehicleSales.reduce((total, sale) => total + (sale.negotiations_count || 0), 0)}
                </p>
              </div>
              <MessageCircle className="text-green-400" size={24} />
            </div>
          </div>

          <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Vehicles Sold</p>
                <p className="text-2xl font-bold text-white">
                  {vehicleSales.filter(sale => sale.is_sold).length}
                </p>
              </div>
              <CheckCircle className="text-purple-400" size={24} />
            </div>
          </div>

          <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Total Value</p>
                <p className="text-2xl font-bold text-white">
                  {formatPrice(vehicleSales.reduce((total, sale) => total + sale.selling_price, 0))}
                </p>
              </div>
              <DollarSign className="text-yellow-400" size={24} />
            </div>
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Vehicle Sales List */}
          <div className="lg:col-span-2">
            <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl">
              <div className="p-6 border-b border-white/20">
                <h2 className="text-xl font-bold text-white">My Vehicle Sales</h2>
                <p className="text-gray-400 text-sm mt-1">Manage your listed vehicles</p>
              </div>

              <div className="p-6">
                {vehicleSales.length > 0 ? (
                  <div className="space-y-4">
                    {vehicleSales.map((sale) => (
                      <div
                        key={sale.id}
                        className={`p-4 rounded-lg border transition-all cursor-pointer ${
                          selectedSale?.id === sale.id
                            ? 'bg-blue-600/20 border-blue-600/40'
                            : 'bg-white/5 border-white/10 hover:bg-white/10'
                        }`}
                        onClick={() => {
                          setSelectedSale(sale);
                          loadNegotiations(sale.id);
                        }}
                      >
                        <div className="flex justify-between items-start">
                          <div className="flex-1">
                            <div className="flex items-center space-x-2 mb-2">
                              <h3 className="text-lg font-semibold text-white">
                                {sale.vehicle?.year} {sale.vehicle?.make} {sale.vehicle?.model}
                              </h3>
                              <div className={`px-2 py-1 rounded-full text-xs flex items-center space-x-1 ${
                                sale.is_sold 
                                  ? 'text-green-400 bg-green-400/20' 
                                  : sale.is_active 
                                    ? 'text-blue-400 bg-blue-400/20' 
                                    : 'text-gray-400 bg-gray-400/20'
                              }`}>
                                {sale.is_sold ? (
                                  <>
                                    <CheckCircle size={12} />
                                    <span>Sold</span>
                                  </>
                                ) : sale.is_active ? (
                                  <>
                                    <Eye size={12} />
                                    <span>Active</span>
                                  </>
                                ) : (
                                  <>
                                    <EyeOff size={12} />
                                    <span>Inactive</span>
                                  </>
                                )}
                              </div>
                            </div>
                            <p className="text-gray-400 text-sm mb-2">{sale.vehicle?.vehicle_name}</p>
                            <div className="flex items-center space-x-4 text-sm">
                              <span className="text-green-400 font-semibold">
                                {formatPrice(sale.selling_price)}
                              </span>
                              <span className="text-gray-400">
                                {sale.negotiations_count || 0} negotiations
                              </span>
                              <span className="text-gray-400">
                                Listed {formatDate(sale.created_at)}
                              </span>
                            </div>
                          </div>
                          <div className="flex space-x-2 ml-4">
                            <button className="p-2 bg-white/10 hover:bg-white/20 rounded-lg transition-colors">
                              <Edit className="text-gray-300" size={16} />
                            </button>
                            <button 
                              onClick={(e) => {
                                e.stopPropagation();
                                handleDeleteSale(sale.id);
                              }}
                              className="p-2 bg-red-600/20 hover:bg-red-600/30 rounded-lg transition-colors"
                            >
                              <Trash2 className="text-red-400" size={16} />
                            </button>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-12">
                    <Car size={48} className="mx-auto mb-4 text-gray-400 opacity-50" />
                    <h3 className="text-lg font-semibold text-white mb-2">No vehicles listed</h3>
                    <p className="text-gray-400 mb-4">Start by listing your first vehicle for sale</p>
                    <Link
                      to="/vehicles"
                      className="inline-flex items-center space-x-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
                    >
                      <Plus size={16} />
                      <span>List Vehicle</span>
                    </Link>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Negotiations Panel */}
          <div className="space-y-6">
            {selectedSale ? (
              <>
                {/* Selected Vehicle Info */}
                <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
                  <h3 className="text-lg font-semibold text-white mb-4">Selected Vehicle</h3>
                  <div className="space-y-2">
                    <p className="text-white font-medium">
                      {selectedSale.vehicle?.year} {selectedSale.vehicle?.make} {selectedSale.vehicle?.model}
                    </p>
                    <p className="text-gray-400 text-sm">{selectedSale.vehicle?.vehicle_name}</p>
                    <p className="text-green-400 font-semibold">{formatPrice(selectedSale.selling_price)}</p>
                    {selectedSale.minimum_price && (
                      <p className="text-gray-400 text-sm">
                        Min: {formatPrice(selectedSale.minimum_price)}
                      </p>
                    )}
                    {negotiations.length > 0 && (
                      <div className="mt-2 pt-2 border-t border-white/10">
                        <p className="text-xs text-gray-400 mb-1">Best Offer</p>
                        <p className="text-blue-400 font-semibold">
                          {formatPrice(Math.min(...negotiations.map(n => n.final_offer)))}
                        </p>
                        {Math.min(...negotiations.map(n => n.final_offer)) < selectedSale.selling_price && (
                          <p className="text-xs text-orange-400">
                            -{formatPrice(selectedSale.selling_price - Math.min(...negotiations.map(n => n.final_offer)))} from asking
                          </p>
                        )}
                      </div>
                    )}
                  </div>
                </div>

                {/* Negotiations */}
                <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl">
                  <div className="p-4 border-b border-white/20">
                    <h3 className="text-lg font-semibold text-white">
                      Negotiations ({negotiations.length})
                    </h3>
                  </div>
                  <div className="p-4">
                    {negotiations.length > 0 ? (
                      <div className="space-y-4">
                        {negotiations.map((negotiation) => (
                          <div key={negotiation.id} className="p-4 bg-white/5 rounded-lg">
                            <div className="flex justify-between items-start mb-3">
                              <div className="flex-1">
                                <div className="flex items-center space-x-2 mb-1">
                                  <User className="text-blue-400" size={16} />
                                  <span className="text-white font-medium">{negotiation.buyer_name}</span>
                                  <div className={`px-2 py-1 rounded-full text-xs flex items-center space-x-1 ${getStatusColor(negotiation.status)}`}>
                                    {getStatusIcon(negotiation.status)}
                                    <span className="capitalize">{negotiation.status}</span>
                                  </div>
                                </div>
                                <p className="text-sm text-gray-400">
                                  {formatDate(negotiation.created_at)}
                                </p>
                                {negotiation.status === 'accepted' && (
                                  <div className="flex items-center space-x-1 mt-1">
                                    <CheckCircle size={12} className="text-green-400" />
                                    <span className="text-xs text-green-400 font-medium">Deal Finalized</span>
                                  </div>
                                )}
                              </div>
                              <div className="text-right">
                                <p className="text-xl font-bold text-green-400">
                                  {formatPrice(negotiation.final_offer)}
                                </p>
                                <p className="text-xs text-gray-400">
                                  {negotiation.status === 'accepted' ? 'Final Sale Price' : 'Negotiated Price'}
                                </p>
                                {selectedSale && negotiation.final_offer < selectedSale.selling_price && (
                                  <div className="text-xs text-orange-400 mt-1">
                                    <span>-{formatPrice(selectedSale.selling_price - negotiation.final_offer)} from asking</span>
                                    <br />
                                    <span>({Math.round((selectedSale.selling_price - negotiation.final_offer) / selectedSale.selling_price * 100)}% discount)</span>
                                  </div>
                                )}
                                {negotiation.status === 'accepted' && (
                                  <div className="text-xs text-green-400 mt-1 font-medium">
                                    🎉 SOLD
                                  </div>
                                )}
                              </div>
                            </div>

                            {/* Contact Info */}
                            <div className="space-y-1 mb-3 text-sm">
                              <div className="flex items-center space-x-2 text-gray-300">
                                <Mail size={12} />
                                <span>{negotiation.buyer_email}</span>
                              </div>
                              {negotiation.buyer_contact && (
                                <div className="flex items-center space-x-2 text-gray-300">
                                  <Phone size={12} />
                                  <span>{negotiation.buyer_contact}</span>
                                </div>
                              )}
                            </div>

                            {/* Action Buttons */}
                            {negotiation.status === 'pending' && (
                              <div className="space-y-2">
                                {negotiation.buyer_name && negotiation.buyer_name !== 'Anonymous' && negotiation.buyer_email ? (
                                  <div className="text-xs text-yellow-400 bg-yellow-400/10 rounded p-2">
                                    💬 Customer has finalized their offer and provided contact details. Accept to complete the sale!
                                  </div>
                                ) : (
                                  <div className="text-xs text-blue-400 bg-blue-400/10 rounded p-2">
                                    💬 Customer is still negotiating. Waiting for final offer and contact details.
                                  </div>
                                )}
                                {negotiation.buyer_name && negotiation.buyer_name !== 'Anonymous' && negotiation.buyer_email ? (
                                  <div className="flex space-x-2">
                                    <button
                                      onClick={() => handleAcceptNegotiation(negotiation.id)}
                                      className="flex-1 bg-green-600 hover:bg-green-700 text-white py-2 px-3 rounded text-sm transition-colors font-medium"
                                    >
                                      ✅ Accept Rs. {formatPrice(negotiation.final_offer).replace('LKR ', '')}
                                    </button>
                                    <button
                                      onClick={() => handleRejectNegotiation(negotiation.id)}
                                      className="flex-1 bg-red-600 hover:bg-red-700 text-white py-2 px-3 rounded text-sm transition-colors"
                                    >
                                      ❌ Reject Offer
                                    </button>
                                  </div>
                                ) : (
                                  <div className="flex space-x-2 opacity-50">
                                    <button
                                      disabled
                                      className="flex-1 bg-gray-600 text-white py-2 px-3 rounded text-sm cursor-not-allowed"
                                    >
                                      ⏳ Waiting for Customer
                                    </button>
                                  </div>
                                )}
                              </div>
                            )}
                            
                            {negotiation.status === 'accepted' && (
                              <div className="text-xs text-green-400 bg-green-400/10 rounded p-2">
                                🎉 Deal completed! Vehicle sold for Rs. {formatPrice(negotiation.final_offer).replace('LKR ', '')}. Contact the buyer to arrange pickup/delivery.
                              </div>
                            )}
                            
                            {negotiation.status === 'rejected' && (
                              <div className="text-xs text-red-400 bg-red-400/10 rounded p-2">
                                ❌ Offer rejected. The buyer may submit a new negotiation if interested.
                              </div>
                            )}
                          </div>
                        ))}
                      </div>
                    ) : (
                      <div className="text-center py-8">
                        <MessageCircle size={32} className="mx-auto mb-3 text-gray-400 opacity-50" />
                        <p className="text-gray-400 text-sm">No negotiations yet</p>
                      </div>
                    )}
                  </div>
                </div>
              </>
            ) : (
              <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
                <div className="text-center py-8">
                  <Car size={32} className="mx-auto mb-3 text-gray-400 opacity-50" />
                  <p className="text-gray-400">Select a vehicle to view negotiations</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SellerDashboard;