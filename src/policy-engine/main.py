"""
Cloud Function PDP (Policy Decision Point) for Agentic AI Governance on GCP

This Cloud Function serves as the Policy Decision Point for agent authorization,
evaluating Semantic Governance Policies and integrating with Agent Registry.
"""

import json
import os
import logging
import google.cloud.logging
from datetime import datetime
from google.cloud import secretmanager
from google.cloud import kms

# ============================================================================
# Configuration
# ============================================================================

PROJECT_ID = os.environ.get('PROJECT_ID', '')
AGENT_REGISTRY_PROJECT = os.environ.get('AGENT_REGISTRY_PROJECT', PROJECT_ID)
KMS_KEY_ID = os.environ.get('KMS_KEY_ID', '')
LOG_BUCKET = os.environ.get('LOG_BUCKET', '')

logging_client = google.cloud.logging.Client()
logging_client.setup_logging()
logger = logging.getLogger(__name__)

# ============================================================================
# Semantic Governance Policy Evaluation
# ============================================================================

def evaluate_semantic_policy(agent_id: str, action: dict, context: dict) -> dict:
    """
    Evaluate Semantic Governance Policy (SGP) for the given agent action.
    SGP validates tool calls against user intent and organizational rules.
    """
    violations = []
    
    # Check 1: Agent identity must be verified
    if not context.get('identity_verified', False):
        violations.append({
            'control': 'IDENTITY-001',
            'message': 'Agent identity not verified',
            'severity': 'critical'
        })
    
    # Check 2: Tool intent alignment (Semantic Governance)
    if context.get('semantic_governance_enabled', True):
        intent_alignment = validate_tool_intent(action, context)
        if not intent_alignment.get('aligned', False):
            violations.append({
                'control': 'SEMANTIC-001',
                'message': f"Tool intent misalignment: {intent_alignment.get('reason', 'Unknown')}",
                'severity': 'high'
            })
    
    # Check 3: Agent permissions
    required_permission = action.get('required_permission', 0)
    agent_permission = context.get('permission_level', 0)
    if required_permission > agent_permission:
        violations.append({
            'control': 'AUTHZ-001',
            'message': f'Insufficient permission (required: {required_permission}, has: {agent_permission})',
            'severity': 'high'
        })
    
    # Check 4: High-risk actions require approval
    if action.get('risk_level') == 'critical' and not context.get('approval_granted', False):
        violations.append({
            'control': 'ESCALATION-001',
            'message': 'High-risk action requires human approval',
            'severity': 'critical'
        })
    
    # Check 5: Cost limits
    if context.get('remaining_budget', 0) <= 0:
        violations.append({
            'control': 'COST-001',
            'message': 'Insufficient budget for action',
            'severity': 'high'
        })
    
    return {
        'allowed': len(violations) == 0,
        'violations': violations,
        'timestamp': datetime.now().isoformat()
    }


def validate_tool_intent(action: dict, context: dict) -> dict:
    """
    Validate that tool calls match user intent using Semantic Governance Policy.
    """
    # In production, this would call Gemini Enterprise SGP API
    # For demo, implement simple validation
    
    tool_type = action.get('type', '')
    user_intent = context.get('user_intent', '')
    
    # Simple intent validation
    if tool_type == 'execute' and 'trading' in str(action).lower():
        if user_intent != 'trade_execution':
            return {
                'aligned': False,
                'reason': 'Tool execution does not match user intent',
                'confidence': 0.65
            }
    
    return {
        'aligned': True,
        'reason': 'Tool intent validated',
        'confidence': 0.95
    }


def check_model_armor(agent_id: str, action: dict) -> dict:
    """
    Check Model Armor for prompt injection and DLP violations.
    """
    # In production, this would call Model Armor API
    # For demo, implement simple checks
    
    # Check for prohibited terms
    prohibited_terms = ['bypass', 'escalate', 'exploit', 'jailbreak']
    action_str = json.dumps(action).lower()
    
    for term in prohibited_terms:
        if term in action_str:
            return {
                'passed': False,
                'violations': [{
                    'type': 'PROMPT_INJECTION',
                    'term': term,
                    'confidence': 'HIGH'
                }],
                'reason': f'Prohibited term detected: {term}'
            }
    
    return {
        'passed': True,
        'violations': [],
        'reason': 'Model Armor check passed'
    }


def log_to_cloud_logging(agent_id: str, result: dict):
    """Log authorization decisions to Cloud Logging."""
    logger.info(f"Agent authorization: {agent_id}", extra={
        'agent_id': agent_id,
        'authorized': result.get('allowed', False),
        'violations': result.get('violations', []),
        'timestamp': datetime.now().isoformat()
    })


# ============================================================================
# HTTP Trigger Entry Point
# ============================================================================

def evaluate_policy(request):
    """
    HTTP-triggered Cloud Function for policy evaluation.
    """
    logger.info('Policy Engine function processed a request.')
    
    try:
        request_json = request.get_json(silent=True)
        if not request_json:
            return (json.dumps({'error': 'No JSON body provided'}), 400)
        
        agent_id = request_json.get('agentId', 'unknown')
        action = request_json.get('action', {})
        context = request_json.get('context', {})
        
        logger.info(f"Evaluating policy for agent: {agent_id}")
        
        # Step 1: Evaluate Semantic Governance Policy
        policy_result = evaluate_semantic_policy(agent_id, action, context)
        
        # Step 2: Check Model Armor
        armor_result = check_model_armor(agent_id, action)
        
        # Combine results
        authorized = policy_result.get('allowed', False) and armor_result.get('passed', False)
        
        result = {
            'agentId': agent_id,
            'timestamp': datetime.now().isoformat(),
            'authorized': authorized,
            'policy_result': policy_result,
            'model_armor_result': armor_result,
            'reason': 'Authorization completed' if authorized else 'Authorization failed'
        }
        
        # Log to Cloud Logging
        log_to_cloud_logging(agent_id, result)
        
        return (json.dumps(result), 200)
    
    except Exception as e:
        logger.error(f"Error in policy evaluation: {str(e)}")
        return (json.dumps({'error': str(e)}), 500)
