# NLyzer AI Agent Architecture - The Intelligent Core

> 🧠 **Comprehensive Blueprint for AI Agent Logic, Decision-Making, and Collaboration**

## Overview

This document defines the internal "minds" of the NLyzer AI agents - their decision-making processes, logic flows, and collaboration patterns. Each agent is designed as a specialist with distinct capabilities, working together under a central coordination system to deliver intelligent, personalized shopping experiences.

---

## 🏪 Core Philosophy: A Team of Specialists

### **Conceptual Model**
Think of the NLyzer chatbox not as a single AI, but as a **"store with a team of specialist employees"**:

- **Store Manager (ConversationManager)**: Greets customers, understands their needs, and directs them to the right specialist
- **Personal Shopper (VisualDiscoveryAgent)**: Expert at understanding visual preferences and finding similar products
- **Travel Consultant (DestinationCommerceAgent)**: Specializes in trip planning and destination-appropriate shopping
- **Style Advisor (StylePsychologyAgent)**: Focuses on confidence, personal style, and emotional shopping needs
- **Inventory Planner (PredictiveCommerceAgent)**: Anticipates future needs and proactively suggests items

### **Core Architectural Principles**

1. **Specialization Over Generalization**: Each agent has a narrow, deep expertise rather than broad capabilities
2. **Shared Memory**: All agents access the same conversation history and customer context stored in Redis
3. **Seamless Handoffs**: Agents can work together, with the ConversationManager orchestrating transitions
4. **Context Preservation**: Customer context, preferences, and conversation state persist across agent switches
5. **Graceful Degradation**: If a premium agent isn't available, the system falls back to core functionality

---

## 🧠 ConversationManager - The Central Brain

The ConversationManager is the orchestration layer that routes customers to the right specialist and maintains conversation coherence.

### **Core Responsibilities**
- Intent recognition and agent routing
- Conversation state management
- Agent coordination and handoffs
- Response formatting and delivery
- Multi-turn conversation handling

### **Detailed Workflow**

| Step | Actor | Action | Data In | Data Out | Technology | Documentation Reference |
|------|-------|--------|---------|----------|------------|-------------------------|
| 1 | NLyzer API | Receive new user message | user_id, store_id, text, image | - | FastAPI | 02_Core_Technologies/FastAPI/ |
| 2 | ConversationManager | Retrieve or create conversation state | user_id, store_id | ConversationState | Redis | 06_Data_Storage/Redis/ |
| 3 | ConversationManager | Perform intent recognition | text, image, conversation_history | SelectedAgent | NLU Model + Heuristics | 07_Core_Product/NLWeb/ |
| 4 | ConversationManager | Instantiate chosen agent | store_id, ConversationState | Agent instance | Python class instantiation | README.md - Agents |
| 5 | SelectedAgent | Execute core logic | text, image, ConversationState | AgentResponse | Agent-specific workflow | See agent sections below |
| 6 | ConversationManager | Receive agent response | AgentResponse | - | - | - |
| 7 | ConversationManager | Update conversation state | AgentResponse, conversation_history | Updated ConversationState | Redis SET | 06_Data_Storage/Redis/ |
| 8 | NLyzer API | Send formatted response | AgentResponse | JSON to frontend | FastAPI | 02_Core_Technologies/FastAPI/ |

### **Scoring-Based Intent Recognition System**

> **Strategic Refinement**: Evolved from rigid priority queue to intelligent scoring system enabling multi-agent collaboration.

```python
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class AgentBid:
    agent_name: str
    score: float
    reasoning: str
    confidence: float

class ConversationManager:
    def __init__(self):
        self.agent_registry = {
            "visual_discovery": VisualDiscoveryAgent,
            "destination_commerce": DestinationCommerceAgent, 
            "style_psychology": StylePsychologyAgent,
            "predictive_commerce": PredictiveCommerceAgent
        }
    
    async def recognize_intent(self, text: str, image: bytes, 
                             context: WorkingContext) -> Tuple[str, List[str]]:
        """
        Multi-agent scoring system that enables sophisticated intent recognition
        and collaboration. Returns primary agent + potential collaborators.
        """
        
        # Collect bids from all available agents
        agent_bids = []
        
        for agent_name, agent_class in self.agent_registry.items():
            if self.tier_has_access(agent_name, context.store_tier):
                bid = await self.get_agent_bid(agent_name, text, image, context)
                agent_bids.append(bid)
        
        # Sort by score (highest first)
        agent_bids.sort(key=lambda x: x.score, reverse=True)
        
        # Primary agent: highest score
        primary_agent = agent_bids[0].agent_name
        
        # Collaborators: agents with score > 5.0 and within 3 points of winner
        collaborators = [
            bid.agent_name for bid in agent_bids[1:] 
            if bid.score > 5.0 and (agent_bids[0].score - bid.score) <= 3.0
        ]
        
        # Log the decision for debugging and learning
        await self.log_intent_decision({
            "text": text,
            "has_image": bool(image),
            "bids": [(b.agent_name, b.score, b.reasoning) for b in agent_bids],
            "primary_agent": primary_agent,
            "collaborators": collaborators
        })
        
        return primary_agent, collaborators
    
    async def get_agent_bid(self, agent_name: str, text: str, image: bytes, 
                           context: WorkingContext) -> AgentBid:
        """Get each agent's bid for handling the current request"""
        
        if agent_name == "visual_discovery":
            return await self.visual_discovery_bid(text, image, context)
        elif agent_name == "destination_commerce":
            return await self.destination_commerce_bid(text, image, context)
        elif agent_name == "style_psychology":
            return await self.style_psychology_bid(text, image, context)
        elif agent_name == "predictive_commerce":
            return await self.predictive_commerce_bid(text, image, context)
    
    async def visual_discovery_bid(self, text: str, image: bytes, 
                                  context: WorkingContext) -> AgentBid:
        """Visual Discovery Agent bidding logic"""
        score = 0.0
        reasoning_parts = []
        
        # Strong signal: Image uploaded
        if image:
            score += 10.0
            reasoning_parts.append("image uploaded")
            
            # Boost if minimal text (pure visual search)
            if not text or len(text.split()) < 5:
                score += 3.0
                reasoning_parts.append("minimal text suggests visual focus")
        
        # Text analysis
        if text:
            visual_keywords = ["find this", "similar to", "looks like", "this style", "match"]
            keyword_matches = sum(1 for kw in visual_keywords if kw in text.lower())
            score += keyword_matches * 2.0
            if keyword_matches > 0:
                reasoning_parts.append(f"{keyword_matches} visual search keywords")
            
            # Context continuation boost
            if context.last_agent == "visual_discovery" and context.awaiting_refinement:
                score += 5.0
                reasoning_parts.append("continuing visual search refinement")
        
        # Base availability boost (always available)
        score += 1.0
        reasoning_parts.append("base availability")
        
        return AgentBid(
            agent_name="visual_discovery",
            score=score,
            reasoning=" + ".join(reasoning_parts),
            confidence=min(score / 12.0, 1.0)  # Normalize to 0-1
        )
    
    async def destination_commerce_bid(self, text: str, image: bytes, 
                                     context: WorkingContext) -> AgentBid:
        """Destination Commerce Agent bidding logic"""
        score = 0.0
        reasoning_parts = []
        
        if not text:
            return AgentBid("destination_commerce", 0.0, "no text input", 0.0)
        
        # Travel keywords (strong signals)
        travel_keywords = ["trip", "travel", "vacation", "pack", "destination", "weather"]
        travel_matches = sum(1 for kw in travel_keywords if kw in text.lower())
        score += travel_matches * 4.0
        if travel_matches > 0:
            reasoning_parts.append(f"{travel_matches} travel keywords")
        
        # Destination name detection (NER would be ideal)
        potential_destinations = await self.detect_destinations(text)
        if potential_destinations:
            score += 5.0
            reasoning_parts.append(f"destination detected: {potential_destinations[0]}")
        
        # Weather/climate keywords
        weather_keywords = ["hot", "cold", "rain", "sunny", "climate", "temperature"]
        weather_matches = sum(1 for kw in weather_keywords if kw in text.lower())
        score += weather_matches * 2.0
        if weather_matches > 0:
            reasoning_parts.append(f"{weather_matches} weather keywords")
        
        # Context boost for travel conversation
        if context.travel_context and context.travel_context.destination:
            score += 3.0
            reasoning_parts.append("existing travel context")
        
        return AgentBid(
            agent_name="destination_commerce",
            score=score,
            reasoning=" + ".join(reasoning_parts) if reasoning_parts else "no travel signals",
            confidence=min(score / 15.0, 1.0)
        )
    
    async def style_psychology_bid(self, text: str, image: bytes, 
                                  context: WorkingContext) -> AgentBid:
        """Style Psychology Agent bidding logic"""
        score = 0.0
        reasoning_parts = []
        
        if not text:
            return AgentBid("style_psychology", 0.0, "no text input", 0.0)
        
        # Emotional/confidence keywords (primary triggers)
        emotion_keywords = ["confidence", "feel", "powerful", "professional", "comfortable"]
        emotion_matches = sum(1 for kw in emotion_keywords if kw in text.lower())
        score += emotion_matches * 4.0
        if emotion_matches > 0:
            reasoning_parts.append(f"{emotion_matches} emotion keywords")
        
        # Style-related keywords
        style_keywords = ["style", "look good", "outfit", "aesthetic", "vibe"]
        style_matches = sum(1 for kw in style_keywords if kw in text.lower())
        score += style_matches * 2.0
        if style_matches > 0:
            reasoning_parts.append(f"{style_matches} style keywords")
        
        # Occasion-specific requests
        occasion_keywords = ["work", "meeting", "date", "party", "interview", "wedding"]
        occasion_matches = sum(1 for kw in occasion_keywords if kw in text.lower())
        score += occasion_matches * 3.0
        if occasion_matches > 0:
            reasoning_parts.append(f"{occasion_matches} occasion keywords")
        
        # Follow-up question boost
        if context.last_agent in ["visual_discovery", "destination_commerce"]:
            if any(phrase in text.lower() for phrase in ["which", "what would", "how do"]):
                score += 4.0
                reasoning_parts.append("follow-up styling question")
        
        # Rich user profile boost
        if context.user_style_profile and context.user_style_profile.confidence_score > 0.7:
            score += 2.0
            reasoning_parts.append("rich style profile available")
        
        return AgentBid(
            agent_name="style_psychology",
            score=score,
            reasoning=" + ".join(reasoning_parts) if reasoning_parts else "no style signals",
            confidence=min(score / 16.0, 1.0)
        )
    
    async def predictive_commerce_bid(self, text: str, image: bytes, 
                                    context: WorkingContext) -> AgentBid:
        """Predictive Commerce Agent bidding logic (usually background-triggered)"""
        score = 0.0
        reasoning_parts = []
        
        # This agent is primarily proactive, but can be reactive in specific cases
        
        # Check for cached predictions
        cached_predictions = await self.get_cached_predictions(context.user_id)
        if cached_predictions and cached_predictions.confidence > 0.85:
            score += 6.0
            reasoning_parts.append("high-confidence prediction available")
        
        # Future-oriented language
        future_keywords = ["need soon", "upcoming", "next month", "planning ahead"]
        future_matches = sum(1 for kw in future_keywords if kw in text.lower())
        score += future_matches * 3.0
        if future_matches > 0:
            reasoning_parts.append(f"{future_matches} future-oriented keywords")
        
        # Seasonal triggers (if appropriate timing)
        if await self.is_seasonal_transition_period():
            score += 2.0
            reasoning_parts.append("seasonal transition period")
        
        return AgentBid(
            agent_name="predictive_commerce",
            score=score,
            reasoning=" + ".join(reasoning_parts) if reasoning_parts else "no predictive triggers",
            confidence=min(score / 10.0, 1.0)
        )
```

