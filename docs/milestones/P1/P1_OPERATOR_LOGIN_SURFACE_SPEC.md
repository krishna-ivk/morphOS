# P1 Operator Login Surface Spec

## Purpose

Define the first production login surface for `skyforce-command-centre-live` so the
operator console has a real entry gate before broader deployment.

This is intentionally narrow. It does not attempt to solve full identity federation.
It establishes a concrete operator sign-in experience, a session model, and the
minimum runtime behaviors needed to protect the Live operator console.

## Goals

- present a distinctive, system-console-style login screen that matches the Command
  Centre visual language
- gate the Live dashboard and issue-detail views behind an explicit operator login
- keep the first implementation simple enough for local and early production use
- preserve the existing operator concepts already present in the platform:
  `operator_identity`, `operator_role`, and `workspace_id`
- keep the primary action visually aligned with the existing bright button treatment

## Non-Goals

- SSO, OAuth, SAML, or external IdP integration
- multi-factor authentication
- password reset or user self-service
- long-term secrets management design
- full RBAC administration UI

## Visual Direction

The login surface should feel like a secure command console rather than a generic
web login form.

### Required characteristics

- black or near-black background
- soft gray monospace system text
- one strong white primary action button
- dark rounded input surfaces consistent with the existing dashboard controls
- generous vertical spacing and a centered mobile-friendly layout

### Required copy

- title: `SKYFORCE`
- subtitle: `Command Centre Live v1.0`
- system notice: `Operator authentication required.`
- status chip: `CONTROL PLANE: ONLINE`
- field label: `OPERATOR ID`
- field label: `ACCESS KEY`
- primary action: `ENTER COMMAND CENTRE`
- trust line: `Authorized operators only. Audit trail active.`

### Optional secondary copy

- `Workspace defaults will apply after sign-in.`
- `Secure operator access required.`

## Interaction Model

### Inputs

The first login screen should require:

- `operator_identity`
- `access_key`

The first login screen may omit free-form `role` and `workspace` entry if those can
be derived from defaults or session rules after sign-in.

## Session Model

Successful login must create a browser session containing:

- `authenticated_operator = true`
- `operator_identity`
- `operator_role`
- `workspace_id`

The first implementation may set:

- default role: `operator`
- default workspace: `workspace-default`

Those defaults must be overridable by environment or future admin policy.

## Auth Boundary

### Protected surfaces

The following Live routes must require authentication:

- `/`
- `/issues/:issue`

### Public surfaces

The following routes remain public:

- `/health`
- `/login`
- `POST /login`

### Redirect behavior

- unauthenticated access to protected routes must redirect to `/login`
- authenticated access to `/login` should redirect to `/`

## Credential Validation

The first implementation may validate a single shared operator access key from
runtime configuration.

The preferred next step is a small operator registry that maps:

- `operator_identity`
- `access_key`
- `role`
- `workspace_id`

This allows different operators to sign in with different default authority
postures without changing the login screen shape.

### Minimum runtime config

- `SKYFORCE_OPERATOR_ACCESS_KEY`
- `SKYFORCE_DEFAULT_OPERATOR_ROLE`
- `SKYFORCE_DEFAULT_WORKSPACE_ID`
- `SKYFORCE_OPERATOR_REGISTRY_JSON` (optional registry override for per-operator
  role and workspace defaults)

If unset, safe local defaults may exist for development, but production deployment
must provide the access key explicitly.

## Trust Boundary

The login surface is only one layer of authority. The backend must also know when
to trust operator context and when to reject it.

### Development posture

For local development, the system may accept operator context from ordinary request
headers after the operator has signed in through the Live UI.

This is acceptable for local proving runs and operator iteration, but it should be
treated explicitly as development posture rather than strong production trust.

### Production posture

For production use, the preferred posture is:

- Live UI creates a session-backed operator context
- Live UI signs operator claims for write actions
- backend verifies the signed claim before trusting:
  - `operator_identity`
  - `operator_role`
  - `workspace_id`

### Production trust config

- `SKYFORCE_OPERATOR_CLAIM_SECRET`

When this shared secret is configured, write paths should prefer signed operator
claims over unauthenticated raw headers.

## Authority Responsibility Split

### `skyforce-command-centre-live`

- presents the login surface
- establishes browser session state
- carries operator identity, role, and workspace through navigation
- signs write-context claims when the shared secret is configured

### `skyforce-api-gateway`

- verifies signed claims when production trust mode is enabled
- enforces role checks on write actions
- applies workspace scoping to relevant operator reads and writes

The backend remains the final authority for whether an action is permitted.

## Operator Context After Login

After authentication, the operator must still be able to see and understand the
active session context:

- operator identity
- role
- workspace

The dashboard and issue pages should display this clearly near the top of the page.

## Button and Control Rules

- the primary button must remain visually consistent with the existing bright CTA
  style already used for main actions
- secondary actions, if added, should use ghost or outline styling
- the login form should avoid extra buttons or links unless they are essential

## Error Handling

On failed login:

- do not leak whether the operator id or access key was wrong
- show one concise message:
  - `Invalid credentials or insufficient authority.`

## Logout

The first implementation should include a basic logout path that:

- clears the operator session
- returns the user to `/login`

## Deployment Readiness Requirements

Before general internal rollout, the login surface must support:

- session-backed route protection
- backend-visible operator identity fields
- operator identity continuity across refresh and Live navigation
- compatibility with the existing operator-scope and workspace-scope model
- signed-claim support for production write authority
- a clearly documented difference between development fallback trust and production trust posture

## Acceptance Criteria

The feature is acceptable when all are true:

1. An unauthenticated operator opening `/` is redirected to `/login`.
2. The login page renders the required copy and the white primary button.
3. A valid login stores operator session state and redirects to `/`.
4. Dashboard and issue routes remain accessible after sign-in.
5. The dashboard and issue pages visibly show the active operator scope.
6. Logout clears the session and returns the operator to `/login`.
7. Production deployments can enable signed operator-claim verification for write actions.
