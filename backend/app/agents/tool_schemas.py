from typing import Any


TOOL_DEFINITIONS: list[dict[str, Any]] = [
    {
        "type": "function",
        "name": "get_customer_details",
        "description": (
            "Retrieve verified customer details from the loan management backend. "
            "Use this when customer identity or customer information is required."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The customer identifier.",
                }
            },
            "required": ["customer_id"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_loan_status",
        "description": (
            "Retrieve the verified current loan status from the loan management "
            "backend. Use this whenever the customer asks about loan status."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "application_id": {
                    "type": "string",
                    "description": "The loan application identifier.",
                }
            },
            "required": ["application_id"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_pending_documents",
        "description": (
            "Retrieve the verified list of documents still required for a loan "
            "application. Use this when the customer asks which documents are "
            "pending or required."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "application_id": {
                    "type": "string",
                    "description": "The loan application identifier.",
                }
            },
            "required": ["application_id"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "create_support_request",
        "description": (
            "Create a support request in the backend when the customer has a "
            "complaint or requests human assistance."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The customer identifier.",
                },
                "reason": {
                    "type": "string",
                    "description": "A concise description of the support reason.",
                },
            },
            "required": ["customer_id", "reason"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "schedule_callback",
        "description": (
            "Schedule a callback for the customer when they request a callback. "
            "Only use a datetime explicitly provided or clearly agreed by the customer."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The customer identifier.",
                },
                "datetime_value": {
                    "type": "string",
                    "description": (
                        "Requested callback date and time in ISO-8601 format."
                    ),
                },
            },
            "required": ["customer_id", "datetime_value"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "send_document_upload_link",
        "description": (
            "Generate a verified document upload link for the customer when "
            "they ask how or where to upload required documents."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The customer identifier.",
                }
            },
            "required": ["customer_id"],
            "additionalProperties": False,
        },
        "strict": True,
    },
]
