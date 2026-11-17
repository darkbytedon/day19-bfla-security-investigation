# Day 19: Broken Function Level Authorization (BFLA) Security Investigation

## 1. Objective

Investigate Broken Function Level Authorization (BFLA), demonstrate unauthorized access to an administrative API function, implement authorization controls, and verify the security improvements.

## 2. Vulnerability Identified

The original `POST /api/admin/create-user` endpoint allowed requests to create users without verifying whether the requester had administrative privileges.

An unauthorized request returned `201 Created`, demonstrating that the administrative function could be executed without proper authorization.

## 3. Security Risks

An attacker could potentially:
- Create unauthorized accounts.
- Abuse administrative functionality.
- Escalate privileges if additional administrative functions were similarly exposed.
- Compromise the application's integrity.

## 4. Remediation Implemented

The application was improved using:

- Password hashing with Werkzeug.
- Session-based authentication.
- Server-side role verification.
- Authentication checks returning `401 Unauthorized`.
- Authorization checks returning `403 Forbidden`.
- Secure, HttpOnly and SameSite cookie settings.
- A configured 30-minute permanent session lifetime.
- Logout functionality that clears the session cookie.

## 5. Security Test Results

| Test | Expected result | Actual result |
|---|---|---|
| Unauthenticated administrative request | 401 | 401 |
| Alice (user) creates account | 403 | 403 |
| Bob (support) creates account | 403 | 403 |
| Admin creates account | 201 | 201 |
| Incorrect login password | 401 | 401 |
| Access after logout | 401 | 401 |

All six checks produced the expected results.

## 6. Important Security Considerations

The application uses Flask's default client-side signed sessions. The session cookie is signed, not encrypted. Clearing the cookie during logout does not automatically revoke a previously copied cookie.

Production systems should consider server-side session storage and session revocation, CSRF protection, HTTPS, rate limiting, persistent user storage, and secure secret management.

Flask debug mode must also be disabled in production.

## 7. Conclusion

The investigation demonstrated how missing function-level authorization can expose administrative API functionality.

After implementing session-based authentication and server-side role checks, unauthorized users were prevented from executing the administrative function.

This exercise improved my practical understanding of authentication, authorization, role-based access control, session management, API security testing, and BFLA remediation.

**Day 19 status: Practical investigation and six security checks completed.**