### **Formalized State Architecture**

> **Strategic Refinement**: Split into immutable SessionState (audit trail) and dynamic WorkingContext (agent handoffs).

```python
from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

class MessageType(Enum):
    USER_TEXT = "user_text"
    USER_IMAGE = "user_image"
    AGENT_RESPONSE = "agent_response"
    SYSTEM_EVENT = "system_event"

@dataclass
class SessionMessage:
    """Immutable message record for audit trail"""
    message_id: str
    session_id: str
    timestamp: datetime
    message_type: MessageType
    content: Dict[str, Any]
    agent_name: Optional[str] = None
    processing_time_ms: Optional[int] = None
    confidence_score: Optional[float] = None

class SessionState:
    """
    Immutable conversation history stored in PostgreSQL.
    Complete audit trail of every interaction.
    """
    def __init__(self, session_id: str, user_id: str, store_id: str):
        self.session_id = session_id
        self.user_id = user_id
        self.store_id = store_id
        self.created_at = datetime.now()
        self._messages: List[SessionMessage] = []
    
    def add_message(self, message: SessionMessage) -> None:
        """Add message to immutable history"""
        # Validate message belongs to this session
        if message.session_id != self.session_id:
            raise ValueError("Message session_id mismatch")
        
        self._messages.append(message)
        
        # Persist to PostgreSQL immediately
        asyncio.create_task(self._persist_message(message))
    
    @property
    def messages(self) -> List[SessionMessage]:
        """Read-only access to messages"""
        return self._messages.copy()
    
    def get_messages_by_agent(self, agent_name: str) -> List[SessionMessage]:
        """Get all messages from specific agent"""
        return [msg for msg in self._messages if msg.agent_name == agent_name]
    
    def get_messages_since(self, timestamp: datetime) -> List[SessionMessage]:
        """Get messages since specific time"""
        return [msg for msg in self._messages if msg.timestamp >= timestamp]
    
    async def _persist_message(self, message: SessionMessage):
        """Persist message to PostgreSQL"""
        # Implementation details for database storage
        pass

@dataclass
class WorkingContext:
    """
    Lightweight, dynamic context passed between agents.
    Stored in Redis for fast access and automatic expiration.
    """
    session_id: str
    user_id: str
    store_id: str
    store_tier: str  # starter, professional, enterprise
    
    # Current conversation state
    last_agent: Optional[str] = None
    awaiting_response: bool = False
    awaiting_refinement: bool = False
    conversation_intent: Optional[str] = None
    last_activity: datetime = None
    
    # Agent results (lightweight summaries)
    active_products: List[Dict[str, Any]] = None  # Current product set
    search_filters: Dict[str, Any] = None  # Active search parameters
    user_style_profile: Optional['StyleProfileSummary'] = None
    travel_context: Optional['TravelContextSummary'] = None
    
    # Quick access caches
    recent_preferences: Dict[str, Any] = None  # Last 5 interactions
    session_metadata: Dict[str, Any] = None  # Custom session data
    
    # Collaboration state
    collaborating_agents: List[str] = None
    handoff_context: Dict[str, Any] = None
    
    def update_from_agent_response(self, agent_name: str, response: 'AgentResponse'):
        """Update working context with agent results"""
        self.last_agent = agent_name
        self.last_activity = datetime.now()
        
        # Update active products if agent returned products
        if response.products:
            self.active_products = [{
                'product_id': p.product_id,
                'name': p.name,
                'price': p.price,
                'confidence': p.confidence if hasattr(p, 'confidence') else None
            } for p in response.products[:10]]  # Keep only top 10 for speed
        
        # Agent-specific updates
        if agent_name == "visual_discovery":
            self.search_filters = response.metadata.get('search_filters', {})
            
        elif agent_name == "style_psychology":
            if response.metadata.get('style_insights'):
                self.user_style_profile = StyleProfileSummary.from_insights(
                    response.metadata['style_insights']
                )
        
        elif agent_name == "destination_commerce":
            if response.metadata.get('travel_context'):
                self.travel_context = TravelContextSummary.from_full_context(
                    response.metadata['travel_context']
                )
        
        # Set awaiting state based on response
        self.awaiting_response = response.expects_user_input
        self.awaiting_refinement = response.offers_refinement
    
    def to_redis_dict(self) -> Dict[str, Any]:
        """Serialize for Redis storage"""
        return {
            'session_id': self.session_id,
            'user_id': self.user_id,
            'store_id': self.store_id,
            'store_tier': self.store_tier,
            'last_agent': self.last_agent,
            'awaiting_response': self.awaiting_response,
            'awaiting_refinement': self.awaiting_refinement,
            'conversation_intent': self.conversation_intent,
            'last_activity': self.last_activity.isoformat() if self.last_activity else None,
            'active_products': self.active_products,
            'search_filters': self.search_filters,
            'user_style_profile': self.user_style_profile.to_dict() if self.user_style_profile else None,
            'travel_context': self.travel_context.to_dict() if self.travel_context else None,
            'recent_preferences': self.recent_preferences,
            'session_metadata': self.session_metadata,
            'collaborating_agents': self.collaborating_agents,
            'handoff_context': self.handoff_context
        }
    
    @classmethod
    def from_redis_dict(cls, data: Dict[str, Any]) -> 'WorkingContext':
        """Deserialize from Redis"""
        context = cls(
            session_id=data['session_id'],
            user_id=data['user_id'],
            store_id=data['store_id'],
            store_tier=data['store_tier']
        )
        
        context.last_agent = data.get('last_agent')
        context.awaiting_response = data.get('awaiting_response', False)
        context.awaiting_refinement = data.get('awaiting_refinement', False)
        context.conversation_intent = data.get('conversation_intent')
        
        if data.get('last_activity'):
            context.last_activity = datetime.fromisoformat(data['last_activity'])
        
        context.active_products = data.get('active_products')
        context.search_filters = data.get('search_filters')
        
        if data.get('user_style_profile'):
            context.user_style_profile = StyleProfileSummary.from_dict(data['user_style_profile'])
        
        if data.get('travel_context'):
            context.travel_context = TravelContextSummary.from_dict(data['travel_context'])
        
        context.recent_preferences = data.get('recent_preferences')
        context.session_metadata = data.get('session_metadata')
        context.collaborating_agents = data.get('collaborating_agents')
        context.handoff_context = data.get('handoff_context')
        
        return context

@dataclass
class StyleProfileSummary:
    """Lightweight style profile for WorkingContext"""
    dominant_colors: List[str]
    preferred_styles: List[str]
    confidence_score: float
    last_updated: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'dominant_colors': self.dominant_colors,
            'preferred_styles': self.preferred_styles,
            'confidence_score': self.confidence_score,
            'last_updated': self.last_updated.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StyleProfileSummary':
        return cls(
            dominant_colors=data['dominant_colors'],
            preferred_styles=data['preferred_styles'],
            confidence_score=data['confidence_score'],
            last_updated=datetime.fromisoformat(data['last_updated'])
        )
    
    @classmethod
    def from_insights(cls, insights: Dict[str, Any]) -> 'StyleProfileSummary':
        return cls(
            dominant_colors=insights.get('colors', [])[:3],  # Top 3 colors
            preferred_styles=insights.get('styles', [])[:3],  # Top 3 styles
            confidence_score=insights.get('confidence', 0.0),
            last_updated=datetime.now()
        )

@dataclass
class TravelContextSummary:
    """Lightweight travel context for WorkingContext"""
    destination: str
    travel_dates: Optional[str]
    weather_summary: Optional[str]
    activities: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'destination': self.destination,
            'travel_dates': self.travel_dates,
            'weather_summary': self.weather_summary,
            'activities': self.activities
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TravelContextSummary':
        return cls(
            destination=data['destination'],
            travel_dates=data.get('travel_dates'),
            weather_summary=data.get('weather_summary'),
            activities=data.get('activities', [])
        )
    
    @classmethod
    def from_full_context(cls, full_context: Dict[str, Any]) -> 'TravelContextSummary':
        return cls(
            destination=full_context.get('destination', ''),
            travel_dates=full_context.get('travel_dates_str'),
            weather_summary=full_context.get('weather_summary'),
            activities=full_context.get('activities', [])[:5]  # Top 5 activities
        )
```

