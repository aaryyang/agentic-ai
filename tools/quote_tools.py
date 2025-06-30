"""
Quote-specific tools for pricing calculations, quote generation, and proposal creation
"""

from typing import Dict, List, Any, Optional
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
import structlog

logger = structlog.get_logger(__name__)


class PricingCalculatorInput(BaseModel):
    """Input for pricing calculations"""
    products: List[Dict[str, Any]] = Field(description="List of products/services to price")
    quantity: int = Field(default=1, description="Quantity for each product")
    discount_type: Optional[str] = Field(default=None, description="Type of discount to apply")
    customer_tier: Optional[str] = Field(default="standard", description="Customer tier for pricing")


class PricingCalculatorTool(BaseTool):
    """Tool for calculating complex pricing with discounts and tiers"""
    
    name = "calculate_pricing"
    description = "Calculate pricing for products/services with volume discounts and customer tiers"
    args_schema = PricingCalculatorInput
    
    def _run(self, products: List[Dict[str, Any]], quantity: int = 1, 
             discount_type: str = None, customer_tier: str = "standard") -> str:
        """Calculate pricing with all applicable discounts"""
        try:
            logger.info(f"Calculating pricing for {len(products)} products")
            
            total_base_price = 0
            pricing_breakdown = []
            
            # Base pricing tiers
            tier_multipliers = {
                "standard": 1.0,
                "premium": 0.9,
                "enterprise": 0.8,
                "partner": 0.75
            }
            
            # Volume discount tiers
            volume_discounts = {
                1: 0.0,
                10: 0.05,
                50: 0.10,
                100: 0.15,
                500: 0.20
            }
            
            for product in products:
                base_price = product.get("price", 100)  # Default price
                product_total = base_price * quantity
                
                # Apply customer tier discount
                tier_multiplier = tier_multipliers.get(customer_tier, 1.0)
                product_total *= tier_multiplier
                
                # Apply volume discount
                volume_discount = 0
                for vol_threshold in sorted(volume_discounts.keys(), reverse=True):
                    if quantity >= vol_threshold:
                        volume_discount = volume_discounts[vol_threshold]
                        break
                
                product_total *= (1 - volume_discount)
                
                pricing_breakdown.append({
                    "product": product.get("name", "Unknown Product"),
                    "base_price": base_price,
                    "quantity": quantity,
                    "tier_discount": f"{(1-tier_multiplier)*100:.1f}%",
                    "volume_discount": f"{volume_discount*100:.1f}%",
                    "final_price": round(product_total, 2)
                })
                
                total_base_price += product_total
            
            # Apply additional discounts if specified
            if discount_type:
                additional_discounts = {
                    "new_customer": 0.10,
                    "renewal": 0.05,
                    "upgrade": 0.15,
                    "promotional": 0.20
                }
                
                additional_discount = additional_discounts.get(discount_type, 0)
                total_base_price *= (1 - additional_discount)
            
            result = {
                "pricing_breakdown": pricing_breakdown,
                "subtotal": round(sum([item["final_price"] for item in pricing_breakdown]), 2),
                "customer_tier": customer_tier,
                "volume_discount_applied": f"{volume_discount*100:.1f}%",
                "additional_discount": discount_type,
                "total_price": round(total_base_price, 2),
                "currency": "USD"
            }
            
            return f"Pricing calculation complete: {result}"
            
        except Exception as e:
            logger.error(f"Error calculating pricing: {str(e)}")
            return f"Error calculating pricing: {str(e)}"


class QuoteGeneratorInput(BaseModel):
    """Input for quote generation"""
    customer_info: Dict[str, Any] = Field(description="Customer information")
    items: List[Dict[str, Any]] = Field(description="Items to include in quote")
    terms: Dict[str, Any] = Field(default={}, description="Quote terms and conditions")


class QuoteGeneratorTool(BaseTool):
    """Tool for generating professional quotes"""
    
    name = "generate_quote"
    description = "Generate professional quotes with itemized pricing and terms"
    args_schema = QuoteGeneratorInput
    
    def _run(self, customer_info: Dict[str, Any], items: List[Dict[str, Any]], 
             terms: Dict[str, Any] = None) -> str:
        """Generate a professional quote"""
        try:
            logger.info(f"Generating quote for {customer_info.get('company', 'Unknown Customer')}")
            
            import uuid
            quote_id = f"QT-{str(uuid.uuid4())[:8].upper()}"
            
            # Calculate totals
            subtotal = sum([item.get("total", 0) for item in items])
            tax_rate = terms.get("tax_rate", 0.08)
            tax_amount = subtotal * tax_rate
            total_amount = subtotal + tax_amount
            
            quote = {
                "quote_id": quote_id,
                "date": "2025-06-27",
                "valid_until": "2025-07-27",
                "customer": {
                    "name": customer_info.get("name", ""),
                    "company": customer_info.get("company", ""),
                    "email": customer_info.get("email", ""),
                    "address": customer_info.get("address", "")
                },
                "items": items,
                "pricing_summary": {
                    "subtotal": round(subtotal, 2),
                    "tax_rate": f"{tax_rate*100:.1f}%",
                    "tax_amount": round(tax_amount, 2),
                    "total": round(total_amount, 2),
                    "currency": "USD"
                },
                "terms": {
                    "payment_terms": terms.get("payment_terms", "Net 30"),
                    "delivery": terms.get("delivery", "2-3 weeks"),
                    "warranty": terms.get("warranty", "1 year"),
                    "validity": "30 days"
                },
                "notes": terms.get("notes", "Thank you for your business!")
            }
            
            return f"Quote generated successfully: {quote}"
            
        except Exception as e:
            logger.error(f"Error generating quote: {str(e)}")
            return f"Error generating quote: {str(e)}"


