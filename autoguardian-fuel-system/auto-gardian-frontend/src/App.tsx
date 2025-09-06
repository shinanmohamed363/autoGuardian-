import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import Dashboard from './pages/Dashboard';
import VehiclesPage from './pages/VehiclesPage';
import FuelRecordsPage from './pages/FuelRecordsPage';
import AIInsightsPage from './pages/AIInsightsPage';
import RecommendationsPage from './pages/RecommendationsPage';
import MarketplacePage from './pages/MarketplacePage';
import VehicleDetailsPage from './pages/VehicleDetailsPage';
import SellerDashboard from './pages/SellerDashboard';

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const token = localStorage.getItem('access_token');
  return token ? <>{children}</> : <Navigate to="/login" replace />;
};

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route 
            path="/dashboard" 
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/vehicles" 
            element={
              <ProtectedRoute>
                <VehiclesPage />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/fuel-records/:vehicleId" 
            element={
              <ProtectedRoute>
                <FuelRecordsPage />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/ai-insights/:vehicleId" 
            element={
              <ProtectedRoute>
                <AIInsightsPage />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/recommendations" 
            element={
              <ProtectedRoute>
                <RecommendationsPage />
              </ProtectedRoute>
            } 
          />
          <Route path="/marketplace" element={<MarketplacePage />} />
          <Route path="/marketplace/:vehicleId" element={<VehicleDetailsPage />} />
          <Route 
            path="/seller-dashboard" 
            element={
              <ProtectedRoute>
                <SellerDashboard />
              </ProtectedRoute>
            } 
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