---

## 🔍 Visual Discovery Agent - The Personal Shopper

### **Agent Profile**
- **Core Purpose**: "I saw this, do you have something like it?"
- **Pricing Tier**: Starter (Core functionality)
- **Personality**: Precise, visual-focused, efficient
- **Specialty**: Understanding visual aesthetics and finding similar products

### **Activation Triggers**
- User uploads an image with no accompanying text
- Text contains phrases like "find this look," "search by image," "similar to this"
- User asks to refine visual search results
- Default agent when no other intent is detected

### **Detailed Agent Workflow**

| Step | Actor | Action | Data In | Data Out | Technology | Documentation Reference |
|------|-------|--------|---------|----------|------------|-------------------------|
| 1 | VisualDiscoveryAgent | Receive activation from ConversationManager | image_bytes, text, store_id | - | - | - |
| 2 | VisualDiscoveryAgent | Call Multimodal Engine for image analysis | image_bytes | StyleDNA {colors, patterns, style, occasion} | OpenAI Vision API | 05_External_Services/AI_Libraries/OpenAI/ |
| 3 | VisualDiscoveryAgent | Generate vector embedding | image_bytes | Vector[1536] | OpenAI Embedding API | 05_External_Services/AI_Libraries/OpenAI/ |
| 4 | VisualDiscoveryAgent | Perform similarity search | Vector, store_id filter | List[ProductMatch] with scores | Qdrant/Pinecone | 07_Core_Product/NLWeb/ |
| 5 | VisualDiscoveryAgent | Fetch product details | product_ids[] | List[Product] with metadata | PostgreSQL | 02_Core_Technologies/SQLAlchemy/ |
| 6 | VisualDiscoveryAgent | Apply intelligent ranking | Products, StyleDNA, user_context | RankedResults | Custom ranking algorithm | - |
| 7 | VisualDiscoveryAgent | Format response with confidence | RankedResults | AgentResponse | Pydantic models | 02_Core_Technologies/Pydantic/ |

### **Weighted Ranking Formula System**

> **Strategic Refinement**: Configurable weighted formula enabling A/B testing and easy tuning without code changes.

```python
from typing import Dict, List, Any
from dataclasses import dataclass
import json

@dataclass
class RankingWeights:
    """Configurable weights for ranking algorithm"""
    base_similarity: float = 0.40  # 40% weight on base similarity
    color_harmony: float = 0.20    # 20% weight on color matching
    style_consistency: float = 0.15 # 15% weight on style matching
    occasion_match: float = 0.10    # 10% weight on occasion
    price_preference: float = 0.08  # 8% weight on price preference
    availability: float = 0.05      # 5% weight on stock status
    brand_affinity: float = 0.02    # 2% weight on brand preference
    
    def __post_init__(self):
        """Validate weights sum to 1.0"""
        total = sum([
            self.base_similarity, self.color_harmony, self.style_consistency,
            self.occasion_match, self.price_preference, self.availability, self.brand_affinity
        ])
        if abs(total - 1.0) > 0.001:
            raise ValueError(f"Weights must sum to 1.0, got {total}")
    
    @classmethod
    def from_config(cls, config_name: str = "default") -> 'RankingWeights':
        """Load weights from configuration file"""
        config_path = f"config/ranking_weights_{config_name}.json"
        try:
            with open(config_path, 'r') as f:
                config_data = json.load(f)
            return cls(**config_data)
        except FileNotFoundError:
            # Return default weights if config not found
            return cls()

class VisualDiscoveryAgent:
    def __init__(self, store_id: str, context: WorkingContext):
        super().__init__(store_id, context)
        
        # Load ranking weights (supports A/B testing)
        self.ranking_weights = self.get_ranking_weights_for_user(context.user_id)
    
    def get_ranking_weights_for_user(self, user_id: str) -> RankingWeights:
        """Get user-specific weights (enables A/B testing)"""
        
        # Check if user is in A/B test
        experiment_variant = self.get_experiment_variant(user_id, "ranking_algorithm_v2")
        
        if experiment_variant == "control":
            return RankingWeights.from_config("default")
        elif experiment_variant == "style_focused":
            return RankingWeights.from_config("style_focused")
        elif experiment_variant == "price_sensitive":
            return RankingWeights.from_config("price_sensitive")
        else:
            return RankingWeights.from_config("default")
    
    def apply_intelligent_ranking(self, products: List[Product], style_dna: StyleDNA, 
                                 context: WorkingContext) -> List[RankedProduct]:
        """
        Sophisticated weighted ranking with configurable parameters
        """
        ranked_products = []
        
        for product in products:
            # Calculate individual component scores (0-1 range)
            base_score = product.similarity_score  # Already normalized 0-1
            color_score = self.calculate_color_harmony(style_dna.colors, product.colors)
            style_score = self.calculate_style_match(style_dna.style, product.style_tags)
            occasion_score = self.calculate_occasion_match(style_dna.occasion, product.occasions)
            price_score = self.calculate_price_preference(product.price, context)
            availability_score = 1.0 if product.in_stock else 0.0
            brand_score = self.calculate_brand_affinity(product.brand, context)
            
            # Apply weighted formula
            final_score = (
                (self.ranking_weights.base_similarity * base_score) +
                (self.ranking_weights.color_harmony * color_score) +
                (self.ranking_weights.style_consistency * style_score) +
                (self.ranking_weights.occasion_match * occasion_score) +
                (self.ranking_weights.price_preference * price_score) +
                (self.ranking_weights.availability * availability_score) +
                (self.ranking_weights.brand_affinity * brand_score)
            )
            
            # Generate detailed scoring breakdown
            score_breakdown = {
                'base_similarity': (base_score, self.ranking_weights.base_similarity),
                'color_harmony': (color_score, self.ranking_weights.color_harmony),
                'style_consistency': (style_score, self.ranking_weights.style_consistency),
                'occasion_match': (occasion_score, self.ranking_weights.occasion_match),
                'price_preference': (price_score, self.ranking_weights.price_preference),
                'availability': (availability_score, self.ranking_weights.availability),
                'brand_affinity': (brand_score, self.ranking_weights.brand_affinity)
            }
            
            ranked_products.append(RankedProduct(
                product=product,
                final_score=final_score,
                reasoning=self.generate_match_reasoning(style_dna, product, score_breakdown),
                score_breakdown=score_breakdown
            ))
        
        return sorted(ranked_products, key=lambda x: x.final_score, reverse=True)
    
    def generate_match_reasoning(self, style_dna: StyleDNA, product: Product) -> str:
        """Generate human-readable explanation for why this product matches"""
        reasons = []
        
        if style_dna.colors and any(color in product.colors for color in style_dna.colors):
            matching_colors = [c for c in style_dna.colors if c in product.colors]
            reasons.append(f"matches your {', '.join(matching_colors)} color preference")
        
        if style_dna.style and style_dna.style in product.style_tags:
            reasons.append(f"fits the {style_dna.style} aesthetic")
        
        if style_dna.occasion and style_dna.occasion in product.occasions:
            reasons.append(f"perfect for {style_dna.occasion} occasions")
        
        return f"Great match because it {' and '.join(reasons)}."
```

### **Response Formatting**

```python
class VisualSearchResponse:
    products: List[RankedProduct]
    total_matches: int
    confidence_score: float
    search_insights: str
    refinement_suggestions: List[str]
    
    def format_for_user(self) -> str:
        response = f"I found {len(self.products)} great matches! Here are the top picks:\n\n"
        
        for i, ranked_product in enumerate(self.products[:5], 1):
            product = ranked_product.product
            response += f"{i}. **{product.name}** - ${product.price}\n"
            response += f"   {ranked_product.reasoning}\n"
            response += f"   Confidence: {ranked_product.final_score:.0%}\n\n"
        
        if self.refinement_suggestions:
            response += "💡 Want to refine your search? Try:\n"
            response += "\n".join(f"• {suggestion}" for suggestion in self.refinement_suggestions)
        
        return response
```

---

## ✈️ Destination Commerce Agent - The Travel Consultant

### **Agent Profile**
- **Core Purpose**: "What should I wear/bring for my trip?"
- **Pricing Tier**: Professional
- **Personality**: Knowledgeable, practical, detail-oriented
- **Specialty**: Weather-aware shopping and cultural considerations

### **Activation Triggers**
- Keywords: "trip," "travel," "vacation," "pack for," destination names
- Weather-related queries combined with shopping intent
- Follow-up questions about travel recommendations

### **Detailed Agent Workflow**

| Step | Actor | Action | Data In | Data Out | Technology | Documentation Reference |
|------|-------|--------|---------|----------|------------|-------------------------|
| 1 | DestinationCommerceAgent | Receive activation | text, ConversationState | - | - | - |
| 2 | DestinationCommerceAgent | Extract entities (destination, dates) | text | ExtractedEntities | NLP/NER | 07_Core_Product/NLWeb/ |
| 3 | DestinationCommerceAgent | Check completeness, ask clarifying questions | ExtractedEntities, context | Question or continue | Multi-turn logic | README.md - Framework |
| 4 | DestinationCommerceAgent | Fetch weather forecast | destination, dates | WeatherForecast | Weather API | nlyzer/intelligence/weather_service.py |
| 5 | DestinationCommerceAgent | Retrieve cultural context | destination | CulturalNotes | Cultural database | nlyzer/intelligence/cultural_database.py |
| 6 | DestinationCommerceAgent | Generate contextual search query | Weather, Culture, user_style | SearchQuery | Internal logic | - |
| 7 | DestinationCommerceAgent | Search product catalog | SearchQuery, store_id | ProductCandidates | PostgreSQL + Vector search | - |
| 8 | DestinationCommerceAgent | Build intelligent wardrobe | Products, travel_context | WardrobeRecommendation | Wardrobe logic | - |
| 9 | DestinationCommerceAgent | Format travel-specific response | WardrobeRecommendation | AgentResponse | Pydantic models | - |

### **Intelligence Logic - Wardrobe Building**

