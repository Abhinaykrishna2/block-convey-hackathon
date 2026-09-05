# Administrative access and logging diagram: visual transcription

- **Source path (repository-relative):** `Hackathon/5. Infrastructure_internal info/admin-access-logging-diagram.png`
- **Source locator:** entire standalone PNG, 1700 x 845 pixels; matching diagram also visually reviewed on page 2, Figure 2 of `Hackathon/5. Infrastructure_internal info/network_architecture_diagrams.pdf`.
- **Evidence status:** illustrative reference template. This status comes from the accompanying PDF's page 2 note, not from text within the standalone PNG.

## Literal visual text

| Visual location | Literal text |
|---|---|
| Top box | `Admin / engineer` |
| First downward arrow annotation | `MFA-verified login` |
| Second box | `VPN gateway`; `Enforces MFA, IP allow-list` |
| Third box | `Bastion host`; `Audited, ephemeral SSH access` |
| Lower-left box | `Production environment`; `App + data tiers (VPC)` |
| Lower-right box | `Centralized logging`; `SIEM, alerting, retention` |

## Visual structure (description)

The downward arrow sequence is Admin / engineer -> VPN gateway -> Bastion host -> Production environment. A rightward arrow leads from Production environment to Centralized logging.

## Interpretation and limits

The arrows depict an administrative access path and a logging destination. They do not prove deployed MFA enforcement, specific approved users or IP ranges, exclusive bastion routing, prohibition of static SSH keys, recording of every command, a retention duration, or operation of a SIEM. No cloud provider or logging product is named. `Audited, ephemeral SSH access` does not specify how access expires or what audit records are collected.

The template's SIEM label alone cannot establish either a current implementation or a committed roadmap; a comparison with operational policy must keep the sources' different evidentiary status explicit.

Accompanying PDF, page 2, literal note:

> Note: these are illustrative templates. For an actual SOC 2 engagement, the diagram must match the real configuration (security group rules, IAM policies, log retention settings) and that configuration is what auditors will test against.
