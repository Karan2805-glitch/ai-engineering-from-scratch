---
name: prompt-api-troubleshooter
description: Diagnose and resolve common LLM API errors, including authentication failures, rate limits, malformed requests, and network issues.
phase: 0
lesson: 4
---

# LLM API Troubleshooting Guide

## Purpose

Diagnose common errors when communicating with large language model APIs. Identify the likely cause using the HTTP status code, error response, request configuration, and provider documentation.

## Common HTTP Errors

### 401 Unauthorized

**Meaning:** Authentication failed.

**Possible causes:**
- API key is missing or invalid.
- The environment variable contains an incorrect value.
- The application is loading the wrong environment configuration.

**How to troubleshoot:**
1. Check that the expected environment variable exists without printing its value.
2. Verify that the key belongs to the intended provider.
3. Confirm that the application loads the correct `.env` file.
4. Test using a newly generated key only if necessary.

**Example:** A request using `invalid_test_key` returned HTTP 401 with the error code `invalid_api_key`.

### 403 Forbidden

**Meaning:** The request was refused.

**Possible causes:**
- The account or key lacks permission for the requested resource.
- A security gateway or network filter blocks the request.
- The provider applies access restrictions.

**How to troubleshoot:**
1. Read the error body for additional details.
2. Check the provider's account and model-access requirements.
3. Compare the SDK request with the raw HTTP request.
4. Investigate network or gateway restrictions when indicated by the response.

**Example:** A raw HTTP request returned HTTP 403 with Cloudflare error 1010. Adding a descriptive User-Agent was followed by a successful request. This was an observed result, not proof that the User-Agent was the only cause.

### 400 Bad Request

**Meaning:** The server could not accept the request as submitted.

**Possible causes:**
- Incorrect JSON structure.
- Missing required fields.
- Unsupported model name or parameter.
- Invalid message format.

**How to troubleshoot:**
1. Validate the request body.
2. Check the provider's current API documentation.
3. Verify the model identifier and supported parameters.
4. Read the response body for the specific validation error.

### 429 Too Many Requests

**Meaning:** The request exceeded a rate limit or quota restriction.

**How to troubleshoot:**
1. Read the provider's error message.
2. Check rate-limit headers and account usage.
3. Reduce request frequency.
4. Retry after the indicated delay, using exponential backoff where appropriate.
5. Check whether the account has exhausted its available quota.

Do not assume every 429 error will resolve by waiting; some quota restrictions require an account or usage-limit change.

### 500, 502, or 503 Server Errors

**Meaning:** The service or an intermediary encountered a server-side problem.

**How to troubleshoot:**
1. Check the provider's service-status page.
2. Retry after a short delay.
3. Use bounded retries with exponential backoff for temporary failures.
4. Avoid retrying indefinitely.

### Timeout or Connection Error

**Meaning:** The request did not complete successfully because of a timeout or connectivity issue.

**How to troubleshoot:**
1. Check network connectivity.
2. Verify the API endpoint.
3. Set a reasonable request timeout.
4. Retry transient failures cautiously.
5. Check whether a proxy, firewall, or VPN affects the connection.

## Secure Diagnostic Practices

- Store API keys in environment variables or an ignored `.env` file.
- Never hardcode secrets in source code.
- Never print, paste, or commit API keys.
- Verify that `.env` is ignored by Git using:

  `git check-ignore -v .env`

- Check whether a file is already tracked using:

  `git ls-files --error-unmatch .env`

- Avoid commands that print API key values to the terminal or logs.
- Never share complete request headers when they contain credentials.
- Redact secrets before sharing error logs.

## SDK Versus Raw HTTP

An SDK simplifies API calls by handling request construction, serialization, response parsing, and other implementation details.

Raw HTTP exposes these details directly. It is useful for understanding authentication headers, JSON payloads, HTTP status codes, and provider responses.

When an SDK succeeds but a raw HTTP request fails, compare:

1. The endpoint URL.
2. Authentication headers.
3. Request body and parameter names.
4. Model identifier.
5. HTTP status and error body.
6. Differences in network or gateway handling.

Do not assume the API key is incorrect simply because one implementation fails.

## Diagnostic Workflow

1. Identify the provider and endpoint.
2. Capture the HTTP status code and sanitized error body.
3. Check that the required environment variable is set without revealing its value.
4. Validate the endpoint, model identifier, headers, and request body.
5. Compare SDK and raw HTTP behavior when useful.
6. Consult the provider's documentation for the specific error.
7. Apply the smallest justified fix.
8. Retry and verify the result.

## Lessons Learned

During this exercise:

- A Groq SDK request successfully generated a model response.
- A raw HTTP request initially returned HTTP 403 with error 1010.
- After adding a descriptive User-Agent, the raw HTTP request succeeded.
- A deliberately invalid API key produced HTTP 401 with error code `invalid_api_key`.
- Both SDK and raw HTTP approaches returned generated text and token-usage information.

These results demonstrate why inspecting the actual error response is more reliable than guessing at the cause.