```python
class DestinationCommerceAgent:
    def build_intelligent_wardrobe(self, products: List[Product], 
                                  travel_context: TravelContext) -> WardrobeRecommendation:
        """
        Create a comprehensive travel wardrobe based on weather, activities, and culture
        """
        wardrobe = WardrobeRecommendation()
        weather = travel_context.weather_forecast
        activities = travel_context.planned_activities
        culture = travel_context.cultural_notes
        
        # Day-by-day outfit planning
        for day in travel_context.travel_days:
            day_weather = weather.get_day_forecast(day)
            day_activities = activities.get_day_activities(day)
            
            day_outfit = self.create_day_outfit(
                products=products,
                weather=day_weather,
                activities=day_activities,
                cultural_requirements=culture
            )
            
            wardrobe.daily_outfits[day] = day_outfit
        
        # Essential categories
        wardrobe.essentials = self.identify_essentials(travel_context)
        wardrobe.layering_pieces = self.suggest_layering(weather.temperature_range)
        wardrobe.footwear = self.recommend_footwear(activities, weather, culture)
        wardrobe.accessories = self.suggest_accessories(weather, activities)
        
        # Packing optimization
        wardrobe.mix_and_match = self.optimize_for_versatility(wardrobe.daily_outfits)
        
        return wardrobe
    
    def create_day_outfit(self, products: List[Product], weather: DayWeather, 
                         activities: List[Activity], cultural_requirements: CulturalNotes) -> DayOutfit:
        """Create weather and activity-appropriate outfit for specific day"""
        
        outfit = DayOutfit()
        
        # Base layer selection based on temperature
        if weather.temperature_high > 75:  # Hot weather
            outfit.tops = self.filter_products(products, category="tops", 
                                             attributes=["lightweight", "breathable"])
            outfit.bottoms = self.filter_products(products, category="bottoms", 
                                                 attributes=["shorts", "lightweight pants"])
        elif weather.temperature_low < 50:  # Cold weather
            outfit.layers = self.filter_products(products, category="outerwear", 
                                                attributes=["warm", "insulated"])
        
        # Activity-specific adjustments
        if "hiking" in [a.name for a in activities]:
            outfit.footwear = self.filter_products(products, category="shoes", 
                                                  attributes=["hiking", "comfortable"])
        elif "business meeting" in [a.name for a in activities]:
            outfit.dress_code = "business_casual"
            outfit = self.apply_dress_code(outfit, products, "business_casual")
        
        # Cultural considerations
        if cultural_requirements.modest_dress_required:
            outfit = self.ensure_modesty(outfit, cultural_requirements.modesty_rules)
        
        # Weather protection
        if weather.precipitation_chance > 60:
            outfit.rain_protection = self.filter_products(products, 
                                                         attributes=["waterproof", "rain_jacket"])
        
        return outfit
```

### **Multi-Turn Conversation Handling**

```python
def handle_missing_information(self, entities: ExtractedEntities, 
                               context: ConversationState) -> AgentResponse:
    """Handle incomplete travel information with intelligent follow-up questions"""
    
    if not entities.destination:
        return AgentResponse(
            text="I'd love to help you plan your travel wardrobe! Where are you headed?",
            expecting="destination",
            suggestions=["Popular destinations: Paris, Tokyo, Bali, New York"]
        )
    
    if not entities.travel_dates:
        return AgentResponse(
            text=f"Great choice - {entities.destination}! When are you planning to travel?",
            expecting="dates",
            suggestions=["This helps me check the weather forecast for your trip"]
        )
    
    if not entities.trip_duration and entities.travel_dates:
        duration = self.calculate_duration(entities.travel_dates)
        if duration > 7:  # Long trip needs more planning
            return AgentResponse(
                text="This is a nice long trip! What activities are you planning?",
                expecting="activities",
                suggestions=["Business meetings", "Sightseeing", "Beach time", "Hiking"]
            )
    
    # All essential information gathered, proceed with recommendation
    return None
```

---

## 💫 Style Psychology Agent - The Confidence Coach

### **Agent Profile**
- **Core Purpose**: "What will make me feel confident/good/professional?"
- **Pricing Tier**: Professional
- **Personality**: Empathetic, intuitive, encouraging
- **Specialty**: Emotional shopping needs and personal style development

### **Activation Triggers**
- Keywords: "confidence," "feel," "work," "professional," "make me look," "style"
- Emotional context in queries ("need to feel powerful," "boost my confidence")
- Secondary activation to refine other agents' results with style considerations

### **Cold Start Solution: Style Onboarding Quiz**

> **Strategic Refinement**: Interactive quiz system to bootstrap StyleProfile for new users, solving the cold start problem.

