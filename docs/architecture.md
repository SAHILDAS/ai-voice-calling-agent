# AI Voice Calling Agent — Architecture

## 1. Overview

The **AI Voice Calling Agent** is a simulated outbound voice-call prototype for a loan management company.

The application behaves as if an AI agent is calling a customer regarding their loan application. The customer/interviewer interacts with the AI agent using the laptop or browser microphone.

The prototype does **not** make real telephone calls and does not integrate with any telecom provider.

The system demonstrates:

- Conversational AI
- Large Language Model (LLM) based agent orchestration
- Speech-to-Text (STT)
- Text-to-Speech (TTS)
- Tool/function calling
- Conversation memory
- Customer intent recognition
- Backend API design using FastAPI
- Angular frontend architecture
- Error handling
- Financial-data guardrails
- Call transcript generation
- Call-summary generation
- Agent/debug activity visualization

The implementation intentionally focuses on a clean and functional prototype rather than production-scale infrastructure.

---

# 2. Goals

## Primary Goals

The system should allow an interviewer to:

1. Select a mock customer.
2. Start a simulated outbound call.
3. Hear the AI agent introduce itself.
4. Speak to the AI through the browser microphone.
5. Convert customer speech into text.
6. Send the customer message to the AI agent.
7. Allow the AI agent to determine the customer's intent.
8. Allow the agent to invoke backend tools when required.
9. Generate a natural-language response.
10. Convert the response to speech.
11. Play the response through the browser.
12. Display the conversation transcript.
13. Display agent/tool activity.
14. End the simulated call.
15. Generate a structured call summary.

## Secondary Goals

The prototype should also demonstrate:

- Conversation context
- Tool execution
- Financial-data safety
- Graceful failure handling
- Structured logging
- Automated testing
- Clear API boundaries
- Replaceable STT/TTS/LLM providers

---

# 3. Non-Goals

The following are intentionally outside the scope of this prototype:

- Real telephone calls
- Telecom provider integration
- Twilio integration
- Exotel integration
- Plivo integration
- Knowlarity integration
- Real Loan Management System integration
- Production authentication/authorization
- Production payment processing
- Real customer data
- Production-grade distributed infrastructure
- Kubernetes deployment
- Large-scale horizontal scaling

The system is strictly a simulated browser-based calling experience.

---

# 4. Technology Stack

## Backend

- Python
- FastAPI
- Pydantic
- Uvicorn
- HTTP/REST APIs
- Optional WebSocket communication

## AI

- LLM provider through an abstracted service layer
- Function/tool calling
- Structured agent state
- Intent detection

## Voice

- Speech-to-Text provider through an abstraction
- Text-to-Speech provider through an abstraction
- Browser microphone
- Browser audio playback

## Frontend

- Angular
- TypeScript
- Angular services
- Angular components
- Browser Media APIs

## Storage

The prototype can use:

- JSON mock data
- In-memory call state
- Local application state

A relational database is not required for the prototype.

---

# 5. High-Level Architecture

```text
                         ┌──────────────────────────┐
                         │      Angular UI          │
                         │                          │
                         │ Customer Selection       │
                         │ Calling Screen           │
                         │ Live Transcript          │
                         │ Agent Activity           │
                         │ Call Controls            │
                         │ Call Summary             │
                         └────────────┬─────────────┘
                                      │
                           HTTP / Optional WebSocket
                                      │
                                      ▼
                         ┌──────────────────────────┐
                         │      FastAPI Backend     │
                         │                          │
                         │ API Layer                │
                         │ Call Management           │
                         │ Agent Orchestration       │
                         │ Conversation State        │
                         │ Tool Execution            │
                         │ Voice Services            │
                         │ Transcript / Summary      │
                         └────────────┬─────────────┘
                                      │
                ┌─────────────────────┼─────────────────────┐
                │                     │                     │
                ▼                     ▼                     ▼
       ┌────────────────┐    ┌────────────────┐    ┌────────────────┐
       │ Speech-to-Text │    │      LLM       │    │ Text-to-Speech │
       │    Service     │    │     Agent      │    │    Service     │
       └────────────────┘    └───────┬────────┘    └────────────────┘
                                     │
                                     ▼
                            ┌──────────────────┐
                            │   Tool Router    │
                            └────────┬─────────┘
                                     │
                ┌────────────────────┼────────────────────┐
                │                    │                    │
                ▼                    ▼                    ▼
        ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
        │ Loan Tools   │     │Customer Tools│     │Support Tools │
        └──────┬───────┘     └──────┬───────┘     └──────┬───────┘
               │                    │                    │
               └────────────────────┼────────────────────┘
                                    ▼
                           ┌──────────────────┐
                           │   Mock Data      │
                           │ Customers / Loan │
                           └──────────────────┘
```

