def build_prompt(user_query, clauses):
    return f"""
You're an insurance policy decision assistant. Given the following:

**User Query:** {user_query}

**Relevant Policy Clauses:**
{'\n'.join(clauses)}

Answer these questions:
1. Is the request approved or rejected?
2. If approved, mention the payout amount.
3. Justify your decision based on clauses.

Respond in JSON:
{{
  "decision": "...",
  "amount": "...",
  "justification": "..."
}}
"""