```python
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

class QuizQuestionType(Enum):
    VISUAL_PREFERENCE = "visual_preference"
    LIFESTYLE_INDICATOR = "lifestyle_indicator"
    CONFIDENCE_GOAL = "confidence_goal"
    OCCASION_PRIORITY = "occasion_priority"
    STYLE_ASPIRATION = "style_aspiration"

@dataclass
class QuizOption:
    option_id: str
    display_text: str
    image_url: Optional[str] = None
    style_attributes: Dict[str, float] = None  # Weighted attributes this choice represents

@dataclass
class QuizQuestion:
    question_id: str
    question_type: QuizQuestionType
    question_text: str
    subtitle: Optional[str] = None
    options: List[QuizOption] = None
    allows_multiple: bool = False
    weight: float = 1.0  # Importance weight for this question

class StyleOnboardingQuiz:
    """
    Interactive quiz system that creates a rich StyleProfile for new users
    in 60-90 seconds, enabling immediate personalized recommendations.
    """
    
    def __init__(self):
        self.questions = self._initialize_quiz_questions()
    
    def _initialize_quiz_questions(self) -> List[QuizQuestion]:
        """Initialize the core quiz questions"""
        
        return [
            # Question 1: Visual Style Preference (Most Important)
            QuizQuestion(
                question_id="visual_style_preference",
                question_type=QuizQuestionType.VISUAL_PREFERENCE,
                question_text="Which of these style vibes resonates most with you?",
                subtitle="This helps me understand your aesthetic preferences",
                weight=2.0,  # Double weight for this crucial question
                options=[
                    QuizOption(
                        option_id="minimalist",
                        display_text="Clean & Minimalist",
                        image_url="/quiz/images/minimalist_style.jpg",
                        style_attributes={
                            "minimalist": 1.0, "modern": 0.7, "classic": 0.5,
                            "colors": ["black", "white", "grey", "beige"]
                        }
                    ),
                    QuizOption(
                        option_id="bohemian",
                        display_text="Bohemian & Free-spirited",
                        image_url="/quiz/images/bohemian_style.jpg",
                        style_attributes={
                            "bohemian": 1.0, "eclectic": 0.8, "artistic": 0.6,
                            "colors": ["earth_tones", "jewel_tones"]
                        }
                    ),
                    QuizOption(
                        option_id="classic",
                        display_text="Timeless & Classic",
                        image_url="/quiz/images/classic_style.jpg",
                        style_attributes={
                            "classic": 1.0, "professional": 0.8, "elegant": 0.7,
                            "colors": ["navy", "black", "cream", "burgundy"]
                        }
                    ),
                    QuizOption(
                        option_id="edgy",
                        display_text="Edgy & Bold",
                        image_url="/quiz/images/edgy_style.jpg",
                        style_attributes={
                            "edgy": 1.0, "modern": 0.6, "bold": 1.0,
                            "colors": ["black", "leather", "metallic"]
                        }
                    )
                ]
            ),
            
            # Question 2: Confidence Goals
            QuizQuestion(
                question_id="confidence_goals",
                question_type=QuizQuestionType.CONFIDENCE_GOAL,
                question_text="What makes you feel most confident?",
                subtitle="Understanding your confidence drivers helps me recommend pieces that empower you",
                weight=1.5,
                allows_multiple=True,  # User can select multiple
                options=[
                    QuizOption(
                        option_id="structured_professional",
                        display_text="Structured, professional pieces",
                        style_attributes={
                            "confidence_boosters": ["blazers", "structured_tops"],
                            "occasions": ["work", "meetings", "professional"]
                        }
                    ),
                    QuizOption(
                        option_id="comfortable_fit",
                        display_text="Perfect fit and comfort",
                        style_attributes={
                            "fit_priorities": ["comfortable", "flattering"],
                            "body_confidence": ["comfort_focused"]
                        }
                    ),
                    QuizOption(
                        option_id="unique_statement",
                        display_text="Unique pieces that stand out",
                        style_attributes={
                            "personality_traits": ["creative", "individual"],
                            "confidence_boosters": ["statement_pieces", "unique_items"]
                        }
                    ),
                    QuizOption(
                        option_id="quality_craftsmanship",
                        display_text="High-quality, well-made items",
                        style_attributes={
                            "value_priorities": ["quality", "craftsmanship"],
                            "brand_preferences": ["premium", "artisanal"]
                        }
                    )
                ]
            ),
            
            # Question 3: Lifestyle Indicators
            QuizQuestion(
                question_id="lifestyle_context",
                question_type=QuizQuestionType.LIFESTYLE_INDICATOR,
                question_text="What best describes your current lifestyle?",
                subtitle="This helps me prioritize the right occasions for your wardrobe",
                weight=1.0,
                options=[
                    QuizOption(
                        option_id="busy_professional",
                        display_text="Busy professional with limited shopping time",
                        style_attributes={
                            "lifestyle_indicators": ["busy_professional", "efficient_shopper"],
                            "occasion_frequency": {"work": 0.7, "casual": 0.2, "special": 0.1},
                            "shopping_preferences": ["versatile", "easy_care"]
                        }
                    ),
                    QuizOption(
                        option_id="creative_flexible",
                        display_text="Creative work with flexible dress codes",
                        style_attributes={
                            "lifestyle_indicators": ["creative", "flexible"],
                            "occasion_frequency": {"creative": 0.6, "casual": 0.3, "work": 0.1},
                            "style_preferences": ["expressive", "unique"]
                        }
                    ),
                    QuizOption(
                        option_id="social_active",
                        display_text="Active social life with varied occasions",
                        style_attributes={
                            "lifestyle_indicators": ["social", "varied_occasions"],
                            "occasion_frequency": {"social": 0.4, "casual": 0.3, "dressy": 0.3},
                            "versatility_needs": ["day_to_night", "multi_occasion"]
                        }
                    ),
                    QuizOption(
                        option_id="lifestyle_transition",
                        display_text="In transition (new job, life change, etc.)",
                        style_attributes={
                            "lifestyle_indicators": ["transition", "exploring"],
                            "style_evolution": ["experimental", "building_wardrobe"],
                            "confidence_needs": ["reinvention", "fresh_start"]
                        }
                    )
                ]
            ),
            
            # Question 4: Occasion Priorities
            QuizQuestion(
                question_id="occasion_priorities",
                question_type=QuizQuestionType.OCCASION_PRIORITY,
                question_text="Which occasions do you shop for most often?",
                subtitle="Select up to 3 that matter most to you",
                weight=1.0,
                allows_multiple=True,
                options=[
                    QuizOption(option_id="work", display_text="Work & Professional"),
                    QuizOption(option_id="casual", display_text="Everyday & Casual"),
                    QuizOption(option_id="social", display_text="Social Events & Outings"),
                    QuizOption(option_id="special", display_text="Special Occasions & Celebrations"),
                    QuizOption(option_id="travel", display_text="Travel & Vacation"),
                    QuizOption(option_id="active", display_text="Active & Athleisure")
                ]
            ),
            
            # Question 5: Style Aspirations (Growth Direction)
            QuizQuestion(
                question_id="style_aspirations",
                question_type=QuizQuestionType.STYLE_ASPIRATION,
                question_text="Is there a style you admire but haven't tried yet?",
                subtitle="Optional: This helps me gently suggest new directions",
                weight=0.5,  # Lower weight, aspirational
                options=[
                    QuizOption(
                        option_id="more_feminine",
                        display_text="More feminine & romantic",
                        style_attributes={"aspiration_styles": ["feminine", "romantic", "soft"]}
                    ),
                    QuizOption(
                        option_id="more_edgy",
                        display_text="Edgier & more bold",
                        style_attributes={"aspiration_styles": ["edgy", "bold", "statement"]}
                    ),
                    QuizOption(
                        option_id="more_polished",
                        display_text="More polished & elevated",
                        style_attributes={"aspiration_styles": ["polished", "elevated", "sophisticated"]}
                    ),
                    QuizOption(
                        option_id="more_relaxed",
                        display_text="More relaxed & effortless",
                        style_attributes={"aspiration_styles": ["relaxed", "effortless", "casual_chic"]}
                    ),
                    QuizOption(
                        option_id="happy_current",
                        display_text="I'm happy with my current style!",
                        style_attributes={"aspiration_styles": []}
                    )
                ]
            )
        ]
    
    async def start_quiz_for_user(self, user_id: str, store_id: str) -> Dict[str, Any]:
        """Start quiz session for new user"""
        
        # Create quiz session
        quiz_session = {
            "session_id": f"quiz_{user_id}_{int(datetime.now().timestamp())}",
            "user_id": user_id,
            "store_id": store_id,
            "current_question": 0,
            "answers": {},
            "started_at": datetime.now(),
            "completion_percentage": 0
        }
        
        # Cache in Redis with 30-minute expiration
        await self.cache_quiz_session(quiz_session)
        
        # Return first question
        return {
            "quiz_session_id": quiz_session["session_id"],
            "question": self.questions[0].to_dict(),
            "progress": {"current": 1, "total": len(self.questions)},
            "estimated_time": "60-90 seconds"
        }
    
    async def process_quiz_answer(self, session_id: str, question_id: str, 
                                 answer_ids: List[str]) -> Dict[str, Any]:
        """Process user's answer and return next question or results"""
        
        # Retrieve quiz session
        session = await self.get_quiz_session(session_id)
        if not session:
            raise ValueError("Quiz session expired or not found")
        
        # Store answer
        session["answers"][question_id] = answer_ids
        session["current_question"] += 1
        session["completion_percentage"] = (session["current_question"] / len(self.questions)) * 100
        
        # Update cached session
        await self.cache_quiz_session(session)
        
        # Check if quiz is complete
        if session["current_question"] >= len(self.questions):
            # Generate StyleProfile from answers
            style_profile = await self.generate_style_profile_from_quiz(session)
            
            # Save to database
            await self.save_user_style_profile(session["user_id"], style_profile)
            
            # Return completion results
            return {
                "quiz_complete": True,
                "style_profile_created": True,
                "confidence_score": style_profile.confidence_score,
                "top_style_attributes": style_profile.get_top_attributes(),
                "personalized_message": self.generate_completion_message(style_profile)
            }
        else:
            # Return next question
            next_question = self.questions[session["current_question"]]
            return {
                "quiz_complete": False,
                "question": next_question.to_dict(),
                "progress": {
                    "current": session["current_question"] + 1, 
                    "total": len(self.questions)
                }
            }
    
    async def generate_style_profile_from_quiz(self, session: Dict[str, Any]) -> StyleProfile:
        """Convert quiz answers into comprehensive StyleProfile"""
        
        answers = session["answers"]
        profile = StyleProfile(user_id=session["user_id"])
        
        # Process each answer with weighted scoring
        total_weight = 0
        style_scores = {}
        
        for question in self.questions:
            if question.question_id not in answers:
                continue
                
            answer_ids = answers[question.question_id]
            question_weight = question.weight
            total_weight += question_weight
            
            # Process selected options
            for answer_id in answer_ids:
                option = next((opt for opt in question.options if opt.option_id == answer_id), None)
                if not option or not option.style_attributes:
                    continue
                
                # Aggregate style attributes with weights
                for attr_name, attr_value in option.style_attributes.items():
                    if attr_name not in style_scores:
                        style_scores[attr_name] = 0
                    
                    if isinstance(attr_value, (int, float)):
                        style_scores[attr_name] += attr_value * question_weight
                    elif isinstance(attr_value, list):
                        # Handle list attributes (colors, preferences, etc.)
                        if attr_name not in profile.__dict__:
                            setattr(profile, attr_name, [])
                        getattr(profile, attr_name).extend(attr_value)
                    elif isinstance(attr_value, dict):
                        # Handle dict attributes (occasion frequency, etc.)
                        if attr_name not in profile.__dict__:
                            setattr(profile, attr_name, {})
                        for k, v in attr_value.items():
                            getattr(profile, attr_name)[k] = v * question_weight
        
        # Normalize scores and set profile attributes
        if total_weight > 0:
            for attr_name, score in style_scores.items():
                normalized_score = score / total_weight
                setattr(profile, attr_name, normalized_score)
        
        # Calculate confidence score based on quiz completeness and consistency
        profile.confidence_score = self.calculate_quiz_confidence(answers)
        profile.quiz_generated = True
        profile.last_updated = datetime.now()
        
        return profile
    
    def calculate_quiz_confidence(self, answers: Dict[str, List[str]]) -> float:
        """Calculate confidence score based on quiz responses"""
        
        # Base confidence from completion rate
        completion_rate = len(answers) / len(self.questions)
        base_confidence = completion_rate * 0.7  # 70% max from completion
        
        # Bonus confidence from consistency and engagement
        consistency_bonus = 0
        engagement_bonus = 0
        
        # Check for multiple selections where allowed (shows engagement)
        for question in self.questions:
            if question.question_id in answers:
                answer_count = len(answers[question.question_id])
                if question.allows_multiple and answer_count > 1:
                    engagement_bonus += 0.05  # 5% bonus per multi-select
                elif not question.allows_multiple and answer_count == 1:
                    consistency_bonus += 0.05  # 5% bonus for clear choices
        
        return min(base_confidence + consistency_bonus + engagement_bonus, 1.0)
    
    def generate_completion_message(self, profile: StyleProfile) -> str:
        """Generate personalized completion message"""
        
        top_style = profile.get_dominant_style()
        confidence_level = "high" if profile.confidence_score > 0.8 else "good"
        
        messages = {
            "minimalist": f"I can see you appreciate clean, intentional style! With {confidence_level} confidence in your preferences, I'll focus on timeless pieces that make a statement through simplicity.",
            "bohemian": f"Your free-spirited style is beautiful! With {confidence_level} confidence in your preferences, I'll find pieces that let your creativity shine through.",
            "classic": f"Timeless elegance is your signature! With {confidence_level} confidence in your preferences, I'll curate sophisticated pieces that never go out of style.",
            "edgy": f"I love your bold style choices! With {confidence_level} confidence in your preferences, I'll find statement pieces that match your fearless attitude."
        }
        
        return messages.get(top_style, f"Your unique style is taking shape! With {confidence_level} confidence in your preferences, I'm ready to find pieces that truly represent you.")

# Integration with StylePsychologyAgent
class StylePsychologyAgent(BaseAgent):
    def __init__(self, store_id: str, context: WorkingContext):
        super().__init__(store_id, context)
        self.quiz_system = StyleOnboardingQuiz()
    
    async def handle_cold_start_user(self, context: WorkingContext) -> AgentResponse:
        """Handle new users with no style profile"""
        
        # Check if user has minimal interaction history
        if self.is_cold_start_user(context):
            # Offer quiz instead of trying to make recommendations
            quiz_start = await self.quiz_system.start_quiz_for_user(
                context.user_id, context.store_id
            )
            
            return AgentResponse(
                text="I'd love to get to know your style! This quick 60-second quiz will help me understand your preferences so I can give you amazing recommendations.",
                quiz_offered=True,
                quiz_data=quiz_start,
                confidence=1.0,
                agent_name="style_psychology",
                follow_up_suggestions=[
                    "Take the style quiz (60 seconds)",
                    "Browse our collections first",
                    "Tell me about a recent favorite purchase"
                ]
            )
        
        # Continue with normal agent logic for users with some data
        return await self.process_with_existing_data(context)
    
    def is_cold_start_user(self, context: WorkingContext) -> bool:
        """Determine if user needs style onboarding"""
        
        # No style profile
        if not context.user_style_profile:
            return True
        
        # Style profile exists but low confidence
        if context.user_style_profile.confidence_score < 0.3:
            return True
        
        # No recent interaction data
        if not context.recent_preferences or len(context.recent_preferences) < 2:
            return True
        
        return False
```

