"""
Cloud Function Remediator: Agent Kill-Switch and Remediation on GCP

This Cloud Function implements kill-switch capabilities and automated remediation
for agentic AI governance violations.
"""

import json
import os
import logging
from datetime import datetime
from google.cloud import secretmanager
from google.cloud import resource_manager

# ============================================================================
# Configuration
# ============================================================================

PROJECT_ID = os.environ.get('PROJECT_ID', '')
AGENT_REGISTRY_PROJECT = os.environ.get('AGENT_REGISTRY_PROJECT', PROJECT_ID)

logger = logging.getLogger(__name__)

# ============================================================================
# Kill-Switch Actions
# ============================================================================

def activate_kill_switch(agent_id: str, reason: str, violation_type: str) -> dict:
    """
    Activate kill-switch for a rogue or compromised agent.
    """
    logger.warning(f"KILL-SWITCH ACTIVATED for agent: {agent_id}")
    logger.warning(f"Reason: {reason}")
    logger.warning(f"Violation Type: {violation_type}")
    
    try:
        # In production, this would call Gemini Enterprise API to disable agent
        # gcloud alpha gemini enterprise agents disable --agent-id={agent_id}
        
        return {
            'status': 'kill-switch-activated',
            'agent_id': agent_id,
            'reason': reason,
            'violation_type': violation_type,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {
            'status': 'kill-switch-failed',
            'agent_id': agent_id,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }


def revoke_agent_credentials(agent_id: str, reason: str) -> dict:
    """
    Revoke agent credentials and access via Cloud IAM.
    """
    logger.info(f"Revoking credentials for agent: {agent_id}")
    
    try:
        # In production, this would revoke IAM credentials
        return {
            'status': 'credentials-revoked',
            'agent_id': agent_id,
            'reason': reason,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {
            'status': 'revocation-failed',
            'agent_id': agent_id,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }


def quarantine_agent(agent_id: str, reason: str) -> dict:
    """
    Quarantine an agent for investigation.
    """
    logger.info(f"Quarantining agent: {agent_id}")
    
    try:
        # In production, this would restrict agent access
        return {
            'status': 'agent-quarantined',
            'agent_id': agent_id,
            'reason': reason,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {
            'status': 'quarantine-failed',
            'agent_id': agent_id,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }


def remove_from_agent_registry(agent_id: str, reason: str) -> dict:
    """
    Remove agent from Agent Registry.
    """
    logger.info(f"Removing agent from registry: {agent_id}")
    
    try:
        # In production, this would call Agent Registry API
        return {
            'status': 'agent-removed-from-registry',
            'agent_id': agent_id,
            'reason': reason,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {
            'status': 'registry-removal-failed',
            'agent_id': agent_id,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }


# ============================================================================
# Violation Classification
# ============================================================================

def classify_violation(violation_type: str) -> dict:
    """
    Classify violation type and determine appropriate action.
    Based on OWASP Agentic Top 10 2026
    """
    severity_map = {
        'GOAL_HIJACK': {'severity': 'critical', 'action': 'kill-switch'},
        'TOOL_MISUSE': {'severity': 'critical', 'action': 'kill-switch'},
        'PRIVILEGE_ABUSE': {'severity': 'critical', 'action': 'kill-switch'},
        'RESOURCE_EXHAUSTION': {'severity': 'high', 'action': 'quarantine'},
        'IDENTITY_CONFUSION': {'severity': 'critical', 'action': 'revoke-credentials'},
        'MEMORY_POISONING': {'severity': 'high', 'action': 'quarantine'},
        'COST_RUNAWAY': {'severity': 'high', 'action': 'quarantine'},
        'MINOR_ANOMALY': {'severity': 'low', 'action': 'log-only'},
        'REGISTRY_VIOLATION': {'severity': 'high', 'action': 'remove-from-registry'}
    }
    
    return severity_map.get(violation_type, {'severity': 'medium', 'action': 'quarantine'})


# ============================================================================
# HTTP Trigger Entry Point
# ============================================================================

def remediate_agent(request):
    """
    HTTP-triggered Cloud Function for remediation.
    """
    logger.info('Remediator function processed a request.')
    
    try:
        request_json = request.get_json(silent=True)
        if not request_json:
            return (json.dumps({'error': 'No JSON body provided'}), 400)
        
        agent_id = request_json.get('agentId', 'unknown')
        violation_type = request_json.get('violationType', 'UNKNOWN')
        reason = request_json.get('reason', 'No reason provided')
        
        logger.info(f"Processing violation for agent: {agent_id}")
        logger.info(f"Violation Type: {violation_type}")
        
        # Classify violation
        classification = classify_violation(violation_type)
        severity = classification.get('severity', 'medium')
        action = classification.get('action', 'quarantine')
        
        # Execute appropriate action
        result = None
        
        if action == 'kill-switch':
            result = activate_kill_switch(agent_id, reason, violation_type)
        elif action == 'revoke-credentials':
            result = revoke_agent_credentials(agent_id, reason)
        elif action == 'quarantine':
            result = quarantine_agent(agent_id, reason)
        elif action == 'remove-from-registry':
            result = remove_from_agent_registry(agent_id, reason)
        else:
            result = {
                'status': 'logged-only',
                'agent_id': agent_id,
                'reason': reason,
                'violation_type': violation_type,
                'timestamp': datetime.now().isoformat()
            }
        
        return (json.dumps({
            'agentId': agent_id,
            'violationType': violation_type,
            'severity': severity,
            'action': action,
            'result': result,
            'timestamp': datetime.now().isoformat()
        }), 200)
    
    except Exception as e:
        logger.error(f"Error in remediation: {str(e)}")
        return (json.dumps({'error': str(e)}), 500)
