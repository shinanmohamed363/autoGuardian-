import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Brain,
  Zap,
  CheckCircle,
  Clock,
  AlertTriangle,
  TrendingUp,
  Wrench,
  Target,
  LogOut,
  Filter,
  RefreshCw,
  Eye,
  Check
} from 'lucide-react';
import { apiService, Recommendation } from '../services/apiService';

const RecommendationsPage: React.FC = () => {
  const user = JSON.parse(localStorage.getItem('user') || '{}');
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [filter, setFilter] = useState<'all' | 'unread' | 'high_priority'>('all');

  useEffect(() => {
    loadRecommendations();
  }, [filter]);

  const loadRecommendations = async () => {
    try {
      setIsLoading(true);
      const params: any = {};
      if (filter === 'unread') params.unread_only = true;
      if (filter === 'high_priority') params.priority = 'high';
      
      const response = await apiService.getRecommendations(user.id, params);
      setRecommendations(response.recommendations || []);
    } catch (error) {
      console.error('Failed to load recommendations:', error);
      // Mock data for demonstration
      setRecommendations([
        {
          id: 1,
          user_id: user.id,
          vehicle_id: 1,
          recommendation_type: 'efficiency',
          title: 'Optimize Highway Driving Patterns',
          description: `## Efficiency Optimization Recommendations

Based on your driving data, here are personalized recommendations to improve fuel efficiency:

### 🎯 Key Insights
- Current highway efficiency: 9.2 L/100km
- Optimal range: 7.8-8.2 L/100km  
- Potential savings: $450/year

### 💡 Recommended Actions
1. **Maintain consistent speeds** between 90-100 km/h
2. **Use cruise control** on highways when possible
3. **Plan routes** to avoid heavy traffic periods
4. **Check tire pressure** monthly (optimal: 32-35 PSI)

### 📊 Expected Results
- 15-20% improvement in highway fuel efficiency
- Estimated annual savings: $400-500
- Reduced emissions: 280kg CO2/year`,
          priority: 'high',
          status: 'new',
          implementation_notes: null,
          created_at: '2025-09-01T10:30:00',
          updated_at: '2025-09-01T10:30:00'
        },
        {
          id: 2,
          user_id: user.id,
          vehicle_id: 1,
          recommendation_type: 'maintenance',
          title: 'Preventive Maintenance Schedule',
          description: `## Maintenance Recommendations

### 🔧 Upcoming Maintenance (Next 30 Days)
- **Air Filter**: Replace at 18,000 km (current: 17,200 km)
- **Tire Rotation**: Due every 10,000 km (last done: 12,500 km ago)

### ⚠️ Monitor Closely  
- **Brake Pads**: 30% remaining (inspect monthly)
- **Engine Oil**: Change in 2,000 km

### 💰 Cost Estimate
- Total estimated cost: $280-340
- Potential savings vs reactive maintenance: $150-200`,
          priority: 'medium',
          status: 'read',
          implementation_notes: null,
          created_at: '2025-08-28T14:15:00',
          updated_at: '2025-08-28T14:15:00'
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleMarkRead = async (recommendationId: number) => {
    try {
      await apiService.markRecommendationRead(recommendationId);
      setRecommendations(recommendations.map(rec => 
        rec.id === recommendationId ? { ...rec, status: 'read' } : rec
      ));
    } catch (error) {
      console.error('Failed to mark as read:', error);
    }
  };

  const handleMarkImplemented = async (recommendationId: number) => {
    try {
      await apiService.markRecommendationImplemented(recommendationId);
      setRecommendations(recommendations.map(rec => 
        rec.id === recommendationId ? { ...rec, status: 'implemented' } : rec
      ));
    } catch (error) {
      console.error('Failed to mark as implemented:', error);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    window.location.href = '/';
  };

  const getPriorityIcon = (priority: string) => {
    switch (priority) {
      case 'high': 
      case 'critical': return <AlertTriangle className="text-red-400" size={20} />;
      case 'medium': return <Clock className="text-yellow-400" size={20} />;
      case 'low': return <CheckCircle className="text-green-400" size={20} />;
      default: return <CheckCircle className="text-green-400" size={20} />;
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'efficiency': return <TrendingUp className="text-blue-400" size={20} />;
      case 'maintenance': return <Wrench className="text-purple-400" size={20} />;
      default: return <Target className="text-gray-400" size={20} />;
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400 mb-4"></div>
          <p className="text-white">Loading AI recommendations...</p>
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
                <Link to="/vehicles" className="text-gray-300 hover:text-white transition-colors">Vehicles</Link>
                <Link to="/analytics" className="text-gray-300 hover:text-white transition-colors">Analytics</Link>
                <Link to="/recommendations" className="text-white hover:text-blue-300 transition-colors">AI Insights</Link>
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
            <h1 className="text-4xl font-bold text-white mb-2 flex items-center space-x-3">
              <Brain className="text-purple-400" size={40} />
              <span>AI Recommendations</span>
            </h1>
            <p className="text-xl text-gray-300">Personalized insights powered by machine learning</p>
          </div>
          <div className="flex space-x-4">
            <button
              onClick={loadRecommendations}
              className="flex items-center space-x-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors duration-200"
            >
              <RefreshCw size={16} />
              <span>Refresh</span>
            </button>
          </div>
        </div>

        {/* Filters */}
        <div className="flex space-x-4 mb-8">
          <button
            onClick={() => setFilter('all')}
            className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
              filter === 'all' ? 'bg-blue-600 text-white' : 'bg-white/10 text-gray-300 hover:bg-white/20'
            }`}
          >
            <Filter size={16} />
            <span>All</span>
          </button>
          <button
            onClick={() => setFilter('unread')}
            className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
              filter === 'unread' ? 'bg-blue-600 text-white' : 'bg-white/10 text-gray-300 hover:bg-white/20'
            }`}
          >
            <Eye size={16} />
            <span>Unread</span>
          </button>
          <button
            onClick={() => setFilter('high_priority')}
            className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
              filter === 'high_priority' ? 'bg-blue-600 text-white' : 'bg-white/10 text-gray-300 hover:bg-white/20'
            }`}
          >
            <AlertTriangle size={16} />
            <span>High Priority</span>
          </button>
        </div>

        {/* Recommendations List */}
        {recommendations.length > 0 ? (
          <div className="space-y-6">
            {recommendations.map((recommendation) => (
              <div key={recommendation.id} className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
                <div className="flex justify-between items-start mb-4">
                  <div className="flex items-center space-x-3">
                    {getCategoryIcon(recommendation.recommendation_type)}
                    <div>
                      <h3 className="text-xl font-semibold text-white">{recommendation.title}</h3>
                      <p className="text-gray-400 text-sm">AI Generated Recommendation</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-3">
                    {getPriorityIcon(recommendation.priority)}
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                      recommendation.priority === 'high' || recommendation.priority === 'critical'
                        ? 'bg-red-600/20 text-red-400' 
                        : recommendation.priority === 'medium'
                        ? 'bg-yellow-600/20 text-yellow-400'
                        : 'bg-green-600/20 text-green-400'
                    }`}>
                      {recommendation.priority} priority
                    </span>
                    {recommendation.status === 'new' && (
                      <span className="bg-blue-600 text-white text-xs px-2 py-1 rounded">New</span>
                    )}
                  </div>
                </div>

                <div className="mb-4">
                  <div className="flex items-center space-x-4 mb-3">
                    <div className="flex items-center space-x-2">
                      <Zap className="text-yellow-400" size={16} />
                      <span className="text-gray-300 text-sm">Type: {recommendation.recommendation_type}</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Target className="text-green-400" size={16} />
                      <span className="text-gray-300 text-sm">Status: {recommendation.status}</span>
                    </div>
                  </div>
                </div>

                <div className="bg-white/5 rounded-lg p-4 mb-4">
                  <div className="prose prose-sm max-w-none text-gray-300">
                    {recommendation.description.split('\n').map((line: string, index: number) => (
                      <p key={index} className="mb-2">{line}</p>
                    ))}
                  </div>
                </div>

                <div className="flex justify-between items-center">
                  <span className="text-gray-400 text-sm">
                    Created: {new Date(recommendation.created_at).toLocaleDateString()}
                  </span>
                  <div className="flex space-x-3">
                    {recommendation.status === 'new' && (
                      <button
                        onClick={() => handleMarkRead(recommendation.id)}
                        className="flex items-center space-x-2 bg-blue-600/20 hover:bg-blue-600/30 text-blue-400 px-3 py-1 rounded-lg transition-colors text-sm"
                      >
                        <Eye size={14} />
                        <span>Mark Read</span>
                      </button>
                    )}
                    {recommendation.status !== 'implemented' && (
                      <button
                        onClick={() => handleMarkImplemented(recommendation.id)}
                        className="flex items-center space-x-2 bg-green-600/20 hover:bg-green-600/30 text-green-400 px-3 py-1 rounded-lg transition-colors text-sm"
                      >
                        <Check size={14} />
                        <span>Mark Implemented</span>
                      </button>
                    )}
                    {recommendation.status === 'implemented' && (
                      <span className="flex items-center space-x-2 bg-green-600/20 text-green-400 px-3 py-1 rounded-lg text-sm">
                        <CheckCircle size={14} />
                        <span>Implemented</span>
                      </span>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-16">
            <div className="bg-white/5 backdrop-blur-md border border-white/20 rounded-2xl p-12 max-w-md mx-auto">
              <Brain size={64} className="mx-auto mb-6 text-gray-400 opacity-50" />
              <h2 className="text-2xl font-semibold text-white mb-4">No Recommendations Yet</h2>
              <p className="text-gray-300 mb-6">Add some vehicles and fuel records to start receiving AI-powered insights and recommendations.</p>
              <Link
                to="/vehicles"
                className="inline-flex items-center space-x-2 bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg transition-colors duration-200"
              >
                <span>Get Started</span>
              </Link>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default RecommendationsPage;