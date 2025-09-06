import { apiCall } from './authService';

// Vehicle Management
export interface Vehicle {
  id?: number;
  user_id?: number;
  vehicle_name: string;
  display_name?: string;
  make: string;
  model: string;
  year: number;
  vehicle_class: string;
  engine_size: number;
  engine_info?: string;
  cylinders: number;
  transmission: string;
  fuel_type: string;
  tank_capacity: number;
  starting_odometer_value: number;
  odo_meter_when_buy_vehicle: number;
  full_tank_capacity: number;
  initial_tank_percentage: number;
  current_odometer?: number;
  total_distance_driven?: number;
  fuel_records_count?: number;
  is_active?: boolean;
  created_at?: string;
  updated_at?: string;
  latest_fuel_record?: any;
  average_consumption_30d?: number;
  consumption_by_type?: any;
}

// Fuel Records
export interface FuelRecord {
  id?: number;
  vehicle_id: number;
  record_date: string;
  record_time: string;
  existing_tank_percentage: number;
  after_refuel_percentage: number;
  odo_meter_current_value: number;
  driving_type: 'city' | 'highway' | 'mix';
  location: string;
  fuel_price: number; // cents per liter
  notes?: string;
  // Calculated fields (returned by backend)
  calculated_fuel_added?: number;
  total_cost?: number;
  km_driven_since_last?: number;
  actual_consumption_l_100km?: number;
  fuel_efficiency_rating?: string;
  cost_per_km?: number;
  fuel_percentage_added?: number;
  fuel_price_per_liter?: number;
  datetime?: string;
  created_at?: string;
  updated_at?: string;
}

// AI Recommendations
export interface Recommendation {
  id: number;
  user_id: number;
  vehicle_id: number | null;
  recommendation_type: 'efficiency' | 'maintenance';
  title: string;
  description: string;
  priority: 'low' | 'medium' | 'high' | 'critical';
  status: 'new' | 'read' | 'implemented';
  implementation_notes: string | null;
  created_at: string;
  updated_at: string;
}

// Vehicle Sales
export interface VehicleSale {
  id: number;
  user_id: number;
  vehicle_id: number;
  selling_price: number;
  minimum_price?: number; // Only visible to owner
  features: string[];
  description?: string;
  is_active: boolean;
  is_sold: boolean;
  created_at: string;
  updated_at: string;
  vehicle?: {
    vehicle_name: string;
    make: string;
    model: string;
    year: number;
    vehicle_class: string;
    engine_size: number;
    fuel_type: string;
    transmission: string;
    current_odometer?: number;
    tank_capacity: number;
    cylinders?: number;
  };
  seller?: {
    name: string;
    location: string;
  };
  negotiations_count?: number;
}

// Negotiation
export interface Negotiation {
  id: number;
  vehicle_sale_id: number;
  buyer_name: string;
  buyer_email: string;
  buyer_contact?: string;
  final_offer: number;
  chat_history: ChatMessage[];
  status: 'pending' | 'accepted' | 'rejected';
  created_at: string;
  updated_at: string;
}

export interface ChatMessage {
  sender: 'buyer' | 'system';
  message: string;
  timestamp: string;
}

export interface NegotiationResponse {
  response: string;
  current_offer: number;
  is_final: boolean;
  negotiation_id: number;
  chat_history: ChatMessage[];
  contact_collected?: boolean;
  final_price?: number;
}

// Analytics Interfaces
export interface DashboardAnalytics {
  user_summary: {
    total_vehicles: number;
    total_fuel_records: number;
    total_distance: number;
    total_fuel_consumed: number;
    average_fuel_efficiency: number;
    total_fuel_cost: number;
    active_recommendations: number;
  };
  recent_activity: Array<{
    type: 'fuel_record' | 'vehicle_added' | 'recommendation';
    description: string;
    date: string;
    vehicle_name?: string;
  }>;
  fuel_efficiency_trend: Array<{
    date: string;
    efficiency: number;
    vehicle_name: string;
  }>;
  cost_analysis: {
    monthly_cost: number;
    cost_per_km: number;
    cost_trend: Array<{
      month: string;
      cost: number;
    }>;
  };
  top_vehicles: Array<{
    vehicle_name: string;
    efficiency: number;
    total_distance: number;
    fuel_consumed: number;
  }>;
}