---

# 6. Frontend Architecture

The Angular application is responsible for the user-facing simulated call experience.

## Main Components

```text
frontend/
└── src/
    └── app/
        ├── components/
        │   ├── customer-selector/
        │   ├── call-screen/
        │   ├── call-header/
        │   ├── transcript/
        │   ├── agent-activity/
        │   ├── call-controls/
        │   └── call-summary/
        │
        ├── services/
        │   ├── customer.service.ts
        │   ├── call.service.ts
        │   ├── voice.service.ts
        │   └── websocket.service.ts
        │
        ├── models/
        │   ├── customer.ts
        │   ├── loan.ts
        │   ├── call.ts
        │   ├── transcript.ts
        │   └── agent-activity.ts
        │
        └── app.routes.ts
```

---

# 7. Customer Selection Flow

The application initially displays available mock customers.

Example:

```text
┌──────────────────────────────────────────────┐
│ Select Customer                              │
├──────────────────────────────────────────────┤
│                                              │
│ Rahul Sharma                                 │
│ Loan: LN1001                                 │
│ Status: Documents Pending                    │
│                                              │
│ Priya Das                                     │
│ Loan: LN1002                                 │
│ Status: Under Review                         │
│                                              │
│ Amit Patel                                    │
│ Loan: LN1003                                 │
│ Status: Approved                             │
│                                              │
│              [ Start Simulated Call ]        │
└──────────────────────────────────────────────┘
```

The customer selector calls:

```text
GET /api/customers
```

When a customer is selected, the frontend can retrieve additional information using:

```text
GET /api/customers/{customer_id}
```

---

# 8. Call State Machine

The simulated call follows a defined lifecycle.

```text
READY
  │
  │ Start Call
  ▼
CALLING
  │
  │ Connected
  ▼
CONNECTED
  │
  │ AI starts conversation
  ▼
CONVERSATION
  │
  │ End Call
  ▼
CALL_ENDED
```

The frontend uses the call state to control the UI.

## READY

The customer is selected but the call has not started.

Available action:

```text
Start Call
```

## CALLING

The application displays:

```text
Calling...
```

No real phone call is made.

## CONNECTED

The simulated call is considered connected.

The AI begins the conversation.

## CONVERSATION

The customer and AI exchange messages.

The UI displays:

- AI speaking indicator
- Customer speaking indicator
- Live transcript
- Tool activity
- Call timer

## CALL_ENDED

The conversation is stopped.

The frontend retrieves and displays the call summary.

---

# 9. Backend Architecture

The FastAPI backend is responsible for application orchestration.

```text
backend/
└── app/
    ├── main.py
    │
    ├── api/
    │   ├── customers.py
    │   ├── loans.py
    │   └── calls.py
    │
    ├── agent/
    │   ├── agent.py
    │   ├── prompts.py
    │   ├── state.py
    │   └── intent.py
    │
    ├── services/
    │   ├── llm_service.py
    │   ├── stt_service.py
    │   ├── tts_service.py
    │   └── summary_service.py
    │
    ├── tools/
    │   ├── loan_tools.py
    │   ├── customer_tools.py
    │   └── support_tools.py
    │
    ├── models/
    │   ├── customer.py
    │   ├── loan.py
    │   └── call.py
    │
    ├── core/
    │   ├── config.py
    │   └── logging.py
    │
    └── data/
```

---

# 10. API Layer

The API layer exposes the application functionality to Angular.

## Customer APIs

### GET /api/customers

Returns available mock customers.

### GET /api/customers/{customer_id}

Returns customer details.

---

# 11. Loan APIs

### GET /api/loans/{application_id}

Returns loan application information.

Financial information must originate from backend data rather than being generated by the LLM.

---

# 12. Call APIs

### POST /api/calls/start

Starts a simulated call.

Example request:

```json
{
  "customer_id": "CUST001"
}
```

Example response:

```json
{
  "call_id": "CALL-001",
  "customer_id": "CUST001",
  "status": "CONNECTED"
}
```

---

