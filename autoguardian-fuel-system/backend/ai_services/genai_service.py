"""
Google Generative AI Service for AutoGuardian Fuel Management System
"""

import google.generativeai as genai
import logging
from typing import Dict, Optional, List
import json

# Setup logging
logger = logging.getLogger(__name__)

class GenAIRecommendationService:
    """Service for generating AI-powered fuel efficiency and maintenance recommendations"""
    
    def __init__(self, api_key: str = "AIzaSyCTSwSJgM3xfBNz2xcLHBhAb2Fn1YTl0So"):
        """Initialize the GenAI service"""
        self.api_key = api_key
        self.model = None
        self.is_configured = False
        self.configure_genai()
    
    def configure_genai(self):
        """Configure Google Generative AI"""
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
            self.is_configured = True
            logger.info("✅ Google Generative AI configured successfully")
        except Exception as e:
            logger.error(f"❌ Failed to configure GenAI: {str(e)}")
            self.is_configured = False
    
    def generate_maintenance_recommendation(self, vehicle_data: Dict, fuel_analysis: Dict) -> Dict:
        """Generate AI-powered maintenance recommendations"""
        if not self.is_configured:
            return self._fallback_maintenance_recommendation(vehicle_data, fuel_analysis)
        
        try:
            # Create detailed prompt for maintenance recommendations
            prompt = self._create_maintenance_prompt(vehicle_data, fuel_analysis)
            
            # Generate content using Gemini
            response = self.model.generate_content(prompt)
            
            # Parse and structure the response
            return self._parse_maintenance_response(response.text, vehicle_data, fuel_analysis)
            
        except Exception as e:
            logger.error(f"❌ GenAI maintenance recommendation failed: {str(e)}")
            return self._fallback_maintenance_recommendation(vehicle_data, fuel_analysis)
    
    def generate_efficiency_recommendation(self, vehicle_data: Dict, fuel_analysis: Dict) -> Dict:
        """Generate AI-powered fuel efficiency recommendations"""
        if not self.is_configured:
            return self._fallback_efficiency_recommendation(vehicle_data, fuel_analysis)
        
        try:
            # Create detailed prompt for efficiency recommendations
            prompt = self._create_efficiency_prompt(vehicle_data, fuel_analysis)
            
            # Generate content using Gemini
            response = self.model.generate_content(prompt)
            
            # Parse and structure the response
            return self._parse_efficiency_response(response.text, vehicle_data, fuel_analysis)
            
        except Exception as e:
            logger.error(f"❌ GenAI efficiency recommendation failed: {str(e)}")
            return self._fallback_efficiency_recommendation(vehicle_data, fuel_analysis)
    
    def _create_maintenance_prompt(self, vehicle_data: Dict, fuel_analysis: Dict) -> str:
        """Create maintenance recommendation prompt"""
        actual_consumption = fuel_analysis.get('actual_consumption', 0)
        predicted_consumption = fuel_analysis.get('predicted_consumption', 0)
        performance_deviation = fuel_analysis.get('percentage_difference', 0)
        
        prompt = f"""
You are an expert automotive mechanic and fuel efficiency specialist. Analyze this vehicle's performance data and provide specific maintenance recommendations.

**Vehicle Details:**
- Make & Model: {vehicle_data.get('make', '')} {vehicle_data.get('model', '')}
- Year: {vehicle_data.get('year', '')}
- Engine: {vehicle_data.get('engine_size', '')}L, {vehicle_data.get('cylinders', '')} cylinders
- Transmission: {vehicle_data.get('transmission', '')}
- Fuel Type: {vehicle_data.get('fuel_type', '')}

**Performance Analysis:**
- Expected Fuel Consumption: {predicted_consumption:.2f} L/100km
- Actual Fuel Consumption: {actual_consumption:.2f} L/100km
- Performance Deviation: {performance_deviation:.1f}% {'worse' if performance_deviation > 0 else 'better'} than expected

**Driving Patterns:**
{self._format_driving_patterns(fuel_analysis.get('driving_patterns', {}))}

**Instructions:**
1. Analyze why the actual consumption differs from expected
2. Provide specific, actionable maintenance recommendations
3. Prioritize recommendations by impact on fuel efficiency
4. Include estimated cost savings potential
5. Use bullet points and clear formatting
6. Keep recommendations practical and achievable

**Response Format:**
## Maintenance Priority Analysis

### Immediate Actions (High Impact):
[List 2-3 high-priority maintenance items]

### Preventive Maintenance (Medium Impact):
[List 3-4 preventive maintenance items]

### Long-term Optimization (Low Impact):
[List 2-3 long-term maintenance items]

### Estimated Savings:
[Provide estimated monthly/yearly savings]

Please provide detailed, vehicle-specific recommendations based on the performance data.
"""
        return prompt
    
    def _create_efficiency_prompt(self, vehicle_data: Dict, fuel_analysis: Dict) -> str:
        """Create efficiency recommendation prompt"""
        actual_consumption = fuel_analysis.get('actual_consumption', 0)
        predicted_consumption = fuel_analysis.get('predicted_consumption', 0)
        
        prompt = f"""
You are a fuel efficiency expert and eco-driving coach. Analyze this vehicle's fuel consumption patterns and provide personalized driving recommendations.

**Vehicle Details:**
- Make & Model: {vehicle_data.get('make', '')} {vehicle_data.get('model', '')}
- Year: {vehicle_data.get('year', '')}
- Engine: {vehicle_data.get('engine_size', '')}L, {vehicle_data.get('cylinders', '')} cylinders
- Transmission: {vehicle_data.get('transmission', '')}

**Fuel Efficiency Analysis:**
- Expected Consumption: {predicted_consumption:.2f} L/100km
- Actual Consumption: {actual_consumption:.2f} L/100km
- Efficiency Gap: {abs(actual_consumption - predicted_consumption):.2f} L/100km

**Driving Patterns:**
{self._format_driving_patterns(fuel_analysis.get('driving_patterns', {}))}

**Instructions:**
1. Identify specific driving behavior improvements
2. Provide vehicle-specific eco-driving tips
3. Suggest route optimization strategies
4. Include seasonal driving considerations
5. Estimate potential fuel savings
6. Make recommendations practical and easy to follow

**Response Format:**
## Fuel Efficiency Optimization Guide

### Immediate Driving Improvements:
[List 3-4 actionable driving behavior changes]

### Vehicle-Specific Tips:
[Provide tips specific to this vehicle type]

### Route & Trip Planning:
[Suggest optimization strategies]

### Seasonal Considerations:
[Weather and seasonal driving tips]

### Potential Savings:
[Estimate monthly/yearly fuel and cost savings]

Please provide personalized, actionable recommendations for improving fuel efficiency.
"""
        return prompt
    
    def _format_driving_patterns(self, patterns: Dict) -> str:
        """Format driving patterns for prompt"""
        if not patterns:
            return "No detailed driving pattern data available"
        
        formatted = []
        for driving_type, data in patterns.items():
            consumption = data.get('consumption', 0)
            km = data.get('km', 0)
            formatted.append(f"- {driving_type.title()}: {consumption:.2f} L/100km ({km} km total)")
        
        return "\n".join(formatted)
    
    def _parse_maintenance_response(self, ai_response: str, vehicle_data: Dict, fuel_analysis: Dict) -> Dict:
        """Parse and structure maintenance recommendation response"""
        return {
            'recommendation_title': 'AI-Powered Maintenance Analysis',
            'recommendation_text': ai_response,
            'category': 'maintenance',
            'priority_level': 'high' if fuel_analysis.get('percentage_difference', 0) > 20 else 'medium',
            'impact_score': min(10.0, max(5.0, fuel_analysis.get('percentage_difference', 0) / 10)),
            'confidence_level': 0.85,
            'ai_model_used': 'gemini-2.0-flash',
            'generation_prompt': 'maintenance_analysis_v1',
            'performance_analysis': self._create_performance_summary(fuel_analysis)
        }
    
    def _parse_efficiency_response(self, ai_response: str, vehicle_data: Dict, fuel_analysis: Dict) -> Dict:
        """Parse and structure efficiency recommendation response"""
        return {
            'recommendation_title': 'Personalized Fuel Efficiency Guide',
            'recommendation_text': ai_response,
            'category': 'fuel_efficiency',
            'priority_level': 'medium',
            'impact_score': min(9.0, max(6.0, abs(fuel_analysis.get('percentage_difference', 0)) / 12)),
            'confidence_level': 0.82,
            'ai_model_used': 'gemini-2.0-flash',
            'generation_prompt': 'efficiency_optimization_v1',
            'performance_analysis': self._create_performance_summary(fuel_analysis)
        }
    
    def _create_performance_summary(self, fuel_analysis: Dict) -> str:
        """Create performance analysis summary"""
        actual = fuel_analysis.get('actual_consumption', 0)
        predicted = fuel_analysis.get('predicted_consumption', 0)
        deviation = fuel_analysis.get('percentage_difference', 0)
        
        if deviation > 20:
            status = "significantly higher than expected"
        elif deviation > 10:
            status = "moderately higher than expected"
        elif deviation > -10:
            status = "close to expected performance"
        else:
            status = "better than expected"
        
        return f"Vehicle consuming {actual:.2f} L/100km vs predicted {predicted:.2f} L/100km - {status}."
    
    def _fallback_maintenance_recommendation(self, vehicle_data: Dict, fuel_analysis: Dict) -> Dict:
        """Fallback maintenance recommendation when AI fails"""
        deviation = fuel_analysis.get('percentage_difference', 0)
        
        if deviation > 30:
            text = """## Critical Maintenance Required

### Immediate Actions (High Priority):
• **Air Filter Replacement** - Clogged filters can increase consumption by 10-15%
• **Spark Plug Inspection** - Worn plugs cause incomplete combustion
• **Tire Pressure Check** - Under-inflated tires increase rolling resistance

### Engine System Check:
• **Oxygen Sensors** - Faulty sensors affect fuel mixture
• **Fuel Injector Cleaning** - Dirty injectors reduce efficiency
• **Mass Airflow Sensor** - Clean or replace if contaminated

### Estimated Impact:
Monthly savings: $80-150 with proper maintenance
Efficiency improvement: 15-25% possible"""

        elif deviation > 10:
            text = """## Preventive Maintenance Schedule

### Regular Maintenance (Medium Priority):
• **Oil Change** - Use recommended viscosity for your climate
• **Air Filter Check** - Replace if dirty or clogged
• **Tire Rotation & Pressure** - Maintain proper alignment

### System Optimization:
• **Engine Tune-up** - Ensure all systems running efficiently
• **Fuel System Service** - Clean injectors and fuel lines
• **Exhaust System Check** - Ensure proper exhaust flow

### Estimated Impact:
Monthly savings: $30-60 with regular maintenance
Efficiency improvement: 8-15% possible"""
        
        else:
            text = """## Optimization Maintenance

### Preventive Care:
• **Regular Oil Changes** - Maintain engine health
• **Filter Replacements** - Keep air and fuel filters clean
• **Fluid Level Checks** - Ensure optimal system performance

### Performance Enhancement:
• **Quality Fuel** - Use recommended octane rating
• **Seasonal Maintenance** - Adapt to weather conditions
• **Drive Belt Inspection** - Ensure proper engine accessories operation

### Estimated Impact:
Monthly savings: $15-30 with optimization
Efficiency improvement: 3-8% possible"""

        return {
            'recommendation_title': 'Maintenance Analysis & Recommendations',
            'recommendation_text': text,
            'category': 'maintenance',
            'priority_level': 'high' if deviation > 20 else 'medium',
            'impact_score': min(9.0, max(6.0, deviation / 10)),
            'confidence_level': 0.75,
            'ai_model_used': 'fallback-system',
            'generation_prompt': 'maintenance_fallback_v1',
            'performance_analysis': self._create_performance_summary(fuel_analysis)
        }
    
    def _fallback_efficiency_recommendation(self, vehicle_data: Dict, fuel_analysis: Dict) -> Dict:
        """Fallback efficiency recommendation when AI fails"""
        text = """## Fuel Efficiency Optimization Guide

### Immediate Driving Improvements:
• **Smooth Acceleration** - Gradual acceleration saves 15-30% fuel
• **Maintain Steady Speed** - Use cruise control on highways
• **Anticipate Traffic** - Coast to red lights and slow traffic
• **Optimal Speed Range** - Drive 50-80 km/h when possible

### Vehicle-Specific Tips:
• **Remove Excess Weight** - Every 45kg reduces efficiency by 1-2%
• **Aerodynamics** - Remove roof racks/carriers when not in use
• **Tire Pressure** - Check monthly, under-inflation wastes fuel
• **A/C Usage** - Use A/C above 50 km/h, windows below that speed

### Trip Planning Strategies:
• **Combine Errands** - Plan efficient routes
• **Avoid Peak Hours** - Less idling in traffic
• **Pre-condition Vehicle** - Warm up efficiently in winter
• **Regular Commute Analysis** - Find most efficient routes

### Potential Savings:
• Monthly fuel savings: $40-80 with improved driving habits
• Annual savings: $500-1000 possible
• Efficiency improvement: 10-20% achievable"""

        return {
            'recommendation_title': 'Personalized Driving Efficiency Guide',
            'recommendation_text': text,
            'category': 'fuel_efficiency', 
            'priority_level': 'medium',
            'impact_score': 7.5,
            'confidence_level': 0.80,
            'ai_model_used': 'fallback-system',
            'generation_prompt': 'efficiency_fallback_v1',
            'performance_analysis': self._create_performance_summary(fuel_analysis)
        }
    
    def test_connection(self) -> Dict:
        """Test the GenAI connection"""
        try:
            if not self.is_configured:
                self.configure_genai()
            
            if self.is_configured:
                # Simple test prompt
                test_response = self.model.generate_content("Say 'GenAI connection successful' if you can see this.")
                return {
                    'status': 'success',
                    'message': 'GenAI connection successful',
                    'response': test_response.text[:100] + '...' if len(test_response.text) > 100 else test_response.text
                }
            else:
                return {'status': 'error', 'message': 'GenAI not properly configured'}
                
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

# Global service instance
_genai_service = None

def get_genai_service():
    """Get global GenAI service instance"""
    global _genai_service
    if _genai_service is None:
        _genai_service = GenAIRecommendationService()
    return _genai_service