"""
AutoGuardian Fuel Management System - Negotiation Bot Service with GenAI Integration
"""

import re
import random
import logging
from typing import Dict, List, Tuple, Optional
from ai_services.genai_service import get_genai_service, GenAIRecommendationService

logger = logging.getLogger(__name__)

class NegotiationBot:
    """AI-powered negotiation bot for vehicle sales with GenAI integration"""
    
    def __init__(self):
        # Flexible negotiation steps - can extend based on conversation
        self.base_negotiation_steps = [
            0.95,  # First counter-offer: 5% reduction
            0.90,  # Second counter-offer: 10% reduction
            0.85,  # Third counter-offer: 15% reduction
            0.80,  # Fourth counter-offer: 20% reduction
            0.75   # Fifth offer: 25% reduction
        ]
        # Can extend to more steps for patient negotiators
        
        # Initialize GenAI service with gemini-2.0-flash for natural conversation
        try:
            self.genai_service = GenAIRecommendationService()
            self.use_ai = self.genai_service.is_configured
            if self.use_ai:
                logger.info("✅ GenAI Flash service initialized for natural negotiation")
            else:
                logger.warning("⚠️ GenAI Flash service not configured, using fallback responses")
        except Exception as e:
            logger.warning(f"⚠️ GenAI service not available, using fallback responses: {str(e)}")
            self.genai_service = None
            self.use_ai = False
        
        # Fallback responses when AI is not available
        self.positive_responses = [
            "I understand you're looking for a good deal!",
            "That's a reasonable request.",
            "I appreciate your interest in this vehicle.",
            "Let me see what I can do for you.",
            "I want to find a price that works for both of us."
        ]
        
        self.feature_highlights = [
            "This vehicle has been well-maintained with recent upgrades.",
            "The additional features I've added significantly increase the value.",
            "These improvements ensure better performance and reliability.",
            "The recent maintenance work saves you money in the long run."
        ]
        
        self.closing_phrases = [
            "This is my best price considering all the improvements.",
            "I think this is a fair price for the condition and features.",
            "Given the recent upgrades, this price offers excellent value.",
            "I believe this price reflects the true value of the vehicle."
        ]
    
    def extract_price_from_message(self, message: str) -> Optional[float]:
        """Extract price from user message"""
        # Look for numbers that could be prices
        price_patterns = [
            r'(?:Rs\.?\s*)?(\d+(?:,\d{3})*(?:\.\d{2})?)',  # Rs. 120000 or 120,000
            r'(\d+)k',  # 120k format
            r'(\d+)K',  # 120K format
        ]
        
        for pattern in price_patterns:
            match = re.search(pattern, message.replace(',', ''))
            if match:
                price_str = match.group(1)
                if 'k' in message.lower() or 'K' in message:
                    return float(price_str) * 1000
                else:
                    return float(price_str)
        
        return None
    
    def generate_ai_response(self, vehicle_sale: Dict, message: str, intent: str, 
                           current_offer: float, negotiation_round: int, 
                           is_final: bool, user_offer: Optional[float] = None, 
                           customer_style: str = 'standard') -> str:
        """Generate AI-powered natural language response"""
        if not self.use_ai or not self.genai_service:
            return None
            
        try:
            # Build context for the AI
            vehicle = vehicle_sale.get('vehicle', {})
            features = vehicle_sale.get('features', [])
            asking_price = vehicle_sale['selling_price']
            minimum_price = vehicle_sale['minimum_price']
            
            # Simple, conversational prompt for natural negotiation
            prompt = f"""
You are Kamal, a friendly car seller in Sri Lanka. Keep responses SHORT and natural.

**Your Car:** {vehicle.get('year', '')} {vehicle.get('make', '')} {vehicle.get('model', '')}
**Your asking price:** Rs. {asking_price:,.0f}
**Your final minimum:** Rs. {minimum_price:,.0f}
**Your current offer:** Rs. {current_offer:,.0f}
**Customer said:** "{message}"

**Rules:**
1. Keep responses 1-2 sentences maximum
2. If this is your final offer (Rs. {minimum_price:,.0f}), say: "My final price is Rs. {minimum_price:,.0f}. Are you interested?"
3. If customer agrees to ANY price (like Rs. {current_offer:,.0f}), say: "Great! Let's make a deal at Rs. {current_offer:,.0f}. I need your name and phone number to finalize."
4. Be natural and friendly, not robotic
5. Don't repeat yourself

**Current status:** {'This IS your final offer - cannot go lower' if is_final else 'You can still negotiate'}

Respond as Kamal - keep it short and conversational.
"""
            
            # Generate response using GenAI
            if hasattr(self.genai_service, 'model') and self.genai_service.model:
                response = self.genai_service.model.generate_content(prompt)
                ai_response = response.text.strip()
                
                # Clean up the response
                ai_response = self._clean_ai_response(ai_response, current_offer)
                
                logger.info(f"✅ Generated AI response for negotiation round {negotiation_round + 1}")
                return ai_response
            else:
                logger.warning("⚠️ GenAI model not available")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error generating AI response: {str(e)}")
            return None
    
    def _get_situation_context(self, intent: str, user_offer: Optional[float], minimum_price: float, is_final: bool) -> str:
        """Get context description for current negotiation situation"""
        if intent == 'price_inquiry':
            return "Customer is asking about the price - provide the current offer clearly"
        elif intent == 'price_reduction':
            if user_offer and user_offer < minimum_price * 0.8:
                return "Customer's offer is significantly below your minimum - explain value and counter reasonably"
            elif is_final:
                return "Customer wants your best price - give your FINAL MINIMUM price and clearly state it's final"
            else:
                return "Customer wants a better price - negotiate fairly while highlighting value"
        elif intent == 'agreement':
            return "Customer has agreed to the price - confirm and ask for contact details to proceed"
        elif intent == 'rejection':
            if is_final:
                return "Customer rejected your final offer - be understanding but firm"
            else:
                return "Customer rejected current offer - make a better offer while highlighting features"
        else:
            return "Customer's intent is unclear - engage naturally and guide toward price discussion"
    
    def _clean_ai_response(self, response: str, current_offer: float) -> str:
        """Clean and validate AI response"""
        # Remove any potential formatting issues
        response = re.sub(r'\n+', ' ', response)  # Replace multiple newlines with space
        response = re.sub(r'\s+', ' ', response)  # Replace multiple spaces with single space
        response = response.strip()
        
        # Ensure the response mentions the current offer if it doesn't already
        if 'Rs.' not in response and current_offer > 0:
            response = f"{response} My current offer is Rs. {current_offer:,.0f}."
        
        return response
    
    def analyze_message_intent(self, message: str, negotiation_history: List[Dict] = None) -> Dict:
        """Use AI to analyze customer message intent and conversation status"""
        if not self.use_ai or not self.genai_service:
            return {'intent': 'general', 'is_ready_to_finalize': False, 'wants_final_price': False}
        
        try:
            # Get recent conversation context
            recent_context = ""
            if negotiation_history:
                recent_messages = negotiation_history[-4:]  # Last 4 messages
                for msg in recent_messages:
                    sender = "Customer" if msg.get('sender') == 'buyer' else "Seller"
                    recent_context += f"{sender}: {msg.get('message', '')}\n"
            
            # AI prompt to understand customer intent
            intent_prompt = f"""
            You are analyzing a car sales negotiation. Look at the customer's message and determine their intent.

            **Recent conversation:**
            {recent_context}

            **Customer's latest message:** "{message}"

            Respond with ONLY this exact JSON format:
            {{
                "intent": "price_inquiry|price_reduction|agreement|rejection|general",
                "is_ready_to_finalize": true/false,
                "wants_final_price": true/false,
                "customer_mood": "eager|hesitant|aggressive|polite|neutral",
                "should_move_to_final": true/false,
                "proposed_final_price": number_or_null
            }}

            **IMPORTANT FINALIZATION DETECTION:**
            Set "is_ready_to_finalize": true AND extract "proposed_final_price" if customer says:
            - "okay lets finalized with [amount]"
            - "lets finalize at [amount]" 
            - "final price [amount]"
            - "make a deal at [amount]"
            - "agreed on [amount]"
            - "deal for [amount]"
            - "finalized with [amount]"
            - "okay [amount]" (after negotiation)
            
            **Other Guidelines:**
            - "wants_final_price": true if asking for best/final/lowest price (not proposing one)
            - "should_move_to_final": true if conversation should move to final price now
            - "proposed_final_price": extract ONLY the number if customer proposes a specific final amount
            - "intent": set to "agreement" if they're ready to finalize
            
            Look carefully for price amounts in the message (like 105000, 105k, etc.) when finalization words are used.
            """
            
            response = self.genai_service.model.generate_content(intent_prompt)
            
            # Parse JSON response
            import json
            try:
                raw_response = response.text.strip()
                
                # Remove markdown code blocks if present
                if raw_response.startswith('```json'):
                    raw_response = raw_response.replace('```json\n', '').replace('```', '').strip()
                elif raw_response.startswith('```'):
                    # Handle other code block formats
                    lines = raw_response.split('\n')
                    raw_response = '\n'.join(lines[1:-1])
                
                result = json.loads(raw_response)
                return result
            except Exception as e:
                logger.error(f"JSON parsing error: {str(e)}, Raw response: {response.text[:200]}")
                # Fallback if JSON parsing fails
                return {'intent': 'general', 'is_ready_to_finalize': False, 'wants_final_price': False, 'proposed_final_price': None}
                
        except Exception as e:
            logger.error(f"Error analyzing intent with AI: {str(e)}")
            return {'intent': 'general', 'is_ready_to_finalize': False, 'wants_final_price': False, 'proposed_final_price': None}
    
    def analyze_customer_negotiation_style(self, negotiation_history: List[Dict]) -> str:
        """Analyze customer's negotiation style from conversation history"""
        if not negotiation_history:
            return 'unknown'
        
        customer_messages = [msg for msg in negotiation_history if msg.get('sender') == 'buyer']
        
        # Aggressive negotiator - makes big price jumps, direct language
        aggressive_keywords = ['final', 'best price', 'lowest', 'rock bottom', 'take it or leave it']
        if any(any(keyword in msg.get('message', '').lower() for keyword in aggressive_keywords) 
               for msg in customer_messages[-2:]):  # Check recent messages
            return 'aggressive'
        
        # Patient negotiator - asks questions, mentions features, longer messages
        patient_indicators = ['why', 'because', 'what about', 'tell me', 'explain', 'condition', 'maintenance']
        if len(customer_messages) > 3 and any(any(indicator in msg.get('message', '').lower() for indicator in patient_indicators) 
                                             for msg in customer_messages):
            return 'patient'
        
        # Polite negotiator - uses courteous language
        polite_keywords = ['please', 'thank you', 'appreciate', 'understand', 'respect']
        if any(any(keyword in msg.get('message', '').lower() for keyword in polite_keywords) 
               for msg in customer_messages):
            return 'polite'
        
        return 'standard'

    def calculate_counter_offer(self, asking_price: float, minimum_price: float, 
                              negotiation_round: int, user_offer: Optional[float] = None,
                              customer_style: str = 'standard') -> float:
        """Calculate counter offer based on negotiation round, user offer, and customer style"""
        
        # If user made a specific offer
        if user_offer:
            # If user offer is above minimum, try to meet halfway
            if user_offer >= minimum_price:
                # Calculate midpoint between user offer and current asking price
                midpoint = (asking_price + user_offer) / 2
                return max(midpoint, minimum_price)
            else:
                # User offer is below minimum, counter with minimum + small buffer
                buffer = 1.10 if customer_style == 'aggressive' else 1.05  # Bigger buffer for aggressive customers
                return minimum_price * buffer
        
        # Adjust negotiation steps based on customer style
        steps = self.base_negotiation_steps.copy()
        
        if customer_style == 'patient':
            # Add more steps for patient customers - they enjoy the process
            steps.extend([0.70, 0.65, 0.60])  # Add 3 more negotiation rounds
        elif customer_style == 'aggressive':
            # Move faster for aggressive customers
            steps = [0.90, 0.80, 0.75]  # Fewer, bigger steps
        elif customer_style == 'polite':
            # Reward politeness with slightly better offers
            steps = [0.93, 0.87, 0.82, 0.77, 0.73]
        
        # Standard negotiation progression
        if negotiation_round < len(steps):
            reduction_factor = steps[negotiation_round]
            counter_offer = asking_price * reduction_factor
            return max(counter_offer, minimum_price)
        else:
            # Final offer - return minimum price
            return minimum_price
    
    def generate_response(self, vehicle_sale: Dict, message: str, 
                         negotiation_history: List[Dict], negotiation_round: int) -> Tuple[str, float, bool]:
        """Generate bot response to user message using AI or fallback"""
        
        asking_price = vehicle_sale['selling_price']
        minimum_price = vehicle_sale['minimum_price']
        features = vehicle_sale.get('features', [])
        
        # Use AI to analyze intent and conversation status
        intent_analysis = self.analyze_message_intent(message, negotiation_history)
        intent = intent_analysis.get('intent', 'general')
        user_offer = self.extract_price_from_message(message)
        customer_style = self.analyze_customer_negotiation_style(negotiation_history)
        
        # Check if AI thinks we should finalize
        should_finalize = intent_analysis.get('is_ready_to_finalize', False)
        wants_final_price = intent_analysis.get('wants_final_price', False)
        should_move_to_final = intent_analysis.get('should_move_to_final', False)
        proposed_final_price = intent_analysis.get('proposed_final_price', None)
        
        # AI-driven finalization decision
        max_rounds = 8 if customer_style == 'patient' else 5 if customer_style == 'polite' else 3 if customer_style == 'aggressive' else 5
        is_final = should_move_to_final or wants_final_price or negotiation_round >= max_rounds
        
        # Handle customer proposing final price
        if should_finalize and proposed_final_price:
            if proposed_final_price >= minimum_price:
                # Customer proposed acceptable final price - accept it
                current_offer = proposed_final_price
                intent = 'agreement'  # Change intent to agreement
                is_final = True
                logger.info(f"🎯 Customer proposed acceptable final price: Rs. {proposed_final_price:,.0f}")
                
                # Generate acceptance response and return immediately
                if self.use_ai:
                    acceptance_prompt = f"""
You are Kamal, a car seller in Sri Lanka. The customer just proposed to finalize the deal at Rs. {proposed_final_price:,.0f}.

**Your Car:** {vehicle_sale.get('vehicle', {}).get('year', '')} {vehicle_sale.get('vehicle', {}).get('make', '')} {vehicle_sale.get('vehicle', {}).get('model', '')}
**Customer said:** "{message}"
**Their proposed final price:** Rs. {proposed_final_price:,.0f}
**Your minimum:** Rs. {minimum_price:,.0f}

Since their offer of Rs. {proposed_final_price:,.0f} is acceptable (above your minimum of Rs. {minimum_price:,.0f}), ACCEPT the deal and ask for their contact details.

Respond with something like: "Great! Let's make a deal at Rs. {proposed_final_price:,.0f}. I need your name and phone number to finalize."

Keep it short, friendly, and natural.
                    """
                    
                    try:
                        acceptance_response = self.genai_service.model.generate_content(acceptance_prompt)
                        return acceptance_response.text.strip(), current_offer, True
                    except:
                        pass
                        
                # Fallback acceptance response
                return f"Great! Let's make a deal at Rs. {proposed_final_price:,.0f}. I need your name and phone number to finalize.", current_offer, True
                
            else:
                # Customer proposed price below minimum - counter with minimum
                current_offer = minimum_price
                is_final = True
                logger.info(f"🎯 Customer proposed price too low ({proposed_final_price:,.0f}), countering with minimum: Rs. {minimum_price:,.0f}")
        
        # Calculate current offer based on negotiation logic
        elif intent == 'price_inquiry':
            if negotiation_round == 0:
                current_offer = asking_price
            else:
                current_offer = self.calculate_counter_offer(asking_price, minimum_price, negotiation_round, customer_style=customer_style)
        elif intent == 'price_reduction':
            current_offer = self.calculate_counter_offer(asking_price, minimum_price, negotiation_round, user_offer, customer_style)
            # Check if we should move to final price - depends on customer style
            final_threshold = 2 if customer_style == 'aggressive' else 4 if customer_style == 'patient' else 3
            if negotiation_round >= final_threshold or current_offer <= minimum_price * 1.01:
                is_final = True
                current_offer = minimum_price  # Set exactly to minimum price for final offer
        elif intent == 'agreement':
            # If we don't have current_offer set already, find the last system offer from history
            if not current_offer:
                current_offer = asking_price
                if negotiation_history:
                    for msg in reversed(negotiation_history):
                        if msg.get('sender') == 'system' and 'Rs.' in msg.get('message', ''):
                            price_match = re.search(r'Rs\.\s*([\d,]+)', msg['message'])
                            if price_match:
                                current_offer = float(price_match.group(1).replace(',', ''))
                                break
            
            # For agreement, generate response and return immediately
            if self.use_ai:
                ai_response = self.generate_ai_response(vehicle_sale, message, intent, current_offer, negotiation_round, is_final, user_offer, customer_style)
                if ai_response:
                    return ai_response, current_offer, True
            
            # Fallback for agreement
            response = f"Great! Let's make a deal at Rs. {current_offer:,.0f}. I need your name and phone number to finalize."
            return response, current_offer, True
            
        elif intent == 'rejection':
            if not is_final:
                current_offer = self.calculate_counter_offer(asking_price, minimum_price, negotiation_round + 1, customer_style=customer_style)
            else:
                current_offer = minimum_price
                is_final = True
        else:
            # General response
            current_offer = asking_price if negotiation_round == 0 else self.calculate_counter_offer(asking_price, minimum_price, negotiation_round, customer_style=customer_style)
        
        # Try to generate AI-powered response
        if self.use_ai:
            ai_response = self.generate_ai_response(vehicle_sale, message, intent, current_offer, negotiation_round, is_final, user_offer, customer_style)
            if ai_response:
                logger.info(f"✅ Using AI-generated response for {customer_style} customer, intent: {intent}")
                
                # Check if AI response is asking for contact details (finalization)
                contact_keywords = ['name', 'phone', 'contact', 'details', 'number', 'email']
                is_requesting_contact = any(keyword in ai_response.lower() for keyword in contact_keywords)
                
                if is_requesting_contact:
                    is_final = True  # Mark as final when requesting contact details
                    logger.info("🎯 AI triggered finalization - requesting contact details")
                
                return ai_response, current_offer, is_final
            else:
                logger.warning(f"⚠️ AI response failed, using fallback for intent: {intent}")
        
        # Fallback to original logic if AI fails
        logger.info(f"ℹ️ Using fallback response for intent: {intent}")
        return self._generate_fallback_response(vehicle_sale, message, intent, current_offer, negotiation_round, is_final, user_offer)
    
    def _generate_fallback_response(self, vehicle_sale: Dict, message: str, intent: str, 
                                  current_offer: float, negotiation_round: int, is_final: bool, 
                                  user_offer: Optional[float] = None) -> Tuple[str, float, bool]:
        """Generate fallback response when AI is not available"""
        
        asking_price = vehicle_sale['selling_price']
        minimum_price = vehicle_sale['minimum_price']
        features = vehicle_sale.get('features', [])
        
        response_parts = []
        
        # Add a positive opening
        if negotiation_round == 0 or intent == 'price_inquiry':
            response_parts.append(random.choice(self.positive_responses))
        
        if intent == 'price_inquiry':
            # User asking for price
            if negotiation_round == 0:
                response_parts.append(f"The asking price for this vehicle is Rs. {asking_price:,.0f}.")
                if features:
                    response_parts.append(f"This price includes valuable features like: {', '.join(features[:3])}.")
            else:
                response_parts.append(f"I can offer it for Rs. {current_offer:,.0f}.")
        
        elif intent == 'price_reduction':
            # User asking for price reduction
            if user_offer and user_offer < minimum_price * 0.8:
                # User offer is too low
                response_parts.append(f"I understand you're looking for a good deal, but Rs. {user_offer:,.0f} is quite low.")
                if features:
                    feature_text = ', '.join(features[:2])
                    response_parts.append(f"Considering that I've added {feature_text}, the value is much higher.")
                response_parts.append(f"I can come down to Rs. {current_offer:,.0f}.")
            else:
                # Reasonable negotiation
                response_parts.append(f"I can offer you Rs. {current_offer:,.0f}.")
                if features and negotiation_round > 1:
                    response_parts.append(random.choice(self.feature_highlights))
            
            # Check if we're at minimum price
            if current_offer <= minimum_price * 1.01:  # Within 1% of minimum
                is_final = True
                response_parts.append(f"This is my final price of Rs. {minimum_price:,.0f}.")
                response_parts.append(random.choice(self.closing_phrases))
        
        elif intent == 'rejection':
            # User rejected the offer
            if not is_final:
                response_parts.append("I understand. Let me make you a better offer.")
                response_parts.append(f"How about Rs. {current_offer:,.0f}?")
                if features:
                    response_parts.append(f"This includes all the improvements: {', '.join(features)}.")
            else:
                # Final rejection
                response_parts.append("I understand this might not be the right fit for you.")
                response_parts.append(f"This is my final price of Rs. {minimum_price:,.0f}.")
                response_parts.append("If you change your mind, feel free to get back to me!")
        
        else:
            # General response
            response_parts.append(f"The current offer is Rs. {current_offer:,.0f}.")
            if features:
                response_parts.append(f"This vehicle comes with: {', '.join(features)}.")
        
        # Add final negotiation prompt
        if not is_final and intent != 'agreement':
            response_parts.append("What do you think about this price?")
        
        response = ' '.join(response_parts)
        return response, current_offer, is_final
    
    def parse_contact_details(self, message: str) -> Optional[Dict[str, str]]:
        """Parse contact details from user message using AI and patterns"""
        
        # First try AI extraction if available
        if self.use_ai and self.genai_service:
            try:
                ai_prompt = f"""
                Extract contact information from this message. Return ONLY valid JSON:

                Message: "{message}"

                Return this exact format (use null for missing info):
                {{
                    "name": "extracted name or null",
                    "email": "extracted email or null", 
                    "phone": "extracted phone number or null",
                    "has_contact_info": true/false
                }}

                Only set has_contact_info to true if you find at least name AND (phone OR email).
                """
                
                response = self.genai_service.model.generate_content(ai_prompt)
                
                import json
                try:
                    result = json.loads(response.text.strip())
                    if result.get('has_contact_info', False):
                        return {
                            'name': result.get('name') or 'Customer',
                            'email': result.get('email') or '',
                            'phone': result.get('phone') or ''
                        }
                except:
                    pass
            except Exception as e:
                logger.warning(f"AI contact parsing failed: {str(e)}")
        
        # Fallback to pattern matching
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'(?:\+94|0)?(?:7[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]|6[0-9]|8[0-9]|9[0-9])[0-9]{7}'
        
        email_match = re.search(email_pattern, message)
        phone_match = re.search(phone_pattern, message.replace(' ', '').replace('-', ''))
        
        # Try to extract name (anything before email or phone)
        name = None
        words = message.split()
        potential_name_words = []
        
        for word in words:
            if '@' in word or word.isdigit() or len(word) < 2:
                break
            potential_name_words.append(word)
        
        if potential_name_words:
            name = ' '.join(potential_name_words[:3])  # Limit to 3 words
        
        if email_match or phone_match or (name and len(name.split()) >= 2):
            return {
                'name': name or 'Customer',
                'email': email_match.group() if email_match else '',
                'phone': phone_match.group() if phone_match else ''
            }
        
        return None