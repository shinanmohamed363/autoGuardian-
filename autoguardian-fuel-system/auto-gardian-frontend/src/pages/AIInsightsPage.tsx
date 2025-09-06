import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import {
  Brain,
  Zap,
  TrendingUp,
  ArrowLeft,
  Star,
  AlertCircle,
  Target,
  Fuel,
  DollarSign,
  Leaf,
  BarChart3,
  Lightbulb,
  Loader2,
  FileDown,
  Mail
} from 'lucide-react';
import { apiService, Vehicle, MLPrediction, AIRecommendation } from '../services/apiService';
import jsPDF from 'jspdf';
import emailjs from '@emailjs/browser';

const AIInsightsPage: React.FC = () => {
  const { vehicleId } = useParams<{ vehicleId: string }>();
  const navigate = useNavigate();
  
  const [vehicle, setVehicle] = useState<Vehicle | null>(null);
  const [mlPrediction, setMlPrediction] = useState<MLPrediction | null>(null);
  const [aiRecommendations, setAiRecommendations] = useState<AIRecommendation | null>(null);
  const [isGeneratingML, setIsGeneratingML] = useState(false);
  const [isGeneratingAI, setIsGeneratingAI] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [isGeneratingPDF, setIsGeneratingPDF] = useState(false);
  const [isSendingEmail, setIsSendingEmail] = useState(false);
  const [userEmail, setUserEmail] = useState('');
  const [showEmailInput, setShowEmailInput] = useState(false);
  const [activeTab, setActiveTab] = useState<'predictions' | 'recommendations'>('predictions');

  useEffect(() => {
    if (vehicleId) {
      loadVehicle();
    }
  }, [vehicleId]);

  const loadVehicle = async () => {
    try {
      setIsLoading(true);
      const response = await apiService.getVehicle(parseInt(vehicleId!));
      setVehicle(response.vehicle);
    } catch (error) {
      console.error('Failed to load vehicle:', error);
      if (error instanceof Error && error.message.includes('401')) {
        navigate('/');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const generateMLPrediction = async () => {
    if (!vehicleId) return;
    
    setIsGeneratingML(true);
    try {
      const response = await apiService.generateMLPrediction(parseInt(vehicleId));
      setMlPrediction(response);
    } catch (error) {
      console.error('Failed to generate ML prediction:', error);
      if (error instanceof Error) {
        alert('Failed to generate ML prediction: ' + error.message);
      }
    } finally {
      setIsGeneratingML(false);
    }
  };

  const generateAIRecommendation = async (type: 'efficiency' | 'maintenance') => {
    if (!vehicleId) return;
    
    setIsGeneratingAI(true);
    try {
      const response = await apiService.generateAIRecommendation(parseInt(vehicleId), type);
      setAiRecommendations(response);
    } catch (error) {
      console.error('Failed to generate AI recommendation:', error);
      if (error instanceof Error) {
        alert('Failed to generate AI recommendation: ' + error.message);
      }
    } finally {
      setIsGeneratingAI(false);
    }
  };

  const generatePDFReport = async () => {
    if (!mlPrediction || !vehicle) {
      alert('Please generate ML prediction first');
      return;
    }

    setIsGeneratingPDF(true);
    try {
      const pdf = new jsPDF();
      
      // Set font
      pdf.setFont('helvetica');
      
      // Header
      pdf.setFontSize(20);
      pdf.setTextColor(34, 139, 34); // Green color
      pdf.text('AutoGuardian Fuel Efficiency Report', 20, 25);
      
      // Divider line
      pdf.setDrawColor(200, 200, 200);
      pdf.line(20, 32, 190, 32);
      
      // Vehicle Information
      pdf.setFontSize(16);
      pdf.setTextColor(0, 0, 0);
      pdf.text('Vehicle Information', 20, 45);
      
      pdf.setFontSize(12);
      pdf.text(`Vehicle: ${vehicle.year} ${vehicle.make} ${vehicle.model}`, 25, 55);
      pdf.text(`Engine: ${vehicle.engine_size}L, ${vehicle.cylinders} cylinders`, 25, 65);
      pdf.text(`Transmission: ${vehicle.transmission}`, 25, 75);
      pdf.text(`Fuel Type: ${vehicle.fuel_type}`, 25, 85);
      pdf.text(`Report Generated: ${new Date().toLocaleDateString()}`, 25, 95);
      
      // ML Prediction Results
      pdf.setFontSize(16);
      pdf.setTextColor(34, 139, 34);
      pdf.text('Fuel Efficiency Analysis', 20, 115);
      
      pdf.setFontSize(12);
      pdf.setTextColor(0, 0, 0);
      
      // Efficiency Rating
      pdf.text(`Efficiency Rating: ${mlPrediction.prediction.efficiency_stars}/5 stars`, 25, 130);
      pdf.text(`Rating: ${mlPrediction.prediction.efficiency_rating?.replace(/⭐/g, '')} `, 25, 140);
      
      // Fuel Consumption
      pdf.text('Fuel Consumption:', 25, 155);
      pdf.text(`• Combined: ${mlPrediction.prediction.combined_l_100km} L/100km`, 30, 165);
      pdf.text(`• Highway: ${mlPrediction.prediction.highway_l_100km} L/100km`, 30, 175);
      pdf.text(`• City: ${mlPrediction.prediction.city_l_100km} L/100km`, 30, 185);
      
      // Annual Projections
      pdf.text('Annual Projections (15,000 km/year):', 25, 200);
      pdf.text(`• Fuel Cost: $${mlPrediction.prediction.annual_fuel_cost?.toFixed(0)}`, 30, 210);
      pdf.text(`• CO2 Emissions: ${(mlPrediction.prediction.annual_co2_emissions / 1000)?.toFixed(1)} tonnes`, 30, 220);
      pdf.text(`• MPG Equivalent: ${mlPrediction.prediction.mpg_equivalent?.toFixed(1)} MPG`, 30, 230);
      
      // Environmental Impact
      pdf.text('Environmental Impact:', 25, 245);
      pdf.text(`• CO2 Emissions: ${mlPrediction.prediction.emissions_g_km} g/km`, 30, 255);
      pdf.text(`• Environmental Rating: Based on emissions output`, 30, 265);
      
      // Model Information
      pdf.setFontSize(14);
      pdf.setTextColor(34, 139, 34);
      pdf.text('Prediction Details', 120, 115);
      
      pdf.setFontSize(10);
      pdf.setTextColor(0, 0, 0);
      pdf.text(`Model Used: ${mlPrediction.prediction.prediction_metadata?.model_used}`, 125, 130);
      pdf.text(`Features: ${mlPrediction.prediction.prediction_metadata?.features_used?.length} parameters`, 125, 140);
      pdf.text(`Generated: ${new Date(mlPrediction.prediction.prediction_metadata?.prediction_date || new Date()).toLocaleDateString()}`, 125, 150);
      
      // Recommendations (if available)
      if (aiRecommendations) {
        pdf.addPage();
        pdf.setFontSize(20);
        pdf.setTextColor(34, 139, 34);
        pdf.text('AI Recommendations', 20, 25);
        
        pdf.setDrawColor(200, 200, 200);
        pdf.line(20, 32, 190, 32);
        
        let yPos = 45;
        aiRecommendations.recommendations.forEach((rec, index) => {
          if (yPos > 250) {
            pdf.addPage();
            yPos = 25;
          }
          
          pdf.setFontSize(14);
          pdf.setTextColor(0, 0, 0);
          pdf.text(`${index + 1}. ${rec.recommendation_title}`, 20, yPos);
          
          pdf.setFontSize(10);
          pdf.text(`Priority: ${rec.priority_level} | Impact: ${rec.impact_score}/10`, 25, yPos + 10);
          
          // Split recommendation text into lines
          const lines = pdf.splitTextToSize(rec.recommendation_text, 170);
          pdf.text(lines.slice(0, 10), 25, yPos + 20); // Limit to 10 lines per recommendation
          
          yPos += 60 + (lines.length * 3);
        });
      }
      
      // Footer
      pdf.setFontSize(8);
      pdf.setTextColor(128, 128, 128);
      pdf.text('Generated by AutoGuardian Fuel Management System', 20, 285);
      pdf.text(`Vehicle ID: ${vehicleId} | Report ID: ${Date.now()}`, 120, 285);
      
      // Save the PDF
      pdf.save(`AutoGuardian-Report-${vehicle.make}-${vehicle.model}-${new Date().toISOString().split('T')[0]}.pdf`);
      
    } catch (error) {
      console.error('PDF generation failed:', error);
      alert('Failed to generate PDF report. Please try again.');
    } finally {
      setIsGeneratingPDF(false);
    }
  };

  // Email functionality
  const sendEmailReport = async () => {
    if (!mlPrediction || !vehicle || !userEmail) {
      alert('Please generate ML prediction and enter email address first');
      return;
    }

    setIsSendingEmail(true);
    try {
      // Initialize EmailJS (you can also do this in useEffect)
      emailjs.init('DKodxJRDdbkiegNFq');

      // Prepare template parameters
      const templateParams = {
        title: `AutoGuardian Fuel Efficiency Report - ${vehicle.year} ${vehicle.make} ${vehicle.model}`,
        toemail: userEmail,
        user_name: 'AutoGuardian User', // You can get this from user context
        vehicle_info: `${vehicle.year} ${vehicle.make} ${vehicle.model}`,
        analysis_date: new Date().toLocaleDateString(),
        efficiency_stars: '⭐'.repeat(mlPrediction.prediction.efficiency_stars),
        efficiency_rating: mlPrediction.prediction.efficiency_rating || 'Good efficiency',
        combined_consumption: mlPrediction.prediction.combined_l_100km.toFixed(1),
        highway_consumption: mlPrediction.prediction.highway_l_100km.toFixed(1),
        city_consumption: mlPrediction.prediction.city_l_100km.toFixed(1),
        annual_cost: mlPrediction.prediction.annual_fuel_cost.toFixed(0),
        co2_emissions: mlPrediction.prediction.emissions_g_km.toFixed(0),
        ai_recommendations: aiRecommendations?.recommendations?.[0]?.recommendation_text || 
                          'Generate AI recommendations for personalized tips to improve your vehicle efficiency.'
      };

      // Send email
      const result = await emailjs.send(
        'service_dnu23n8', // Service ID
        'template_4zbjcsd', // Template ID  
        templateParams
      );

      if (result.status === 200) {
        alert(`Report sent successfully to ${userEmail}!`);
        setUserEmail('');
        setShowEmailInput(false);
      } else {
        throw new Error('Email sending failed');
      }

    } catch (error) {
      console.error('Email sending failed:', error);
      alert('Failed to send email report. Please check your email address and try again.');
    } finally {
      setIsSendingEmail(false);
    }
  };

  const renderStars = (count: number) => {
    return Array.from({ length: 5 }, (_, i) => (
      <Star
        key={i}
        className={`w-4 h-4 ${i < count ? 'text-yellow-400 fill-current' : 'text-gray-400'}`}
      />
    ));
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'critical': return 'text-red-400 bg-red-400/20';
      case 'high': return 'text-orange-400 bg-orange-400/20';
      case 'medium': return 'text-yellow-400 bg-yellow-400/20';
      case 'low': return 'text-green-400 bg-green-400/20';
      default: return 'text-gray-400 bg-gray-400/20';
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400 mb-4"></div>
          <p className="text-white">Loading AI Insights...</p>
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
                  <Brain className="w-8 h-8 mr-3 text-purple-400" />
                  AI Insights
                </h1>
                {vehicle && (
                  <p className="text-gray-300 text-sm">{vehicle.display_name}</p>
                )}
              </div>
            </div>
            <div className="flex space-x-3">
              <button
                onClick={() => setActiveTab('predictions')}
                className={`px-4 py-2 rounded-lg transition-all duration-200 ${
                  activeTab === 'predictions'
                    ? 'bg-blue-600 text-white'
                    : 'bg-white/10 text-gray-300 hover:bg-white/20'
                }`}
              >
                <Zap className="w-4 h-4 inline mr-2" />
                Predictions
              </button>
              <button
                onClick={() => setActiveTab('recommendations')}
                className={`px-4 py-2 rounded-lg transition-all duration-200 ${
                  activeTab === 'recommendations'
                    ? 'bg-purple-600 text-white'
                    : 'bg-white/10 text-gray-300 hover:bg-white/20'
                }`}
              >
                <Lightbulb className="w-4 h-4 inline mr-2" />
                Recommendations
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* ML Predictions Tab */}
        {activeTab === 'predictions' && (
          <div className="space-y-8">
            {/* Generate Prediction Section */}
            <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h2 className="text-xl font-semibold text-white">Fuel Efficiency Predictions</h2>
                  <p className="text-gray-300 text-sm">AI-powered machine learning analysis</p>
                </div>
                <div className="flex space-x-3">
                  <button
                    onClick={generateMLPrediction}
                    disabled={isGeneratingML}
                    className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 disabled:opacity-50 text-white px-6 py-3 rounded-lg flex items-center space-x-2 transition-all duration-200"
                  >
                    {isGeneratingML ? (
                      <Loader2 className="w-5 h-5 animate-spin" />
                    ) : (
                      <Zap className="w-5 h-5" />
                    )}
                    <span>{isGeneratingML ? 'Generating...' : 'Generate Prediction'}</span>
                  </button>
                  {mlPrediction && (
                    <button
                      onClick={generatePDFReport}
                      disabled={!mlPrediction || isGeneratingPDF}
                      className="bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 disabled:opacity-50 text-white px-6 py-3 rounded-lg flex items-center space-x-2 transition-all duration-200"
                    >
                      {isGeneratingPDF ? (
                        <Loader2 className="w-5 h-5 animate-spin" />
                      ) : (
                        <FileDown className="w-5 h-5" />
                      )}
                      <span>{isGeneratingPDF ? 'Generating...' : 'Download PDF'}</span>
                    </button>
                  )}
                  {mlPrediction && (
                    <button
                      onClick={() => setShowEmailInput(!showEmailInput)}
                      disabled={!mlPrediction}
                      className="bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 disabled:opacity-50 text-white px-6 py-3 rounded-lg flex items-center space-x-2 transition-all duration-200"
                    >
                      <Mail className="w-5 h-5" />
                      <span>Email Report</span>
                    </button>
                  )}
                </div>
              </div>

              {/* Email Input Section */}
              {showEmailInput && mlPrediction && (
                <div className="bg-white/5 backdrop-blur-md border border-white/10 rounded-xl p-6 mb-6">
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <h3 className="text-lg font-semibold text-white">Email Report</h3>
                      <p className="text-gray-300 text-sm">Send your fuel efficiency analysis via email</p>
                    </div>
                  </div>
                  <div className="flex space-x-4">
                    <input
                      type="email"
                      value={userEmail}
                      onChange={(e) => setUserEmail(e.target.value)}
                      placeholder="Enter your email address"
                      className="flex-1 bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    />
                    <button
                      onClick={sendEmailReport}
                      disabled={!userEmail || isSendingEmail}
                      className="bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 disabled:opacity-50 text-white px-6 py-3 rounded-lg flex items-center space-x-2 transition-all duration-200"
                    >
                      {isSendingEmail ? (
                        <Loader2 className="w-5 h-5 animate-spin" />
                      ) : (
                        <Mail className="w-5 h-5" />
                      )}
                      <span>{isSendingEmail ? 'Sending...' : 'Send Report'}</span>
                    </button>
                  </div>
                </div>
              )}

              {mlPrediction && (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {/* Efficiency Rating */}
                  <div className="bg-white/5 border border-white/10 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="text-white font-medium">Efficiency Rating</h3>
                      <Target className="w-5 h-5 text-blue-400" />
                    </div>
                    <div className="flex items-center space-x-2 mb-2">
                      {renderStars(mlPrediction.prediction.efficiency_stars)}
                    </div>
                    <p className="text-gray-300 text-sm">{mlPrediction.prediction.efficiency_rating}</p>
                  </div>

                  {/* Fuel Consumption */}
                  <div className="bg-white/5 border border-white/10 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="text-white font-medium">Fuel Consumption</h3>
                      <Fuel className="w-5 h-5 text-green-400" />
                    </div>
                    <div className="space-y-1">
                      <div className="flex justify-between">
                        <span className="text-gray-400 text-sm">Combined:</span>
                        <span className="text-white font-medium">{mlPrediction.prediction.combined_l_100km.toFixed(1)} L/100km</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400 text-sm">Highway:</span>
                        <span className="text-green-300">{mlPrediction.prediction.highway_l_100km.toFixed(1)} L/100km</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400 text-sm">City:</span>
                        <span className="text-orange-300">{mlPrediction.prediction.city_l_100km.toFixed(1)} L/100km</span>
                      </div>
                    </div>
                  </div>

                  {/* Cost Analysis */}
                  <div className="bg-white/5 border border-white/10 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="text-white font-medium">Annual Cost</h3>
                      <DollarSign className="w-5 h-5 text-yellow-400" />
                    </div>
                    <div className="space-y-2">
                      <div>
                        <p className="text-2xl font-bold text-white">${mlPrediction.prediction.annual_fuel_cost.toFixed(0)}</p>
                        <p className="text-gray-400 text-sm">Estimated yearly fuel cost</p>
                      </div>
                      <div className="text-sm text-gray-300">
                        MPG Equivalent: {mlPrediction.prediction.mpg_equivalent.toFixed(1)}
                      </div>
                    </div>
                  </div>

                  {/* Environmental Impact */}
                  <div className="bg-white/5 border border-white/10 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="text-white font-medium">Environmental Impact</h3>
                      <Leaf className="w-5 h-5 text-green-400" />
                    </div>
                    <div className="space-y-2">
                      <div>
                        <p className="text-white font-medium">{mlPrediction.prediction.emissions_g_km.toFixed(0)} g/km</p>
                        <p className="text-gray-400 text-sm">CO₂ emissions</p>
                      </div>
                      <div>
                        <p className="text-green-300 font-medium">{(mlPrediction.prediction.annual_co2_emissions / 1000).toFixed(1)} tonnes</p>
                        <p className="text-gray-400 text-sm">Annual CO₂</p>
                      </div>
                    </div>
                  </div>

                  {/* Model Info */}
                  <div className="bg-white/5 border border-white/10 rounded-lg p-4 md:col-span-2">
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="text-white font-medium">Prediction Details</h3>
                      <BarChart3 className="w-5 h-5 text-purple-400" />
                    </div>
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <p className="text-gray-400">Model Used:</p>
                        <p className="text-white">{mlPrediction.prediction.prediction_metadata.model_used}</p>
                      </div>
                      <div>
                        <p className="text-gray-400">Features:</p>
                        <p className="text-white">{mlPrediction.prediction.prediction_metadata.features_used.length} parameters</p>
                      </div>
                      <div>
                        <p className="text-gray-400">Generated:</p>
                        <p className="text-white">{new Date(mlPrediction.prediction.prediction_metadata.prediction_date).toLocaleDateString()}</p>
                      </div>
                      <div>
                        <p className="text-gray-400">Vehicle:</p>
                        <p className="text-white">{mlPrediction.vehicle_info.year} {mlPrediction.vehicle_info.make} {mlPrediction.vehicle_info.model}</p>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {!mlPrediction && (
                <div className="text-center py-12">
                  <Zap className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-300 text-lg mb-2">Generate AI Prediction</p>
                  <p className="text-gray-400">Click the button above to get machine learning insights</p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* AI Recommendations Tab */}
        {activeTab === 'recommendations' && (
          <div className="space-y-8">
            {/* Generate Recommendations Section */}
            <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h2 className="text-xl font-semibold text-white">AI Recommendations</h2>
                  <p className="text-gray-300 text-sm">Personalized insights powered by GenAI</p>
                </div>
                <div className="flex space-x-3">
                  <button
                    onClick={() => generateAIRecommendation('efficiency')}
                    disabled={isGeneratingAI}
                    className="bg-gradient-to-r from-green-500 to-blue-600 hover:from-green-600 hover:to-blue-700 disabled:opacity-50 text-white px-4 py-2 rounded-lg flex items-center space-x-2 transition-all duration-200"
                  >
                    {isGeneratingAI ? (
                      <Loader2 className="w-4 h-4 animate-spin" />
                    ) : (
                      <TrendingUp className="w-4 h-4" />
                    )}
                    <span>Efficiency Tips</span>
                  </button>
                  <button
                    onClick={() => generateAIRecommendation('maintenance')}
                    disabled={isGeneratingAI}
                    className="bg-gradient-to-r from-orange-500 to-red-600 hover:from-orange-600 hover:to-red-700 disabled:opacity-50 text-white px-4 py-2 rounded-lg flex items-center space-x-2 transition-all duration-200"
                  >
                    {isGeneratingAI ? (
                      <Loader2 className="w-4 h-4 animate-spin" />
                    ) : (
                      <AlertCircle className="w-4 h-4" />
                    )}
                    <span>Maintenance</span>
                  </button>
                </div>
              </div>

              {aiRecommendations && (
                <div className="space-y-6">
                  {aiRecommendations.recommendations.map((rec, index) => (
                    <div key={index} className="bg-white/5 border border-white/10 rounded-lg p-6">
                      <div className="flex items-start justify-between mb-4">
                        <div>
                          <h3 className="text-xl font-semibold text-white mb-2">{rec.recommendation_title}</h3>
                          <div className="flex items-center space-x-4 mb-3">
                            <span className={`px-3 py-1 rounded-full text-xs font-medium ${getPriorityColor(rec.priority_level)}`}>
                              {rec.priority_level.toUpperCase()}
                            </span>
                            <div className="flex items-center space-x-1 text-sm text-gray-400">
                              <Target className="w-4 h-4" />
                              <span>Impact: {rec.impact_score}/10</span>
                            </div>
                            <div className="flex items-center space-x-1 text-sm text-gray-400">
                              <Brain className="w-4 h-4" />
                              <span>{rec.ai_model_used}</span>
                            </div>
                          </div>
                          <p className="text-blue-300 text-sm bg-blue-400/10 rounded-lg p-3">
                            {rec.performance_analysis}
                          </p>
                        </div>
                      </div>
                      <div className="prose prose-invert max-w-none">
                        <div className="text-gray-300 whitespace-pre-wrap">
                          {rec.recommendation_text}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {!aiRecommendations && (
                <div className="text-center py-12">
                  <Lightbulb className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-300 text-lg mb-2">Generate AI Recommendations</p>
                  <p className="text-gray-400">Click the buttons above to get personalized insights</p>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AIInsightsPage;