export interface ComprehensiveReport {
  vehicle_info: Vehicle;
  summary_stats: {
    total_distance: number;
    total_fuel: number;
    average_efficiency: number;
    total_cost: number;
    number_of_records: number;
  };
  efficiency_trend: Array<{
    date: string;
    efficiency: number;
    distance: number;
  }>;
  cost_analysis: {
    cost_per_km: number;
    monthly_costs: Array<{
      month: string;
      cost: number;
    }>;
  };
  recommendations: Recommendation[];
}

// ML Predictions
export interface MLPrediction {
  message: string;
  prediction: {
    combined_l_100km: number;
    highway_l_100km: number;
    city_l_100km: number;
    emissions_g_km: number;
    efficiency_rating: string;
    efficiency_stars: number;
    mpg_equivalent: number;
    annual_fuel_cost: number;
    annual_co2_emissions: number;
    prediction_metadata: {
      model_used: string;
      prediction_date: string;
      features_used: string[];
      preprocessing_applied: boolean;
    };
  };
  vehicle_id: number;
  vehicle_info: {
    make: string;
    model: string;
    year: number;
    engine_info: string;
  };
}

// AI Recommendations
export interface AIRecommendation {
  message: string;
  recommendations: Array<{
    recommendation_type: string;
    recommendation_title: string;
    recommendation_text: string;
    performance_analysis: string;
    priority_level: 'low' | 'medium' | 'high' | 'critical';
    category: string;
    impact_score: number;
    ai_model_used: string;
    confidence_level: number;
    vehicle_id: number;
  }>;
}