class ProposalInput(BaseModel):
    """Input for proposal creation"""
    client_info: Dict[str, Any] = Field(description="Client information and requirements")
    solution: Dict[str, Any] = Field(description="Proposed solution details")
    pricing: Dict[str, Any] = Field(description="Pricing information")


class ProposalTool(BaseTool):
    """Tool for creating comprehensive business proposals"""
    
    name = "create_proposal"
    description = "Create detailed business proposals with solutions and pricing"
    args_schema = ProposalInput
    
    def _run(self, client_info: Dict[str, Any], solution: Dict[str, Any], 
             pricing: Dict[str, Any]) -> str:
        """Create a comprehensive business proposal"""
        try:
            logger.info(f"Creating proposal for {client_info.get('company', 'Unknown Client')}")
            
            import uuid
            proposal_id = f"PROP-{str(uuid.uuid4())[:8].upper()}"
            
            proposal = {
                "proposal_id": proposal_id,
                "date": "2025-06-27",
                "client": client_info,
                "executive_summary": {
                    "challenge": solution.get("problem_statement", "Business challenge to address"),
                    "solution_overview": solution.get("overview", "Our recommended solution"),
                    "key_benefits": solution.get("benefits", ["Improved efficiency", "Cost savings", "Better outcomes"])
                },
                "solution_details": {
                    "approach": solution.get("approach", "Comprehensive implementation approach"),
                    "deliverables": solution.get("deliverables", ["Phase 1 deliverables", "Phase 2 deliverables"]),
                    "timeline": solution.get("timeline", "12-week implementation"),
                    "methodology": solution.get("methodology", "Proven implementation methodology")
                },
                "investment": {
                    "total_investment": pricing.get("total", 0),
                    "payment_schedule": pricing.get("payment_schedule", "50% upfront, 50% on completion"),
                    "roi_projection": pricing.get("roi", "200% ROI within 12 months")
                },
                "next_steps": [
                    "Review and approve proposal",
                    "Sign service agreement",
                    "Begin project kickoff",
                    "Start implementation"
                ],
                "validity": "30 days from proposal date"
            }
            
            return f"Business proposal created: {proposal}"
            
        except Exception as e:
            logger.error(f"Error creating proposal: {str(e)}")
            return f"Error creating proposal: {str(e)}"


class DiscountInput(BaseModel):
    """Input for discount calculations"""
    base_amount: float = Field(description="Base amount before discount")
    discount_type: str = Field(description="Type of discount (percentage, fixed, volume)")
    discount_value: float = Field(description="Discount value")
    approval_required: bool = Field(default=True, description="Whether approval is required")


class DiscountTool(BaseTool):
    """Tool for calculating and applying discounts"""
    
    name = "apply_discount"
    description = "Calculate and apply various types of discounts with approval workflows"
    args_schema = DiscountInput
    
    def _run(self, base_amount: float, discount_type: str, discount_value: float, 
             approval_required: bool = True) -> str:
        """Apply discount and handle approval workflow"""
        try:
            logger.info(f"Applying {discount_type} discount of {discount_value}")
            
            if discount_type == "percentage":
                discount_amount = base_amount * (discount_value / 100)
                final_amount = base_amount - discount_amount
            elif discount_type == "fixed":
                discount_amount = discount_value
                final_amount = base_amount - discount_amount
            elif discount_type == "volume":
                # Volume discount based on tiers
                discount_percentage = min(discount_value, 25)  # Cap at 25%
                discount_amount = base_amount * (discount_percentage / 100)
                final_amount = base_amount - discount_amount
            else:
                return f"Unknown discount type: {discount_type}"
            
            # Check if approval is required
            approval_status = "pending" if approval_required and discount_amount > base_amount * 0.15 else "auto_approved"
            
            result = {
                "base_amount": base_amount,
                "discount_type": discount_type,
                "discount_value": discount_value,
                "discount_amount": round(discount_amount, 2),
                "final_amount": round(final_amount, 2),
                "discount_percentage": round((discount_amount / base_amount) * 100, 2),
                "approval_status": approval_status,
                "savings": round(discount_amount, 2)
            }
            
            return f"Discount applied: {result}"
            
        except Exception as e:
            logger.error(f"Error applying discount: {str(e)}")
            return f"Error applying discount: {str(e)}"