### POST /api/calls/{call_id}/message

Processes a customer message.

The request can contain either:

- Transcribed customer text
- Voice-derived text

Example:

```json
{
  "message": "Why is my loan still pending?"
}
```

The backend:

1. Adds the message to conversation state.
2. Sends the conversation to the agent.
3. Determines intent.
4. Determines whether a tool is required.
5. Executes the selected tool.
6. Provides the tool result to the LLM.
7. Generates the final response.
8. Adds the response to the transcript.
9. Returns the response and agent activity.

---

### POST /api/calls/{call_id}/end

Ends the simulated call.

The backend:

1. Stops the active conversation.
2. Calculates call duration.
3. Generates the final call summary.
4. Stores the final transcript and summary.

---

### GET /api/calls/{call_id}/transcript

Returns the complete conversation transcript.

---

### GET /api/calls/{call_id}/summary

Returns the structured call summary.

---

# 13. AI Agent Architecture

The AI agent is the central component of the application.

The agent should not operate as a hardcoded decision tree.

Instead, the agent uses:

```text
Customer Message
       │
       ▼
Conversation Context
       │
       ▼
LLM Agent
       │
       ├── Direct Response
       │
       └── Tool Call
               │
               ▼
          Tool Execution
               │
               ▼
          Tool Result
               │
               ▼
              LLM
               │
               ▼
        Final Response
```

---

# 14. Agent Decision Process

For each customer message:

```text
1. Receive customer message
2. Load current conversation state
3. Identify customer intent
4. Determine whether backend information is required
5. Select appropriate tool if necessary
6. Execute tool
7. Validate tool result
8. Provide result to LLM
9. Generate natural-language response
10. Store agent activity
11. Return response
```

The LLM is therefore responsible for deciding what action is appropriate rather than following a fixed conversation script.

---

# 15. Tool / Function Calling

The backend exposes tools to the AI agent.

At least three tools are required. The prototype implements the following tools.

## 15.1 get_loan_status

```text
get_loan_status(application_id)
```

Purpose:

Retrieve the current loan application status.

Example:

```json
{
  "application_id": "LN1001",
  "status": "DOCUMENTS_PENDING"
}
```

---

## 15.2 get_pending_documents

```text
get_pending_documents(application_id)
```

Purpose:

Retrieve documents that are still required.

Example:

```json
{
  "application_id": "LN1001",
  "pending_documents": [
    "Last 3 months bank statement",
    "Latest salary slip"
  ]
}
```

---

## 15.3 create_support_request

```text
create_support_request(customer_id, reason)
```

Purpose:

Create a support request when the customer has a complaint or issue that requires follow-up.

---

## 15.4 schedule_callback

```text
schedule_callback(customer_id, datetime)
```

Purpose:

Schedule a future callback requested by the customer.

---

## 15.5 get_customer_details

```text
get_customer_details(customer_id)
```

Purpose:

Retrieve customer information from backend data.

---

## 15.6 send_document_upload_link

```text
send_document_upload_link(customer_id)
```

Purpose:

Generate or return a mock document-upload link.

---

# 16. Financial Data Guardrail

The LLM must never invent financial or customer information.

The following information must come from backend tools or APIs:

- Loan status
- Loan amount
- Interest rate
- Approval status
- EMI
- Customer information
- Pending documents

Example:

```text
Customer:
"What is my loan status?"

Incorrect:
LLM invents the status.

Correct:

LLM
  ↓
get_loan_status()
  ↓
Backend data
  ↓
LLM
  ↓
Natural-language response
```

If the backend tool fails, the agent must not guess the answer.

Instead, it should explain that the information is currently unavailable and optionally create a follow-up request.

---

# 17. Conversation Memory

Each active call maintains its own conversation state.

Example:

```json
{
  "call_id": "CALL-001",
  "customer_id": "CUST001",
  "loan_application_id": "LN1001",
  "messages": [],
  "tool_calls": [],
  "detected_intents": [],
  "actions_taken": [],
  "callback_requested": false
}
```

Conversation history is provided to the agent so that references such as:

```text
Customer:
"What documents do I need?"

AI:
"You need your bank statement and latest salary slip."

Customer:
"How do I upload them?"
```

can be interpreted correctly.

In this example, "them" refers to the previously discussed pending documents.

---

# 18. Intent Recognition

The system recognizes customer intent.

Supported intents:

