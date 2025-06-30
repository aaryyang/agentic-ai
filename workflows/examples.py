"""
Example workflow definitions for common CRM automation scenarios
"""

# Lead Processing Workflow
LEAD_QUALIFICATION_WORKFLOW = {
    "name": "Automated Lead Qualification",
    "description": "Automatically qualify incoming leads and assign to sales reps",
    "steps": [
        {
            "type": "agent_task",
            "parameters": {
                "agent_type": "sales",
                "task": "Qualify incoming lead based on BANT criteria",
                "context": {
                    "lead_source": "web_form",
                    "qualification_criteria": ["budget", "authority", "need", "timeline"]
                }
            }
        },
        {
            "type": "condition",
            "parameters": {
                "condition": "qualification_score >= 75"
            }
        },
        {
            "type": "agent_task",
            "parameters": {
                "agent_type": "sales",
                "task": "Assign high-quality lead to senior sales rep",
                "context": {
                    "assignment_rule": "round_robin",
                    "rep_tier": "senior"
                }
            }
        },
        {
            "type": "notification",
            "parameters": {
                "message": "High-priority lead assigned for immediate follow-up",
                "recipients": ["sales_manager@company.com"]
            }
        }
    ]
}

# Quote Generation Workflow
QUOTE_GENERATION_WORKFLOW = {
    "name": "Automated Quote Generation",
    "description": "Generate and send quotes based on customer requirements",
    "steps": [
        {
            "type": "agent_task",
            "parameters": {
                "agent_type": "quote",
                "task": "Calculate pricing based on customer requirements",
                "context": {
                    "pricing_model": "tiered",
                    "discount_eligibility": True
                }
            }
        },
        {
            "type": "agent_task",
            "parameters": {
                "agent_type": "quote",
                "task": "Generate professional quote document",
                "context": {
                    "template": "standard_quote",
                    "include_terms": True
                }
            }
        },
        {
            "type": "data_operation",
            "parameters": {
                "operation": "create",
                "target": "crm",
                "data": {
                    "record_type": "quote",
                    "status": "sent"
                }
            }
        },
        {
            "type": "notification",
            "parameters": {
                "message": "Quote generated and sent to customer",
                "recipients": ["sales@company.com"]
            }
        }
    ]
}

# Meeting Follow-up Workflow
MEETING_FOLLOWUP_WORKFLOW = {
    "name": "Post-Meeting Follow-up",
    "description": "Automated follow-up actions after client meetings",
    "steps": [
        {
            "type": "wait",
            "parameters": {
                "seconds": 3600  # Wait 1 hour after meeting
            }
        },
        {
            "type": "agent_task",
            "parameters": {
                "agent_type": "operations",
                "task": "Create follow-up tasks based on meeting notes",
                "context": {
                    "task_types": ["proposal_prep", "demo_scheduling", "contract_review"]
                }
            }
        },
        {
            "type": "agent_task",
            "parameters": {
                "agent_type": "scheduler",
                "task": "Schedule follow-up meeting in 1 week",
                "context": {
                    "meeting_type": "follow_up",
                    "duration": 30
                }
            }
        },
        {
            "type": "notification",
            "parameters": {
                "message": "Follow-up tasks created and next meeting scheduled",
                "recipients": ["account_manager@company.com"]
            }
        }
    ]
}

# Customer Onboarding Workflow
CUSTOMER_ONBOARDING_WORKFLOW = {
    "name": "New Customer Onboarding",
    "description": "Comprehensive onboarding process for new customers",
    "steps": [
        {
            "type": "agent_task",
            "parameters": {
                "agent_type": "operations",
                "task": "Create customer record and setup account",
                "context": {
                    "account_type": "enterprise",
                    "setup_requirements": ["user_accounts", "integrations", "training"]
                }
            }
        },
        {
            "type": "agent_task",
            "parameters": {
                "agent_type": "scheduler",
                "task": "Schedule kickoff meeting with customer success team",
                "context": {
                    "meeting_type": "kickoff",
                    "duration": 90,
                    "participants": ["customer_success", "technical_team"]
                }
            }
        },
        {
            "type": "notification",
            "parameters": {
                "message": "Welcome package sent to new customer",
                "recipients": ["customer_success@company.com"]
            }
        },
        {
            "type": "agent_task",
            "parameters": {
                "agent_type": "operations",
                "task": "Set up 30, 60, 90 day check-in reminders",
                "context": {
                    "reminder_type": "customer_health_check",
                    "automated": True
                }
            }
        }
    ]
}

# Sales Pipeline Update Workflow
PIPELINE_UPDATE_WORKFLOW = {
    "name": "Automated Pipeline Updates",
    "description": "Update pipeline stages based on customer interactions",
    "steps": [
        {
            "type": "agent_task",
            "parameters": {
                "agent_type": "sales",
                "task": "Analyze recent customer interactions and update deal stage",
                "context": {
                    "interaction_types": ["email", "call", "meeting", "proposal_sent"],
                    "stage_progression_rules": "standard"
                }
            }
        },
        {
            "type": "agent_task",
            "parameters": {
                "agent_type": "sales",
                "task": "Update deal probability based on engagement score",
                "context": {
                    "scoring_model": "engagement_based",
                    "factors": ["response_time", "meeting_attendance", "stakeholder_involvement"]
                }
            }
        },
        {
            "type": "data_operation",
            "parameters": {
                "operation": "update",
                "target": "crm",
                "data": {
                    "record_type": "deal",
                    "fields": ["stage", "probability", "last_updated"]
                }
            }
        }
    ]
}

# All available workflows
AVAILABLE_WORKFLOWS = {
    "lead_qualification": LEAD_QUALIFICATION_WORKFLOW,
    "quote_generation": QUOTE_GENERATION_WORKFLOW,
    "meeting_followup": MEETING_FOLLOWUP_WORKFLOW,
    "customer_onboarding": CUSTOMER_ONBOARDING_WORKFLOW,
    "pipeline_update": PIPELINE_UPDATE_WORKFLOW
}
