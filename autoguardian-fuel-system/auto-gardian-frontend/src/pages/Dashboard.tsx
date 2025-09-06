import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Car,
  Fuel,
  TrendingUp,
  DollarSign,
  AlertTriangle,
  CheckCircle,
  Activity,
  BarChart3,
  Zap,
  Users,
  Settings,
  LogOut,
  Plus,
  Brain,
  Gauge,
  Calendar,
  MapPin
} from 'lucide-react';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import { apiService, DashboardAnalytics } from '../services/apiService';

const Dashboard: React.FC = () => {
  const user = JSON.parse(localStorage.getItem('user') || '{}');
  const [analytics, setAnalytics] = useState<DashboardAnalytics | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedPeriod, setSelectedPeriod] = useState('30d');

  useEffect(() => {
    loadDashboardData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedPeriod]);

  const loadDashboardData = async () => {
    // Check if user is properly logged in
    const token = localStorage.getItem('access_token');
    if (!token || !user.id) {
      console.log('No valid token or user data, using mock data');
      setIsLoading(false);
      return;
    }

    try {
      setIsLoading(true);
      const data = await apiService.getDashboardAnalytics(user.id);
      setAnalytics(data);
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
      // Set mock data for demonstration
      setAnalytics({
        user_summary: {
          total_vehicles: 2,
          total_fuel_records: 15,
          total_distance: 5420,
          total_fuel_consumed: 660,
          average_fuel_efficiency: 8.2,
          total_fuel_cost: 1248.50,
          active_recommendations: 5
        },
        recent_activity: [
          {
            type: 'fuel_record',
            description: 'Added fuel record for Honda Civic',
            date: '2025-09-01T10:30:00',
            vehicle_name: 'Honda Civic'
          },
          {
            type: 'recommendation',
            description: 'New AI recommendation: Optimize Highway Driving',
            date: '2025-09-01T09:15:00'
          }
        ],
        fuel_efficiency_trend: [
          { date: '2025-08-01', efficiency: 8.5, vehicle_name: 'Honda Civic' },
          { date: '2025-08-08', efficiency: 8.3, vehicle_name: 'Honda Civic' },
          { date: '2025-08-15', efficiency: 8.1, vehicle_name: 'Honda Civic' },
          { date: '2025-08-22', efficiency: 7.8, vehicle_name: 'Honda Civic' },
          { date: '2025-08-29', efficiency: 7.6, vehicle_name: 'Honda Civic' }
        ],
        cost_analysis: {
          monthly_cost: 385.20,
          cost_per_km: 0.23,
          cost_trend: [
            { month: '2025-01', cost: 340.20 },
            { month: '2025-02', cost: 385.20 },
            { month: '2025-03', cost: 420.10 }
          ]
        },
        top_vehicles: [
          {
            vehicle_name: 'Honda Civic',
            efficiency: 8.2,
            total_distance: 3420,
            fuel_consumed: 420
          },
          {
            vehicle_name: 'Toyota Corolla',
            efficiency: 7.8,
            total_distance: 2000,
            fuel_consumed: 240
          }
        ]
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    window.location.href = '/';
  };

  const efficiencyData = analytics?.fuel_efficiency_trend || [];
  const pieData = [
    { name: 'Fuel Costs', value: 65, color: '#3B82F6' },
    { name: 'Maintenance', value: 25, color: '#10B981' },
    { name: 'Insurance', value: 10, color: '#F59E0B' }
  ];

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400 mb-4"></div>
          <p className="text-white">Loading your dashboard...</p>
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
                <Link to="/dashboard" className="text-white hover:text-blue-300 transition-colors">Dashboard</Link>
                <Link to="/vehicles" className="text-gray-300 hover:text-white transition-colors">Vehicles</Link>
                <Link to="/marketplace" className="text-gray-300 hover:text-white transition-colors">Marketplace</Link>
                <Link to="/seller-dashboard" className="text-gray-300 hover:text-white transition-colors">My Sales</Link>
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
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">Dashboard Overview</h1>
          <p className="text-xl text-gray-300">Your AI-powered vehicle insights at a glance</p>
        </div>

        {/* Key Metrics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Total Vehicles</p>
                <p className="text-2xl font-bold text-white">{analytics?.user_summary?.total_vehicles || 0}</p>
              </div>
              <div className="bg-blue-600/20 p-3 rounded-lg">
                <Car className="text-blue-400" size={24} />
              </div>
            </div>
          </div>

          <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Fuel Records</p>
                <p className="text-2xl font-bold text-white">{analytics?.user_summary?.total_fuel_records || 0}</p>
              </div>
              <div className="bg-green-600/20 p-3 rounded-lg">
                <Fuel className="text-green-400" size={24} />
              </div>
            </div>
          </div>

          <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Total Distance</p>
                <p className="text-2xl font-bold text-white">{analytics?.user_summary?.total_distance?.toLocaleString() || 0} km</p>
              </div>
              <div className="bg-purple-600/20 p-3 rounded-lg">
                <Activity className="text-purple-400" size={24} />
              </div>
            </div>
          </div>

          <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Avg Efficiency</p>
                <p className="text-2xl font-bold text-white">{analytics?.user_summary?.average_fuel_efficiency || 0} L/100km</p>
              </div>
              <div className="bg-yellow-600/20 p-3 rounded-lg">
                <Gauge className="text-yellow-400" size={24} />
              </div>
            </div>
          </div>
        </div>

        {/* Charts Row */}
        <div className="grid lg:grid-cols-2 gap-8 mb-8">
          {/* Fuel Efficiency Trend */}
          <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xl font-semibold text-white">Fuel Efficiency Trend</h3>
              <div className="flex space-x-2">
                {['7d', '30d', '90d'].map((period) => (
                  <button
                    key={period}
                    onClick={() => setSelectedPeriod(period)}
                    className={`px-3 py-1 rounded-lg text-sm transition-colors ${
                      selectedPeriod === period
                        ? 'bg-blue-600 text-white'
                        : 'bg-white/10 text-gray-300 hover:bg-white/20'
                    }`}
                  >
                    {period}
                  </button>
                ))}
              </div>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={efficiencyData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                <XAxis dataKey="date" stroke="#9CA3AF" fontSize={12} />
                <YAxis stroke="#9CA3AF" fontSize={12} />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'rgba(15, 23, 42, 0.9)', 
                    border: '1px solid rgba(255,255,255,0.1)',
                    borderRadius: '8px',
                    color: 'white'
                  }} 
                />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="efficiency" 
                  stroke="#3B82F6" 
                  strokeWidth={2}
                  name="Actual"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Cost Breakdown */}
          <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
            <h3 className="text-xl font-semibold text-white mb-6">Cost Breakdown</h3>
            <div className="flex justify-center">
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {pieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: 'rgba(15, 23, 42, 0.9)', 
                      border: '1px solid rgba(255,255,255,0.1)',
                      borderRadius: '8px',
                      color: 'white'
                    }} 
                  />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* Quick Actions & Recent Recommendations */}
        <div className="grid lg:grid-cols-3 gap-8 mb-8">
          {/* Quick Actions */}
          <div className="lg:col-span-1 bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
            <h3 className="text-xl font-semibold text-white mb-4">Quick Actions</h3>
            <div className="space-y-3">
              <Link 
                to="/add-vehicle"
                className="flex items-center space-x-3 w-full p-3 bg-blue-600/20 hover:bg-blue-600/30 rounded-lg transition-colors"
              >
                <Plus className="text-blue-400" size={20} />
                <span className="text-white">Add Vehicle</span>
              </Link>
              <Link 
                to="/add-fuel-record"
                className="flex items-center space-x-3 w-full p-3 bg-green-600/20 hover:bg-green-600/30 rounded-lg transition-colors"
              >
                <Fuel className="text-green-400" size={20} />
                <span className="text-white">Log Fuel</span>
              </Link>
              <button className="flex items-center space-x-3 w-full p-3 bg-purple-600/20 hover:bg-purple-600/30 rounded-lg transition-colors">
                <Brain className="text-purple-400" size={20} />
                <span className="text-white">Generate AI Insights</span>
              </button>
            </div>
          </div>

          {/* Recent Activity */}
          <div className="lg:col-span-2 bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-semibold text-white">Recent Activity</h3>
              <Link to="/recommendations" className="text-blue-400 hover:text-blue-300 text-sm">
                View All
              </Link>
            </div>
            <div className="space-y-4">
              {analytics?.recent_activity?.slice(0, 3).map((activity, index) => (
                <div key={index} className="bg-white/5 rounded-lg p-4 border border-white/10">
                  <div className="flex justify-between items-start mb-2">
                    <div className="flex items-center space-x-2">
                      {activity.type === 'fuel_record' ? (
                        <Fuel className="text-green-400" size={16} />
                      ) : activity.type === 'recommendation' ? (
                        <Zap className="text-yellow-400" size={16} />
                      ) : (
                        <Car className="text-blue-400" size={16} />
                      )}
                      <span className="text-white font-medium">{activity.description}</span>
                    </div>
                    <span className="text-gray-400 text-xs">
                      {new Date(activity.date).toLocaleDateString()}
                    </span>
                  </div>
                  {activity.vehicle_name && (
                    <p className="text-gray-300 text-sm">Vehicle: {activity.vehicle_name}</p>
                  )}
                </div>
              )) || (
                <div className="text-center text-gray-400 py-8">
                  <Brain size={48} className="mx-auto mb-4 opacity-50" />
                  <p>No recent activity</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Feature Cards */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Link to="/vehicles" className="group bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6 hover:bg-white/15 transition-all duration-200">
            <div className="flex items-center justify-between mb-4">
              <Car className="text-blue-400 group-hover:scale-110 transition-transform" size={32} />
              <span className="text-blue-400 opacity-0 group-hover:opacity-100 transition-opacity">→</span>
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">Vehicle Management</h3>
            <p className="text-gray-300 text-sm">Manage your fleet and track performance</p>
          </Link>

          <Link to="/analytics" className="group bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6 hover:bg-white/15 transition-all duration-200">
            <div className="flex items-center justify-between mb-4">
              <BarChart3 className="text-green-400 group-hover:scale-110 transition-transform" size={32} />
              <span className="text-green-400 opacity-0 group-hover:opacity-100 transition-opacity">→</span>
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">Advanced Analytics</h3>
            <p className="text-gray-300 text-sm">Deep insights into your driving patterns</p>
          </Link>

          <Link to="/recommendations" className="group bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6 hover:bg-white/15 transition-all duration-200">
            <div className="flex items-center justify-between mb-4">
              <Brain className="text-purple-400 group-hover:scale-110 transition-transform" size={32} />
              <span className="text-purple-400 opacity-0 group-hover:opacity-100 transition-opacity">→</span>
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">AI Recommendations</h3>
            <p className="text-gray-300 text-sm">Personalized insights and suggestions</p>
          </Link>

          <Link to="/community" className="group bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6 hover:bg-white/15 transition-all duration-200">
            <div className="flex items-center justify-between mb-4">
              <Users className="text-cyan-400 group-hover:scale-110 transition-transform" size={32} />
              <span className="text-cyan-400 opacity-0 group-hover:opacity-100 transition-opacity">→</span>
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">Community</h3>
            <p className="text-gray-300 text-sm">Connect with other vehicle owners</p>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;