export const apiService = {
  // Vehicle Management
  async registerVehicle(vehicleData: Vehicle) {
    return apiCall('/vehicles', {
      method: 'POST',
      body: JSON.stringify(vehicleData),
    });
  },

  async getVehicles() {
    return apiCall('/vehicles');
  },

  async getVehicle(vehicleId: number) {
    return apiCall(`/vehicles/${vehicleId}`);
  },

  async updateVehicle(vehicleId: number, vehicleData: Partial<Vehicle>) {
    return apiCall(`/vehicles/${vehicleId}`, {
      method: 'PUT',
      body: JSON.stringify(vehicleData),
    });
  },

  async deleteVehicle(vehicleId: number) {
    return apiCall(`/vehicles/${vehicleId}`, {
      method: 'DELETE',
    });
  },

  // Fuel Records Management
  async addFuelRecord(fuelRecord: FuelRecord) {
    return apiCall('/fuel-records', {
      method: 'POST',
      body: JSON.stringify(fuelRecord),
    });
  },

  async getFuelRecords(vehicleId: number, params?: { limit?: number; days?: number }) {
    const queryParams = params ? new URLSearchParams(params as any).toString() : '';
    return apiCall(`/fuel-records/${vehicleId}${queryParams ? '?' + queryParams : ''}`);
  },

  async getFuelRecord(recordId: number) {
    return apiCall(`/fuel-records/record/${recordId}`);
  },

  async updateFuelRecord(recordId: number, recordData: Partial<FuelRecord>) {
    return apiCall(`/fuel-records/record/${recordId}`, {
      method: 'PUT',
      body: JSON.stringify(recordData),
    });
  },

  async deleteFuelRecord(recordId: number) {
    return apiCall(`/fuel-records/record/${recordId}`, {
      method: 'DELETE',
    });
  },

  async validateOdometer(vehicleId: number, odometerReading: number) {
    return apiCall('/fuel-records/validate-odometer', {
      method: 'POST',
      body: JSON.stringify({
        vehicle_id: vehicleId,
        odometer_reading: odometerReading
      }),
    });
  },

  // ML Predictions
  async generateMLPrediction(vehicleId: number) {
    return apiCall('/predictions', {
      method: 'POST',
      body: JSON.stringify({ vehicle_id: vehicleId }),
    });
  },

  // AI Recommendations
  async testGenAI() {
    return apiCall('/recommendations/test-genai');
  },

  async generateRecommendation(vehicleId: number, recommendationType: 'efficiency' | 'maintenance') {
    return apiCall('/recommendations/generate', {
      method: 'POST',
      body: JSON.stringify({
        vehicle_id: vehicleId,
        recommendation_type: recommendationType
      }),
    });
  },

  // Alias for AIInsightsPage compatibility
  async generateAIRecommendation(vehicleId: number, recommendationType: 'efficiency' | 'maintenance') {
    return apiCall('/recommendations/generate', {
      method: 'POST',
      body: JSON.stringify({
        vehicle_id: vehicleId,
        recommendation_type: recommendationType
      }),
    });
  },

  async getRecommendations(userId: number, params?: {
    status?: 'new' | 'read' | 'implemented';
    recommendation_type?: 'efficiency' | 'maintenance';
    priority?: 'low' | 'medium' | 'high' | 'critical'
  }) {
    const queryParams = params ? new URLSearchParams(params as any).toString() : '';
    return apiCall(`/recommendations/${userId}${queryParams ? '?' + queryParams : ''}`);
  },

  async getVehicleRecommendations(vehicleId: number) {
    return apiCall(`/recommendations/vehicle/${vehicleId}`);
  },

  async getRecommendation(recommendationId: number) {
    return apiCall(`/recommendations/${recommendationId}`);
  },

  async getRecommendationsSummary() {
    return apiCall('/recommendations/summary');
  },

  async markRecommendationRead(recommendationId: number) {
    return apiCall(`/recommendations/${recommendationId}/read`, {
      method: 'PUT',
    });
  },

  async markRecommendationImplemented(recommendationId: number, notes?: string) {
    return apiCall(`/recommendations/${recommendationId}/implement`, {
      method: 'PUT',
      body: JSON.stringify({ implementation_notes: notes }),
    });
  },

  // Analytics & Statistics
  async getDashboardAnalytics(userId: number): Promise<DashboardAnalytics> {
    return apiCall(`/analytics/dashboard/${userId}`);
  },

  async getComprehensiveReport(vehicleId: number, startDate: string, endDate: string): Promise<ComprehensiveReport> {
    return apiCall(`/analytics/comprehensive-report/${vehicleId}`, {
      method: 'POST',
      body: JSON.stringify({
        start_date: startDate,
        end_date: endDate
      }),
    });
  },

  async getDrivingPatterns(vehicleId: number) {
    return apiCall(`/analytics/driving-patterns/${vehicleId}`);
  },

  async getConsumptionTrends(vehicleId: number) {
    return apiCall(`/analytics/consumption-trends/${vehicleId}`);
  },

  // Vehicle Sales API
  async createVehicleSale(saleData: {
    vehicle_id: number;
    selling_price: number;
    minimum_price: number;
    features: string[];
    description?: string;
  }) {
    return apiCall('/vehicle-sales', {
      method: 'POST',
      body: JSON.stringify(saleData),
    });
  },

  async getVehicleSales(params?: { limit?: number; offset?: number }) {
    const queryParams = params ? new URLSearchParams(params as any).toString() : '';
    return apiCall(`/vehicle-sales${queryParams ? '?' + queryParams : ''}`);
  },

  async getMyVehicleSales() {
    return apiCall('/vehicle-sales/my-sales');
  },

  async getVehicleSale(saleId: number) {
    return apiCall(`/vehicle-sales/${saleId}`);
  },

  async updateVehicleSale(saleId: number, updateData: {
    selling_price?: number;
    minimum_price?: number;
    features?: string[];
    description?: string;
    is_active?: boolean;
  }) {
    return apiCall(`/vehicle-sales/${saleId}`, {
      method: 'PUT',
      body: JSON.stringify(updateData),
    });
  },

  async deleteVehicleSale(saleId: number) {
    return apiCall(`/vehicle-sales/${saleId}`, {
      method: 'DELETE',
    });
  },

  // Negotiation API
  async startNegotiation(saleId: number, message: string) {
    return apiCall(`/vehicle-sales/${saleId}/negotiate`, {
      method: 'POST',
      body: JSON.stringify({ message }),
    });
  },

  async continueNegotiation(saleId: number, negotiationId: number, message: string) {
    return apiCall(`/vehicle-sales/${saleId}/negotiate`, {
      method: 'POST',
      body: JSON.stringify({ message, negotiation_id: negotiationId }),
    });
  },

  async getSaleNegotiations(saleId: number) {
    return apiCall(`/vehicle-sales/${saleId}/negotiations`);
  },

  async acceptNegotiation(negotiationId: number) {
    return apiCall(`/vehicle-sales/negotiations/${negotiationId}/accept`, {
      method: 'PUT',
    });
  },

  async rejectNegotiation(negotiationId: number) {
    return apiCall(`/vehicle-sales/negotiations/${negotiationId}/reject`, {
      method: 'PUT',
    });
  }
};