```text
LOAN_STATUS
DOCUMENT_REQUIREMENT
DOCUMENT_UPLOAD
CALLBACK_REQUEST
COMPLAINT
NOT_INTERESTED
WRONG_PERSON
GENERAL_QUERY
END_CALL
```

The detected intent is stored as part of the call activity and included in the final call summary.

---

# 19. Voice Processing Architecture

Voice processing is separated from the agent implementation.

```text
Browser Microphone
       │
       ▼
Audio Capture
       │
       ▼
Speech-to-Text Provider
       │
       ▼
Customer Text
       │
       ▼
AI Agent
       │
       ▼
AI Response Text
       │
       ▼
Text-to-Speech Provider
       │
       ▼
Browser Audio
```

---

# 20. Speech-to-Text Abstraction

The backend should expose an abstract STT interface.

Conceptually:

```text
STTProvider
     │
     └── Concrete STT implementation
```

Example interface:

```python
class STTProvider:
    async def transcribe(self, audio: bytes) -> str:
        ...
```

The agent should not depend directly on a specific STT vendor.

This allows the provider to be replaced later.

---

# 21. Text-to-Speech Abstraction

Similarly:

```text
TTSProvider
     │
     └── Concrete TTS implementation
```

Conceptually:

```python
class TTSProvider:
    async def synthesize(self, text: str) -> bytes:
        ...
```

The agent produces text, while the TTS service is responsible for converting the text into audio.

---

# 22. LLM Provider Abstraction

The LLM should also be isolated behind a service layer.

```text
Agent
  │
  ▼
LLMService
  │
  ▼
LLM Provider
```

The agent should not contain provider-specific implementation details.

This keeps:

- Agent logic
- Provider integration
- Configuration

separate.

---

# 23. Complete Voice Conversation Flow

The complete conversation looks like this:

```text
Customer speaks
      │
      ▼
Browser microphone
      │
      ▼
Speech-to-Text
      │
      ▼
Customer message
      │
      ▼
FastAPI
      │
      ▼
Conversation State
      │
      ▼
AI Agent
      │
      ├───────────────┐
      │               │
      │ No tool       │ Tool required
      │               │
      ▼               ▼
   Generate       Execute Tool
   response           │
      │               ▼
      │          Tool Result
      │               │
      └───────┬───────┘
              ▼
        Final LLM Response
              │
              ▼
        Transcript Update
              │
              ▼
        Text-to-Speech
              │
              ▼
        Browser Audio
```

---

# 24. Agent Activity

The frontend provides a developer/debug view.

Each interaction can expose:

```text
Customer Message
        ↓
Detected Intent
        ↓
Selected Tool
        ↓
Tool Arguments
        ↓
Tool Response
        ↓
Generated LLM Response
        ↓
Text-to-Speech
```

Example:

```text
CUSTOMER MESSAGE
"Why is my loan pending?"

INTENT
LOAN_STATUS

TOOL
get_loan_status

ARGUMENT
application_id = LN1001

TOOL RESPONSE
DOCUMENTS_PENDING

LLM RESPONSE
"Your application is currently pending because..."

TTS
Completed
```

This makes the agent's decision process observable during the interview demo.

---

# 25. Transcript Architecture

Every conversation event is stored in the call transcript.

Example:

```json
{
  "timestamp": "2026-10-05T10:00:01",
  "speaker": "customer",
  "type": "message",
  "content": "Why is my loan pending?"
}
```

Tool activity can be represented as:

```json
{
  "timestamp": "2026-10-05T10:00:02",
  "speaker": "agent",
  "type": "tool_call",
  "tool": "get_loan_status",
  "arguments": {
    "application_id": "LN1001"
  }
}
```

The final AI response can then be recorded:

```json
{
  "timestamp": "2026-10-05T10:00:03",
  "speaker": "ai",
  "type": "message",
  "content": "Your application is currently pending..."
}
```

---

# 26. Call Summary

When the call ends, the system generates a structured summary.

Example:

```json
{
  "customer_id": "CUST001",
  "application_id": "LN1001",
  "duration_seconds": 222,
  "primary_intent": "CALLBACK_REQUEST",
  "outcome": "CALLBACK_SCHEDULED",
  "summary": "Customer contacted regarding loan application status and requested a callback.",
  "sentiment": "NEUTRAL",
  "actions_taken": [
    "Retrieved loan status",
    "Retrieved pending documents",
    "Scheduled callback"
  ],
  "callback_requested": true
}
```