### **Detailed Agent Workflow**

| Step | Actor | Action | Data In | Data Out | Technology | Documentation Reference |
|------|-------|--------|---------|----------|------------|-------------------------|
| 1 | StylePsychologyAgent | Receive activation | text, ConversationState | - | - | - |
| 2 | StylePsychologyAgent | Build comprehensive style profile | user_id, conversation_history | StyleProfile | PostgreSQL + Redis | 06_Data_Storage/ |
| 3 | StylePsychologyAgent | Analyze emotional/contextual intent | text, style_profile | DesiredFeeling | NLP sentiment analysis | 07_Core_Product/NLWeb/ |
| 4 | StylePsychologyAgent | Apply style-aware product filtering | Product catalog, StyleProfile | FilteredProducts | Custom ML model | README.md - Personalization |
| 5 | StylePsychologyAgent | Generate styling psychology insights | FilteredProducts, DesiredFeeling | PsychologyInsights | GPT-3.5/4 | 05_External_Services/AI_Libraries/ |
| 6 | StylePsychologyAgent | Create confidence-building response | Products, insights, styling_tips | AgentResponse | Response templates | - |
| 7 | StylePsychologyAgent | Update user style profile | interaction_data, choices | Updated StyleProfile | PostgreSQL | 02_Core_Technologies/SQLAlchemy/ |

### **Intelligence Logic - Style Profile Building**

```python
class StyleProfile:
    """Comprehensive user style profile built from multiple data sources"""
    
    # Derived from purchases and interactions
    preferred_colors: List[str]
    avoided_colors: List[str]
    style_categories: Dict[str, float]  # {"minimalist": 0.8, "bohemian": 0.3}
    preferred_brands: List[str]
    size_preferences: Dict[str, str]
    price_sensitivity: float
    
    # Derived from conversations
    body_confidence_areas: List[str]  # Areas they want to highlight/minimize
    lifestyle_indicators: List[str]   # "busy_professional", "creative_type"
    occasion_frequency: Dict[str, int]  # How often they shop for work vs casual
    
    # Psychological preferences
    confidence_boosters: List[str]    # "structured_blazers", "A_line_dresses"
    comfort_zones: List[str]          # Styles they always return to
    aspiration_styles: List[str]      # Styles they want to try but haven't
    
class StylePsychologyAgent:
    def build_style_profile(self, user_id: str, context: ConversationState) -> StyleProfile:
        """Build comprehensive style profile from all available data"""
        
        profile = StyleProfile()
        
        # Analyze purchase history
        purchases = self.get_user_purchases(user_id)
        profile.preferred_colors = self.extract_color_preferences(purchases)
        profile.style_categories = self.analyze_style_distribution(purchases)
        profile.preferred_brands = self.identify_brand_loyalty(purchases)
        
        # Analyze conversation history
        conversations = self.get_conversation_history(user_id)
        profile.body_confidence_areas = self.extract_confidence_indicators(conversations)
        profile.lifestyle_indicators = self.infer_lifestyle(conversations, purchases)
        
        # Analyze interaction patterns
        interactions = self.get_user_interactions(user_id)
        profile.comfort_zones = self.identify_repeat_patterns(interactions)
        profile.aspiration_styles = self.identify_browsed_but_not_bought(interactions)
        
        return profile
    
    def analyze_emotional_intent(self, text: str, profile: StyleProfile) -> DesiredFeeling:
        """Understand the emotional/psychological need behind the request"""
        
        # Confidence-related keywords and their implications
        confidence_mapping = {
            "powerful": {"styles": ["structured", "tailored"], "colors": ["black", "navy", "burgundy"]},
            "feminine": {"styles": ["flowing", "soft"], "colors": ["pink", "pastels", "florals"]},
            "professional": {"styles": ["blazers", "pencil_skirts"], "colors": ["neutral", "classic"]},
            "creative": {"styles": ["unique", "artistic"], "colors": ["bold", "unexpected"]},
            "approachable": {"styles": ["soft", "casual_chic"], "colors": ["warm", "friendly"]},
        }
        
        desired_feeling = DesiredFeeling()
        
        for keyword, attributes in confidence_mapping.items():
            if keyword in text.lower():
                desired_feeling.primary_emotion = keyword
                desired_feeling.recommended_styles = attributes["styles"]
                desired_feeling.recommended_colors = attributes["colors"]
                break
        
        # Consider user's existing style profile
        if profile.comfort_zones:
            desired_feeling.comfort_integration = self.suggest_comfort_zone_bridge(
                desired_feeling, profile.comfort_zones
            )
        
        return desired_feeling
```

### **Confidence-Building Response Generation**

```python
def create_confidence_building_response(self, products: List[Product], 
                                       insights: PsychologyInsights,
                                       desired_feeling: DesiredFeeling) -> AgentResponse:
    """Generate empathetic, confidence-building product recommendations"""
    
    response_parts = []
    
    # Empathetic opening based on emotional context
    if desired_feeling.primary_emotion == "powerful":
        opening = "I understand you want to feel powerful and confident! Here are pieces that will help you command any room:"
    elif desired_feeling.primary_emotion == "professional":
        opening = "Perfect timing to elevate your professional wardrobe! These pieces will help you feel polished and confident:"
    else:
        opening = f"I love that you want to feel {desired_feeling.primary_emotion}! Here's what I've selected:"
    
    response_parts.append(opening)
    
    # Product recommendations with psychological reasoning
    for i, product in enumerate(products[:3], 1):
        reason = insights.get_psychological_reason(product, desired_feeling)
        styling_tip = insights.get_styling_tip(product, desired_feeling)
        
        product_text = f"\n{i}. **{product.name}** - ${product.price}\n"
        product_text += f"   💫 {reason}\n"
        product_text += f"   ✨ Styling tip: {styling_tip}\n"
        
        response_parts.append(product_text)
    
    # Confidence-building conclusion
    conclusion = self.generate_confidence_conclusion(desired_feeling, insights)
    response_parts.append(f"\n{conclusion}")
    
    return AgentResponse(
        text="\n".join(response_parts),
        products=products,
        confidence_boost_message=insights.confidence_message,
        styling_tips=insights.all_styling_tips
    )

def generate_confidence_conclusion(self, desired_feeling: DesiredFeeling, 
                                  insights: PsychologyInsights) -> str:
    """Generate encouraging, personalized conclusion"""
    
    conclusions = {
        "powerful": "Remember: confidence comes from within, but the right outfit can be your armor. You've got this! 💪",
        "professional": "These pieces will help you feel as capable as you are. Walk into that meeting knowing you look incredible! 🌟",
        "creative": "Your unique style is what makes you special. These pieces will help you express your creativity with confidence! 🎨",
        "feminine": "Embrace your femininity with pieces that make you feel beautiful and strong. You deserve to feel amazing! 🌸"
    }
    
    return conclusions.get(desired_feeling.primary_emotion, 
                          "You have amazing style instincts. Trust yourself and wear what makes you feel fantastic! ✨")
```

---

## 🔮 Predictive Commerce Agent - The Proactive Planner

### **Agent Profile**
- **Core Purpose**: "You will need this soon" - anticipating customer needs
- **Pricing Tier**: Enterprise
- **Personality**: Insightful, anticipatory, helpful
- **Specialty**: Pattern recognition and proactive recommendations

### **Activation Pattern**
Unlike other agents, the Predictive Commerce Agent is **not reactive**. It operates on:
- Scheduled background analysis (daily/weekly)
- User login triggers (checking for new predictions)
- Seasonal/weather change events
- Life event triggers (birthday approaching, season changing)

### **Detailed Agent Workflow**

| Step | Actor | Action | Data In | Data Out | Technology | Documentation Reference |
|------|-------|--------|---------|----------|------------|-------------------------|
| 1 | GCP Cloud Scheduler | Trigger predictive analysis job | Cron schedule | Pub/Sub message | Cloud Scheduler | 03_Infrastructure/Cloud_Platforms/GCP/ |
| 2 | Predictive Worker | Receive job for specific user | user_id, analysis_type | - | Cloud Function/Celery | 02_Core_Technologies/Celery/ |
| 3 | PredictiveCommerceAgent | Build comprehensive user profile | user_id | FullUserProfile | PostgreSQL aggregation | - |
| 4 | PredictiveCommerceAgent | Run forecasting models | FullUserProfile, seasonal_data | PredictedNeeds | ML models (Prophet) | 07_Core_Product/NLWeb/ |
| 5 | PredictiveCommerceAgent | Find products for predicted needs | PredictedNeeds, store_id | CuratedCollection | Product matching | - |
| 6 | PredictiveCommerceAgent | Score prediction confidence | CuratedCollection, user_patterns | ScoredPredictions | Confidence modeling | - |
| 7 | PredictiveCommerceAgent | Cache recommendations | user_id, ScoredPredictions | Cache success | Redis SET with TTL | 06_Data_Storage/Redis/ |
| 8 | Frontend (on login) | Check for predictions | user_id | CuratedCollection or null | Redis GET | - |

### **Intelligence Logic - Predictive Modeling**

