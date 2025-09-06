import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Car,
  ArrowLeft,
  Calendar,
  Fuel,
  Settings,
  MapPin,
  User,
  MessageCircle,
  Send,
  Phone,
  Mail,
  Star,
  Tag,
  Info
} from 'lucide-react';
import { apiService, VehicleSale, NegotiationResponse, ChatMessage } from '../services/apiService';

const VehicleDetailsPage: React.FC = () => {
  const { vehicleId } = useParams<{ vehicleId: string }>();
  const navigate = useNavigate();
  const [vehicle, setVehicle] = useState<VehicleSale | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [showChat, setShowChat] = useState(false);
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [messageInput, setMessageInput] = useState('');
  const [isSending, setIsSending] = useState(false);
  const [negotiationId, setNegotiationId] = useState<number | null>(null);
  const [isNegotiationComplete, setIsNegotiationComplete] = useState(false);
  const [finalPrice, setFinalPrice] = useState<number | null>(null);
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (vehicleId) {
      loadVehicleDetails(parseInt(vehicleId));
    }
  }, [vehicleId]);

  useEffect(() => {
    scrollToBottom();
  }, [chatMessages]);

  const loadVehicleDetails = async (id: number) => {
    try {
      setIsLoading(true);
      const response = await apiService.getVehicleSale(id);
      console.log('Vehicle details:', response);
      setVehicle(response.vehicle_sale);
    } catch (error) {
      console.error('Failed to load vehicle details:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const startNegotiation = async () => {
    if (!vehicle) return;
    
    setShowChat(true);
    
    // Start with a greeting if no messages exist
    if (chatMessages.length === 0) {
      const greeting = `Hi! I'm interested in your ${vehicle.vehicle?.year} ${vehicle.vehicle?.make} ${vehicle.vehicle?.model}. What's the price?`;
      await sendMessage(greeting);
    }
  };

  const sendMessage = async (message: string) => {
    if (!vehicle || (!message.trim() && !messageInput.trim())) return;

    const messageToSend = message || messageInput;
    setIsSending(true);

    try {
      // Add user message to chat
      const userMessage: ChatMessage = {
        sender: 'buyer',
        message: messageToSend,
        timestamp: new Date().toISOString()
      };
      setChatMessages(prev => [...prev, userMessage]);
      setMessageInput('');

      // Send to negotiation API
      let response: NegotiationResponse;
      
      if (negotiationId) {
        response = await apiService.continueNegotiation(vehicle.id, negotiationId, messageToSend);
      } else {
        response = await apiService.startNegotiation(vehicle.id, messageToSend);
        setNegotiationId(response.negotiation_id);
      }

      // Add bot response to chat
      const botMessage: ChatMessage = {
        sender: 'system',
        message: response.response,
        timestamp: new Date().toISOString()
      };
      setChatMessages(prev => [...prev, botMessage]);

      // Check if negotiation is complete
      if (response.contact_collected && response.final_price) {
        setIsNegotiationComplete(true);
        setFinalPrice(response.final_price);
      }

    } catch (error) {
      console.error('Failed to send message:', error);
      // Add error message
      const errorMessage: ChatMessage = {
        sender: 'system',
        message: 'Sorry, there was an error processing your message. Please try again.',
        timestamp: new Date().toISOString()
      };
      setChatMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsSending(false);
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
      month: 'long',
      day: 'numeric'
    });
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400 mb-4"></div>
          <p className="text-white">Loading vehicle details...</p>
        </div>
      </div>
    );
  }

  if (!vehicle) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <Car size={64} className="mx-auto mb-6 text-gray-400 opacity-50" />
          <h2 className="text-2xl font-semibold text-white mb-4">Vehicle not found</h2>
          <button
            onClick={() => navigate('/marketplace')}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg transition-colors"
          >
            Back to Marketplace
          </button>
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
            <button
              onClick={() => navigate('/marketplace')}
              className="flex items-center space-x-2 text-gray-300 hover:text-white transition-colors"
            >
              <ArrowLeft size={20} />
              <span>Back to Marketplace</span>
            </button>
            <div className="text-sm text-gray-300">
              Listed {formatDate(vehicle.created_at)}
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Vehicle Images */}
            <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
              <div className="bg-gradient-to-br from-blue-600/20 to-purple-600/20 rounded-xl h-80 flex items-center justify-center mb-4">
                <Car className="text-blue-400" size={120} />
              </div>
              <div className="grid grid-cols-4 gap-2">
                {[1, 2, 3, 4].map((_, index) => (
                  <div key={index} className="bg-white/5 rounded-lg h-20 flex items-center justify-center">
                    <Car className="text-gray-400" size={24} />
                  </div>
                ))}
              </div>
            </div>

            {/* Vehicle Info */}
            <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h1 className="text-3xl font-bold text-white mb-2">
                    {vehicle.vehicle?.year} {vehicle.vehicle?.make} {vehicle.vehicle?.model}
                  </h1>
                  <p className="text-xl text-gray-300">{vehicle.vehicle?.vehicle_name}</p>
                </div>
                <div className="text-right">
                  <div className="text-3xl font-bold text-green-400">
                    {formatPrice(vehicle.selling_price)}
                  </div>
                  <p className="text-sm text-gray-400">Asking Price</p>
                </div>
              </div>

              {/* Features */}
              {vehicle.features && vehicle.features.length > 0 && (
                <div className="mb-6">
                  <h3 className="text-lg font-semibold text-white mb-3 flex items-center">
                    <Star className="mr-2 text-yellow-400" size={20} />
                    Additional Features
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {vehicle.features.map((feature, index) => (
                      <span
                        key={index}
                        className="px-3 py-1 bg-blue-600/20 text-blue-300 rounded-full text-sm flex items-center"
                      >
                        <Tag className="mr-1" size={12} />
                        {feature}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Description */}
              {vehicle.description && (
                <div className="mb-6">
                  <h3 className="text-lg font-semibold text-white mb-3 flex items-center">
                    <Info className="mr-2 text-blue-400" size={20} />
                    Description
                  </h3>
                  <p className="text-gray-300 leading-relaxed">{vehicle.description}</p>
                </div>
              )}

              {/* Specifications */}
              <div>
                <h3 className="text-lg font-semibold text-white mb-4">Specifications</h3>
                <div className="grid md:grid-cols-2 gap-4">
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-gray-400">Make</span>
                      <span className="text-white font-medium">{vehicle.vehicle?.make}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-400">Model</span>
                      <span className="text-white font-medium">{vehicle.vehicle?.model}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-400">Year</span>
                      <span className="text-white font-medium">{vehicle.vehicle?.year}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-400">Class</span>
                      <span className="text-white font-medium">{vehicle.vehicle?.vehicle_class}</span>
                    </div>
                  </div>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-gray-400">Engine Size</span>
                      <span className="text-white font-medium">{vehicle.vehicle?.engine_size}L</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-400">Fuel Type</span>
                      <span className="text-white font-medium">{vehicle.vehicle?.fuel_type}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-400">Transmission</span>
                      <span className="text-white font-medium">{vehicle.vehicle?.transmission}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-400">Tank Capacity</span>
                      <span className="text-white font-medium">{vehicle.vehicle?.tank_capacity}L</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Seller Info */}
            <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
                <User className="mr-2 text-blue-400" size={20} />
                Seller Information
              </h3>
              <div className="space-y-3">
                <div className="flex items-center space-x-2">
                  <User className="text-gray-400" size={16} />
                  <span className="text-white">{vehicle.seller?.name || 'Private Seller'}</span>
                </div>
                <div className="flex items-center space-x-2">
                  <MapPin className="text-gray-400" size={16} />
                  <span className="text-gray-300">{vehicle.seller?.location || 'Colombo, Sri Lanka'}</span>
                </div>
              </div>
            </div>

            {/* Contact Actions */}
            <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
              <h3 className="text-lg font-semibold text-white mb-4">Interested?</h3>
              <div className="space-y-3">
                <button
                  onClick={startNegotiation}
                  className="w-full flex items-center justify-center space-x-2 bg-green-600 hover:bg-green-700 text-white py-3 px-4 rounded-lg transition-colors"
                >
                  <MessageCircle size={20} />
                  <span>Start Price Negotiation</span>
                </button>
                
                {isNegotiationComplete && finalPrice && (
                  <div className="p-3 bg-green-600/20 border border-green-600/30 rounded-lg">
                    <p className="text-green-300 text-sm mb-1">🎉 Negotiation Complete!</p>
                    <p className="text-white font-medium">Final Price: {formatPrice(finalPrice)}</p>
                    <p className="text-gray-300 text-xs mt-1">The seller will contact you soon.</p>
                  </div>
                )}
              </div>
            </div>

            {/* Safety Tips */}
            <div className="bg-yellow-600/10 border border-yellow-600/20 rounded-xl p-6">
              <h3 className="text-lg font-semibold text-yellow-300 mb-4">🛡️ Safety Tips</h3>
              <ul className="text-sm text-yellow-100 space-y-2">
                <li>• Meet in public places</li>
                <li>• Inspect the vehicle thoroughly</li>
                <li>• Verify ownership documents</li>
                <li>• Consider a pre-purchase inspection</li>
                <li>• Use secure payment methods</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Chat Modal */}
      {showChat && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <div className="bg-slate-800 border border-white/20 rounded-xl w-full max-w-md h-[600px] flex flex-col">
            {/* Chat Header */}
            <div className="p-4 border-b border-white/20">
              <div className="flex justify-between items-center">
                <h3 className="text-lg font-semibold text-white">Price Negotiation</h3>
                <button
                  onClick={() => setShowChat(false)}
                  className="text-gray-400 hover:text-white"
                >
                  ×
                </button>
              </div>
              <p className="text-sm text-gray-400 mt-1">
                {vehicle.vehicle?.year} {vehicle.vehicle?.make} {vehicle.vehicle?.model}
              </p>
            </div>

            {/* Chat Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-3">
              {chatMessages.map((msg, index) => (
                <div
                  key={index}
                  className={`flex ${msg.sender === 'buyer' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[80%] p-3 rounded-lg ${
                      msg.sender === 'buyer'
                        ? 'bg-blue-600 text-white'
                        : 'bg-white/10 text-gray-100'
                    }`}
                  >
                    <p className="text-sm">{msg.message}</p>
                    <p className="text-xs opacity-70 mt-1">
                      {new Date(msg.timestamp).toLocaleTimeString([], { 
                        hour: '2-digit', 
                        minute: '2-digit' 
                      })}
                    </p>
                  </div>
                </div>
              ))}
              <div ref={chatEndRef} />
            </div>

            {/* Chat Input */}
            {!isNegotiationComplete && (
              <div className="p-4 border-t border-white/20">
                <div className="flex space-x-2">
                  <input
                    type="text"
                    value={messageInput}
                    onChange={(e) => setMessageInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && !isSending && sendMessage('')}
                    placeholder="Type your message..."
                    className="flex-1 px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    disabled={isSending}
                  />
                  <button
                    onClick={() => sendMessage('')}
                    disabled={isSending || !messageInput.trim()}
                    className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white p-2 rounded-lg transition-colors"
                  >
                    <Send size={16} />
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default VehicleDetailsPage;