---

# 27. Mock Customer Data

The prototype contains at least three customers.

## Rahul Sharma

```text
Customer ID:
CUST001

Loan Application:
LN1001

Status:
DOCUMENTS_PENDING
```

Pending documents:

```text
Last 3 months bank statement
Latest salary slip
```

## Priya Das

```text
Customer ID:
CUST002

Loan Application:
LN1002

Status:
UNDER_REVIEW
```

## Amit Patel

```text
Customer ID:
CUST003

Loan Application:
LN1003

Status:
APPROVED
```

These customers are intentionally configured with different loan states so that they can drive different conversation paths.

---

# 28. Example Conversation

## Scenario: Rahul — Documents Pending

### AI

> Hello Rahul. This is an AI assistant calling on behalf of ABC Finance regarding your loan application. Is this a good time to talk?

### Customer

> Yes. Why is my loan still pending?

### Agent

```text
Intent:
LOAN_STATUS

Tool:
get_loan_status(LN1001)
```

### Tool Result

```text
DOCUMENTS_PENDING
```

### AI

> Your application is currently pending because some documents are still required.

### Customer

> What documents do you need?

### Agent

```text
Intent:
DOCUMENT_REQUIREMENT

Tool:
get_pending_documents(LN1001)
```

### Tool Result

```text
Last 3 months bank statement
Latest salary slip
```

### AI

> We still need your last three months of bank statements and your latest salary slip.

### Customer

> How can I upload them?

### Agent

```text
Intent:
DOCUMENT_UPLOAD

Tool:
send_document_upload_link(CUST001)
```

### AI

> I can provide you with the document upload link.

This demonstrates:

- Conversation understanding
- Context
- Intent detection
- Tool calling
- Backend data retrieval
- Natural-language generation
- Voice interaction

---

# 29. Error Handling

The application should gracefully handle failures.

## Microphone Failure

If microphone access is unavailable:

```text
Microphone access is unavailable.
Please allow microphone access and try again.
```

## Speech Recognition Failure

```text
I couldn't understand that.
Could you please repeat?
```

## LLM Failure

```text
I'm having trouble processing your request right now.
Please try again.
```

## TTS Failure

If speech generation fails, the text response should still be displayed.

## Tool Failure

If a backend lookup fails:

```text
I'm unable to retrieve that information right now.
I can create a follow-up request if you'd like.
```

The agent must never invent missing information.

## Customer Not Found

The backend should return an appropriate error rather than allowing the agent to continue with incorrect customer information.

## Loan Not Found

The agent should explain that the application information is currently unavailable.

---

# 30. Guardrails

The AI agent must follow these rules.

## Never Request Sensitive Authentication Information

The AI must never request:

- OTP
- PIN
- Password
- CVV
- Full card information

## Never Invent Financial Information

The AI must not invent:

- Loan status
- Loan amount
- Interest rate
- EMI
- Approval status
- Customer details
- Pending documents

## Backend Is the Source of Truth

Important financial information must come from backend tools or APIs.

---

# 31. Call Controls

The Angular UI provides:

```text
Start Call
Mute
End Call
```

Optional controls may include:

```text
Pause AI
Restart Conversation
Change Customer
```

The basic controls have priority over optional controls.

---

# 32. Optional Real-Time Communication

The initial implementation can use HTTP APIs.

For example:

```text
POST /api/calls/{call_id}/message
```

A WebSocket layer may be added later for real-time updates.

Potential architecture:

```text
Angular
   │
   │ WebSocket
   ▼
FastAPI
   │
   ├── Transcript Events
   ├── Agent Events
   ├── Tool Events
   └── Voice Events
```

WebSocket communication is treated as an enhancement rather than a prerequisite for the core prototype.

---

# 33. Optional Barge-In Handling

A future enhancement is interruption detection.

Expected behavior:

```text
AI is speaking
      │
      ▼
Customer starts speaking
      │
      ▼
Detect interruption
      │
      ▼
Stop/pause AI audio
      │
      ▼
Process customer message
```

This feature is considered optional/bonus and should only be implemented after the core voice flow is stable.

---

# 34. Data Flow

## Starting a Call

```text
Angular
   │
   │ POST /api/calls/start
   ▼
FastAPI
   │
   ├── Validate customer
   ├── Create call state
   └── Return call ID
   │
   ▼
Angular
   │
   ▼
Connected UI
```