```python
class PredictiveCommerceAgent:
    def build_full_user_profile(self, user_id: str) -> FullUserProfile:
        """Create comprehensive profile for predictive analysis"""
        
        profile = FullUserProfile()
        
        # Purchase history analysis
        purchases = self.get_purchase_history(user_id, months=24)
        profile.seasonal_patterns = self.analyze_seasonal_buying(purchases)
        profile.category_cycles = self.identify_replacement_cycles(purchases)
        profile.brand_loyalty = self.calculate_brand_stickiness(purchases)
        profile.price_evolution = self.track_price_point_changes(purchases)
        
        # Behavioral analysis
        interactions = self.get_user_interactions(user_id, months=6)
        profile.browsing_patterns = self.analyze_browsing_behavior(interactions)
        profile.search_evolution = self.track_search_pattern_changes(interactions)
        profile.engagement_cycles = self.identify_shopping_frequency(interactions)
        
        # External data integration
        profile.location_data = self.get_user_location_context(user_id)
        profile.calendar_events = self.infer_upcoming_needs(purchases, interactions)
        
        return profile
    
    def run_forecasting_models(self, profile: FullUserProfile) -> List[PredictedNeed]:
        """Apply multiple forecasting models to predict future needs"""
        
        predictions = []
        
        # Model 1: Seasonal Forecasting
        seasonal_needs = self.predict_seasonal_needs(profile.seasonal_patterns)
        predictions.extend(seasonal_needs)
        
        # Model 2: Replacement Cycle Prediction
        replacement_needs = self.predict_replacements(profile.category_cycles)
        predictions.extend(replacement_needs)
        
        # Model 3: Life Event Prediction
        life_event_needs = self.predict_life_event_shopping(profile.calendar_events)
        predictions.extend(life_event_needs)
        
        # Model 4: Weather-Driven Needs
        weather_needs = self.predict_weather_driven_needs(profile.location_data)
        predictions.extend(weather_needs)
        
        # Model 5: Style Evolution Prediction
        style_evolution = self.predict_style_changes(profile.search_evolution)
        predictions.extend(style_evolution)
        
        return self.consolidate_predictions(predictions)
    
    def predict_seasonal_needs(self, seasonal_patterns: Dict) -> List[PredictedNeed]:
        """Predict needs based on seasonal buying patterns"""
        
        predictions = []
        current_season = self.get_current_season()
        next_season = self.get_next_season()
        
        # Look at what they bought last year at this time
        last_year_purchases = seasonal_patterns.get(f"{next_season}_last_year", [])
        
        for category, items in last_year_purchases.items():
            # Predict they'll need similar items this year
            confidence = self.calculate_seasonal_confidence(category, items)
            
            if confidence > 0.7:  # High confidence prediction
                predictions.append(PredictedNeed(
                    category=category,
                    need_type="seasonal_refresh",
                    confidence=confidence,
                    predicted_timing=self.estimate_seasonal_timing(next_season),
                    reasoning=f"Last {next_season}, you shopped for {category}. "
                             f"Time to refresh your {next_season} wardrobe!"
                ))
        
        return predictions
    
    def predict_replacements(self, category_cycles: Dict) -> List[PredictedNeed]:
        """Predict when items need replacing based on purchase cycles"""
        
        predictions = []
        
        for category, cycle_data in category_cycles.items():
            last_purchase = cycle_data["last_purchase_date"]
            average_cycle = cycle_data["average_replacement_cycle"]
            
            days_since_purchase = (datetime.now() - last_purchase).days
            predicted_replacement_date = last_purchase + timedelta(days=average_cycle)
            
            if predicted_replacement_date <= datetime.now() + timedelta(days=30):
                # Replacement due within 30 days
                confidence = min(0.9, days_since_purchase / average_cycle)
                
                predictions.append(PredictedNeed(
                    category=category,
                    need_type="replacement",
                    confidence=confidence,
                    predicted_timing="within_30_days",
                    reasoning=f"Your {category} from {last_purchase.strftime('%B %Y')} "
                             f"is due for replacement based on your typical {average_cycle}-day cycle."
                ))
        
        return predictions
```

### **Proactive Delivery System**

```python
def create_proactive_recommendation(self, predictions: List[ScoredPrediction], 
                                   user_context: UserContext) -> ProactiveRecommendation:
    """Create compelling proactive recommendation for user"""
    
    # Select best prediction based on confidence and timing
    best_prediction = max(predictions, key=lambda p: p.confidence * p.urgency_score)
    
    if best_prediction.confidence < 0.6:
        return None  # Don't show low-confidence predictions
    
    recommendation = ProactiveRecommendation()
    
    # Personalized message based on prediction type
    if best_prediction.need_type == "seasonal_refresh":
        recommendation.headline = f"🍂 {self.get_season_name()} wardrobe refresh time!"
        recommendation.message = f"Based on your shopping last year, you'll love these new {best_prediction.category} arrivals."
    
    elif best_prediction.need_type == "replacement":
        recommendation.headline = f"💡 Time to refresh your {best_prediction.category}"
        recommendation.message = best_prediction.reasoning
    
    elif best_prediction.need_type == "life_event":
        recommendation.headline = f"🎉 Perfect timing for {best_prediction.event_type}"
        recommendation.message = f"We've curated some special pieces for your upcoming {best_prediction.event_type}."
    
    # Add products with explanations
    recommendation.products = best_prediction.curated_products
    recommendation.confidence_display = f"{best_prediction.confidence:.0%} match"
    recommendation.timing_note = self.format_timing(best_prediction.predicted_timing)
    
    return recommendation

def format_for_dashboard_display(self, recommendation: ProactiveRecommendation) -> Dict:
    """Format for display in B2B dashboard or user interface"""
    
    return {
        "type": "proactive_recommendation",
        "headline": recommendation.headline,
        "message": recommendation.message,
        "products": [p.to_dict() for p in recommendation.products],
        "confidence": recommendation.confidence_display,
        "timing": recommendation.timing_note,
        "cta": "View Recommendations",
        "dismissible": True,
        "analytics_label": f"predictive_{recommendation.need_type}"
    }
```

---

## 🤝 Agent Collaboration Patterns

### **Multi-Agent Workflows**
Agents don't work in isolation - they collaborate to provide sophisticated, layered assistance.

#### **Pattern 1: Sequential Refinement**

```
User: [Uploads beach photo] "Which of these would look most professional for a conference?"

Flow:
1. ConversationManager routes to VisualDiscoveryAgent (image upload trigger)
2. VisualDiscoveryAgent finds 10 beach-inspired dresses
3. ConversationManager detects "professional" keyword in follow-up
4. StylePsychologyAgent activated with previous results as input
5. StylePsychologyAgent re-ranks for professionalism + personal style
6. Response combines visual similarity + professional styling advice
```

#### **Pattern 2: Collaborative Enhancement**

```
User: "I'm going to Miami for a business conference next month"

Flow:
1. ConversationManager detects travel + business keywords
2. DestinationCommerceAgent activated for primary response
3. StylePsychologyAgent automatically consulted for business styling
4. Combined response: weather-appropriate + professionally confident
```

#### **Pattern 3: Predictive Integration**

```
Background Process:
1. PredictiveCommerceAgent identifies user needs winter coat
2. Caches recommendation in Redis

User Session:
1. User uploads photo of current coat: "Something similar but warmer"
2. VisualDiscoveryAgent finds similar styles
3. ConversationManager checks predictive cache
4. Response enhanced with: "Perfect timing! Based on the weather forecast and your shopping patterns, you'll need this soon."
```

### **State Sharing Architecture**

```python
class SharedConversationState:
    """State object passed between all agents"""
    
    # Core context
    user_id: str
    store_id: str
    session_id: str
    
    # Cross-agent data
    active_products: List[Product]  # Products from previous agent
    user_style_profile: StyleProfile  # Shared style understanding
    search_context: Dict[str, Any]  # Search parameters and filters
    conversation_intent: Intent  # Overall conversation goal
    
    # Agent-specific results that others can use
    visual_search_results: Optional[List[Product]]
    travel_context: Optional[TravelContext]
    style_recommendations: Optional[List[StyleAdvice]]
    predictions: Optional[List[PredictedNeed]]
    
    def update_from_agent(self, agent_name: str, agent_response: AgentResponse):
        """Update shared state when agent completes"""
        
        if agent_name == "visual_discovery":
            self.visual_search_results = agent_response.products
            self.search_context.update(agent_response.search_metadata)
        
        elif agent_name == "destination_commerce":
            self.travel_context = agent_response.travel_context
            
        elif agent_name == "style_psychology":
            self.user_style_profile.update(agent_response.style_insights)
            self.style_recommendations = agent_response.style_advice
        
        # Always add to conversation history
        self.conversation_history.append(agent_response.to_message())
```

### **Handoff Protocols**

```python
class AgentHandoff:
    @staticmethod
    def should_collaborate(current_agent: str, user_input: str, 
                          context: SharedConversationState) -> Optional[str]:
        """Determine if another agent should collaborate"""
        
        collaboration_triggers = {
            "visual_discovery": {
                "professional": "style_psychology",
                "work": "style_psychology", 
                "travel": "destination_commerce",
                "trip": "destination_commerce"
            },
            "destination_commerce": {
                "confident": "style_psychology",
                "professional": "style_psychology"
            },
            "style_psychology": {
                "travel": "destination_commerce",
                "similar to this": "visual_discovery"
            }
        }
        
        triggers = collaboration_triggers.get(current_agent, {})
        
        for keyword, target_agent in triggers.items():
            if keyword in user_input.lower():
                return target_agent
        
        return None
    
    @staticmethod
    def prepare_handoff_context(from_agent: str, to_agent: str, 
                               context: SharedConversationState) -> Dict:
        """Prepare context for agent handoff"""
        
        handoff_context = {
            "previous_agent": from_agent,
            "previous_results": context.get_agent_results(from_agent),
            "shared_state": context,
            "collaboration_type": "refinement"
        }
        
        # Agent-specific context preparation
        if to_agent == "style_psychology":
            handoff_context["style_context"] = {
                "products_to_analyze": context.active_products,
                "style_requirement": context.extract_style_keywords(),
                "confidence_goal": context.extract_confidence_keywords()
            }
        
        return handoff_context
```

---

## 🔧 Implementation Specifications

### **Base Agent Architecture**

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class AgentResponse(BaseModel):
    """Standardized response format for all agents"""
    text: str
    products: Optional[List[Product]] = None
    confidence: float
    agent_name: str
    reasoning: Optional[str] = None
    follow_up_suggestions: List[str] = []
    metadata: Dict[str, Any] = {}

class BaseAgent(ABC):
    """Base class that all agents inherit from"""
    
    def __init__(self, store_id: str, context: SharedConversationState):
        self.store_id = store_id
        self.context = context
        self.logger = logging.getLogger(f"agent.{self.__class__.__name__}")
    
    @abstractmethod
    async def process(self, user_input: str, image: Optional[bytes] = None) -> AgentResponse:
        """Main processing method that each agent must implement"""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return list of capabilities this agent provides"""
        pass
    
    def update_context(self, response: AgentResponse):
        """Update shared context with agent results"""
        self.context.update_from_agent(self.__class__.__name__.lower(), response)
    
    async def get_products(self, filters: Dict[str, Any]) -> List[Product]:
        """Common product retrieval method"""
        # Implementation details for database/vector search
        pass
    
    def format_response(self, products: List[Product], 
                       reasoning: str, confidence: float) -> AgentResponse:
        """Common response formatting"""
        return AgentResponse(
            text=self.generate_response_text(products, reasoning),
            products=products,
            confidence=confidence,
            agent_name=self.__class__.__name__,
            reasoning=reasoning
        )

class VisualDiscoveryAgent(BaseAgent):
    """Implementation of Visual Discovery Agent"""
    
    async def process(self, user_input: str, image: Optional[bytes] = None) -> AgentResponse:
        """Process visual search request"""
        if not image:
            return self.format_error("No image provided for visual search")
        
        # Step 1: Extract visual features
        style_dna = await self.extract_style_dna(image)
        
        # Step 2: Generate embeddings
        embedding = await self.generate_embedding(image)
        
        # Step 3: Search similar products
        candidates = await self.search_similar_products(embedding)
        
        # Step 4: Apply intelligent ranking
        ranked_products = self.apply_intelligent_ranking(candidates, style_dna)
        
        # Step 5: Format response
        response = self.format_response(
            products=ranked_products[:10],
            reasoning=f"Found {len(candidates)} visually similar products",
            confidence=self.calculate_overall_confidence(ranked_products)
        )
        
        self.update_context(response)
        return response
    
    def get_capabilities(self) -> List[str]:
        return ["visual_similarity_search", "style_analysis", "product_matching"]
```

### **Database Schema for Agent State**

```sql
-- Conversation state storage
CREATE TABLE conversation_states (
    session_id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255),
    store_id VARCHAR(255),
    active_agent VARCHAR(100),
    state_data JSONB,
    last_activity TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Agent interaction logs
CREATE TABLE agent_interactions (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255),
    agent_name VARCHAR(100),
    user_input TEXT,
    agent_response JSONB,
    processing_time_ms INTEGER,
    confidence_score FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Style profiles for Style Psychology Agent
CREATE TABLE user_style_profiles (
    user_id VARCHAR(255) PRIMARY KEY,
    store_id VARCHAR(255),
    style_data JSONB,
    confidence_scores JSONB,
    last_updated TIMESTAMP DEFAULT NOW()
);

-- Predictive recommendations cache
CREATE TABLE predictive_recommendations (
    user_id VARCHAR(255),
    store_id VARCHAR(255),
    prediction_type VARCHAR(100),
    recommendations JSONB,
    confidence FLOAT,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (user_id, store_id, prediction_type)
);
```

---

## 📈 Intelligence Evolution & Learning

### **Continuous Learning Architecture**

```python
class AgentLearningSystem:
    """System for continuous improvement of agent intelligence"""
    
    def __init__(self):
        self.feedback_processor = FeedbackProcessor()
        self.model_updater = ModelUpdater()
        self.performance_tracker = PerformanceTracker()
    
    async def process_user_feedback(self, session_id: str, feedback: UserFeedback):
        """Process user feedback to improve agent performance"""
        
        # Get the interaction that received feedback
        interaction = await self.get_interaction(session_id, feedback.interaction_id)
        
        if feedback.type == "positive":
            # Reinforce successful patterns
            await self.reinforce_success_pattern(interaction, feedback)
        
        elif feedback.type == "negative":
            # Learn from failures
            await self.learn_from_failure(interaction, feedback)
        
        # Update agent models
        await self.update_agent_models(interaction.agent_name, feedback)
    
    async def reinforce_success_pattern(self, interaction: AgentInteraction, 
                                       feedback: UserFeedback):
        """Reinforce patterns that led to successful outcomes"""
        
        if interaction.agent_name == "visual_discovery":
            # Strengthen visual similarity weights for successful matches
            successful_features = interaction.response.metadata.get("style_features")
            await self.update_visual_weights(successful_features, weight_increase=0.1)
        
        elif interaction.agent_name == "style_psychology":
            # Reinforce successful style-emotion mappings
            successful_mapping = {
                "user_emotion": interaction.user_input_analysis.emotion,
                "recommended_style": interaction.response.metadata.get("style_recommendation"),
                "user_satisfaction": feedback.score
            }
            await self.update_psychology_model(successful_mapping)
    
    async def analyze_agent_performance(self, agent_name: str, 
                                       time_period: timedelta) -> PerformanceReport:
        """Analyze agent performance over time"""
        
        interactions = await self.get_agent_interactions(agent_name, time_period)
        
        report = PerformanceReport()
        report.agent_name = agent_name
        report.total_interactions = len(interactions)
        report.average_confidence = np.mean([i.confidence_score for i in interactions])
        report.user_satisfaction = await self.calculate_satisfaction_score(interactions)
        
        # Agent-specific metrics
        if agent_name == "visual_discovery":
            report.visual_accuracy = await self.calculate_visual_accuracy(interactions)
            report.top_performing_categories = await self.analyze_category_performance(interactions)
        
        elif agent_name == "style_psychology":
            report.style_prediction_accuracy = await self.calculate_style_accuracy(interactions)
            report.confidence_boost_effectiveness = await self.measure_confidence_impact(interactions)
        
        return report
```

### **A/B Testing Framework for Agents**

```python
class AgentExperimentFramework:
    """Framework for A/B testing different agent behaviors"""
    
    def __init__(self):
        self.experiment_manager = ExperimentManager()
        self.variant_router = VariantRouter()
    
    async def create_agent_experiment(self, experiment_config: ExperimentConfig):
        """Create new A/B test for agent behavior"""
        
        experiment = AgentExperiment()
        experiment.name = experiment_config.name
        experiment.agent_name = experiment_config.agent_name
        experiment.variants = experiment_config.variants
        experiment.traffic_allocation = experiment_config.traffic_allocation
        experiment.success_metrics = experiment_config.success_metrics
        
        # Example: Test different ranking algorithms for Visual Discovery
        if experiment_config.agent_name == "visual_discovery":
            experiment.variants = {
                "control": {"ranking_algorithm": "similarity_only"},
                "variant_a": {"ranking_algorithm": "similarity_plus_style"},
                "variant_b": {"ranking_algorithm": "ml_enhanced_ranking"}
            }
        
        await self.experiment_manager.create_experiment(experiment)
        return experiment.id
    
    async def get_agent_variant(self, user_id: str, agent_name: str) -> Dict[str, Any]:
        """Get the variant configuration for a user and agent"""
        
        active_experiments = await self.experiment_manager.get_active_experiments(agent_name)
        
        variant_config = {}
        for experiment in active_experiments:
            user_variant = await self.variant_router.get_user_variant(
                user_id, experiment.id
            )
            variant_config.update(experiment.variants[user_variant])
        
        return variant_config
    
    async def track_experiment_outcome(self, user_id: str, experiment_id: str, 
                                      outcome: ExperimentOutcome):
        """Track the outcome of an experimental interaction"""
        
        await self.experiment_manager.record_outcome(
            experiment_id=experiment_id,
            user_id=user_id,
            variant=outcome.variant,
            success_metrics=outcome.metrics,
            timestamp=datetime.now()
        )
```

### **Performance Monitoring Dashboard**

```python
class AgentPerformanceMonitor:
    """Real-time monitoring of agent performance"""
    
    def get_real_time_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics for all agents"""
        
        return {
            "visual_discovery": {
                "requests_per_minute": self.get_rpm("visual_discovery"),
                "average_confidence": self.get_avg_confidence("visual_discovery"),
                "error_rate": self.get_error_rate("visual_discovery"),
                "response_time_p95": self.get_response_time("visual_discovery", 95)
            },
            "destination_commerce": {
                "requests_per_minute": self.get_rpm("destination_commerce"),
                "weather_api_success_rate": self.get_external_api_success("weather"),
                "complete_recommendation_rate": self.get_completion_rate("destination_commerce")
            },
            "style_psychology": {
                "style_profile_accuracy": self.get_style_accuracy(),
                "confidence_boost_score": self.get_confidence_impact(),
                "personalization_effectiveness": self.get_personalization_score()
            },
            "predictive_commerce": {
                "prediction_accuracy": self.get_prediction_accuracy(),
                "proactive_engagement_rate": self.get_proactive_engagement(),
                "prediction_conversion_rate": self.get_prediction_conversion()
            }
        }
    
    def set_performance_alerts(self):
        """Set up alerts for agent performance issues"""
        
        alerts = [
            Alert(
                name="visual_discovery_low_confidence",
                condition="avg_confidence < 0.7 for 5 minutes",
                action="notify_ml_team"
            ),
            Alert(
                name="destination_commerce_weather_api_failure",
                condition="weather_api_success_rate < 0.95 for 2 minutes",
                action="switch_to_backup_weather_service"
            ),
            Alert(
                name="style_psychology_low_satisfaction",
                condition="user_satisfaction < 0.8 for 10 minutes",
                action="fallback_to_simple_recommendations"
            )
        ]
        
        for alert in alerts:
            self.alert_manager.create_alert(alert)
```

---

This comprehensive AI Agent Architecture document provides the complete blueprint for implementing the intelligent core of the NLyzer platform. Each agent is designed with specific capabilities, clear decision-making processes, and sophisticated collaboration patterns that work together to create a truly intelligent shopping assistant.

The architecture supports continuous learning, A/B testing, and performance monitoring to ensure the agents evolve and improve over time, delivering increasingly personalized and effective shopping experiences for every customer.