## Processing Customer Speech

```text
Microphone
   │
   ▼
STT
   │
   ▼
Customer Text
   │
   ▼
POST /api/calls/{id}/message
   │
   ▼
Agent
   │
   ├── Intent
   ├── Tool
   ├── Tool Result
   └── LLM Response
   │
   ▼
TTS
   │
   ▼
Audio
```

## Ending a Call

```text
Angular
   │
   │ POST /api/calls/{id}/end
   ▼
FastAPI
   │
   ├── Stop call
   ├── Finalize transcript
   ├── Generate summary
   └── Calculate duration
   │
   ▼
Call Summary
```

---

# 35. Repository Structure

The planned repository structure is:

```text
ai-voice-calling-agent/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── calls.py
│   │   │   ├── customers.py
│   │   │   └── loans.py
│   │   │
│   │   ├── agent/
│   │   │   ├── agent.py
│   │   │   ├── intent.py
│   │   │   ├── prompts.py
│   │   │   └── state.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── logging.py
│   │   │
│   │   ├── models/
│   │   │   ├── call.py
│   │   │   ├── customer.py
│   │   │   └── loan.py
│   │   │
│   │   ├── services/
│   │   │   ├── llm_service.py
│   │   │   ├── stt_service.py
│   │   │   ├── summary_service.py
│   │   │   └── tts_service.py
│   │   │
│   │   ├── tools/
│   │   │   ├── customer_tools.py
│   │   │   ├── loan_tools.py
│   │   │   └── support_tools.py
│   │   │
│   │   └── main.py
│   │
│   ├── data/
│   │   └── customers.json
│   │
│   ├── tests/
│   │   ├── test_api.py
│   │   ├── test_tools.py
│   │   └── test_agent.py
│   │
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   └── app/
│   │
│   ├── angular.json
│   ├── package.json
│   └── README.md
│
├── docs/
│   ├── architecture.md
│   ├── api.md
│   └── demo.md
│
├── .env.example
├── .gitignore
└── README.md
```

---

# 36. Testing Strategy

Testing will be implemented at multiple levels.

## Unit Tests

Tools:

```text
get_loan_status
get_pending_documents
create_support_request
schedule_callback
get_customer_details
send_document_upload_link
```

## Agent Tests

Test scenarios include:

```text
LOAN_STATUS
DOCUMENT_REQUIREMENT
DOCUMENT_UPLOAD
CALLBACK_REQUEST
COMPLAINT
NOT_INTERESTED
WRONG_PERSON
GENERAL_QUERY
END_CALL
```

## API Tests

The following endpoints should be covered:

```text
GET /api/customers
GET /api/customers/{customer_id}
GET /api/loans/{application_id}

POST /api/calls/start
POST /api/calls/{call_id}/message
POST /api/calls/{call_id}/end

GET /api/calls/{call_id}/transcript
GET /api/calls/{call_id}/summary
```

## Error Tests

Test:

```text
Unknown customer
Unknown loan
Tool failure
LLM failure
STT failure
TTS failure
Invalid call ID
Empty message
Microphone unavailable
```

---

# 37. Logging

Structured application logging should capture useful events such as:

```text
CALL_STARTED
CUSTOMER_MESSAGE
INTENT_DETECTED
TOOL_CALLED
TOOL_COMPLETED
LLM_RESPONSE
TTS_STARTED
TTS_COMPLETED
CALL_ENDED
CALL_SUMMARY_GENERATED
ERROR
```

Logs should not contain sensitive information unnecessarily.

---

# 38. Configuration

Configuration is provided through environment variables.

Example:

```text
APP_NAME
APP_ENV
LOG_LEVEL

LLM_PROVIDER
LLM_API_KEY
LLM_MODEL

STT_PROVIDER

TTS_PROVIDER

FRONTEND_URL
```

Secrets are stored locally in `.env` and are never committed to Git.

`.env.example` documents the required configuration without containing credentials.

---

# 39. Security Considerations

Although this is a prototype, the application follows basic security practices:

- API keys are not committed to Git.
- Sensitive credentials are loaded from environment variables.
- Mock customer data is used.
- No real financial information is stored.
- No real phone calls are made.
- No payment information is processed.
- The AI does not request OTP/PIN/password/CVV information.

---

# 40. Performance and Latency

The application should measure important stages where practical:

```text
STT latency
LLM latency
Tool execution latency
TTS latency
Total response latency
```

Example:

```text
Customer speech
      │
      ├── STT: 850 ms
      ├── LLM: 1200 ms
      ├── Tool: 80 ms
      └── TTS: 700 ms
```

Latency measurement is useful for evaluating the voice experience but is not required for the core prototype.

---

# 41. Future Enhancements

Potential future improvements include:

- WebSocket-based streaming
- Real-time audio streaming
- Barge-in detection
- Hindi + English conversation
- Automatic language switching
- Conversation replay
- PostgreSQL persistence
- Authentication
- Production-grade observability
- Docker deployment
- Distributed architecture
- Real Loan Management System integration
- Real telecom integration

These enhancements are intentionally separated from the core prototype so that they do not compromise delivery of the required functionality.

---

# 42. Demonstration Flow

The recommended recruiter demonstration is:

```text
1. Open Angular application
       ↓
2. Select Rahul Sharma
       ↓
3. Start Simulated Call
       ↓
4. AI introduces itself
       ↓
5. Customer asks:
   "Why is my loan still pending?"
       ↓
6. Agent detects:
   LOAN_STATUS
       ↓
7. Agent calls:
   get_loan_status()
       ↓
8. Agent responds using backend result
       ↓
9. Customer asks:
   "What documents do I need?"
       ↓
10. Agent calls:
    get_pending_documents()
       ↓
11. Customer asks:
    "How do I upload them?"
       ↓
12. Agent calls:
    send_document_upload_link()
       ↓
13. Customer requests callback
       ↓
14. Agent calls:
    schedule_callback()
       ↓
15. End Call
       ↓
16. Display transcript
       ↓
17. Display structured call summary
```

This single demonstration exercises the core architecture:

```text
Voice
+
STT
+
LLM
+
Intent
+
Memory
+
Tool Calling
+
TTS
+
Transcript
+
Summary
+
Angular
+
FastAPI
```

---

# 43. Engineering Principles

The implementation follows these principles:

## Separation of Concerns

Frontend, API, agent, tools, and external providers remain separate.

## Provider Abstraction

LLM, STT, and TTS providers are accessed through service abstractions.

## Backend as Source of Truth

Financial/customer information comes from backend tools rather than LLM-generated facts.

## Observable Agent

Agent decisions and tool activity are exposed through the debug/activity panel.

## Graceful Failure

External service failures should not crash the simulated call.

## Simple Prototype Architecture

The implementation avoids unnecessary infrastructure while demonstrating the required engineering concepts.

## Testability

Core business logic and API behavior are separated so that they can be tested independently.

---

# 44. Definition of Done

The prototype is considered complete when:

- [ ] Angular application starts successfully.
- [ ] FastAPI backend starts successfully.
- [ ] Customer selection works.
- [ ] Simulated call can be started.
- [ ] AI introduction is played.
- [ ] Browser microphone input works.
- [ ] Customer speech is transcribed.
- [ ] LLM agent processes the conversation.
- [ ] At least three backend tools work.
- [ ] Conversation memory works.
- [ ] Intent detection works.
- [ ] AI response is converted to speech.
- [ ] Live transcript is displayed.
- [ ] Agent activity is displayed.
- [ ] Call can be muted.
- [ ] Call can be ended.
- [ ] Call summary is generated.
- [ ] Guardrails are implemented.
- [ ] Error handling is implemented.
- [ ] Mock customers are available.
- [ ] Unit tests pass.
- [ ] Integration/API tests pass.
- [ ] README is complete.
- [ ] Architecture documentation is complete.
- [ ] API documentation is complete.
- [ ] Sample transcript exists.
- [ ] Sample call summary exists.
- [ ] Local setup instructions work from a clean checkout.
- [ ] Git repository contains clean, meaningful commits.

---

# 45. Conclusion

The AI Voice Calling Agent is designed as a focused prototype demonstrating how conversational AI, voice technologies, LLM agents, backend tools, and frontend interfaces can be combined into a simulated customer-service calling workflow.

The architecture prioritizes:

```text
Functional Voice Experience
        +
Real Agent Decision Making
        +
Tool Calling
        +
Conversation Memory
        +
Strong Backend Design
        +
Clear Frontend UX
        +
Safety / Guardrails
        +
Testing / Documentation
```

The implementation intentionally avoids unnecessary production infrastructure and focuses on demonstrating sound engineering decisions within the scope of the assignment.