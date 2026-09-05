# B2B SaaS network architecture: reference PDF transcription

- **Source path (repository-relative):** `Hackathon/5. Infrastructure_internal info/network_architecture_diagrams.pdf`
- **Source locator:** all 2 PDF pages, including both embedded diagrams and the page 2 note; pages rendered and visually inspected.
- **Evidence status:** illustrative templates, explicitly stated by the source. This is not an auditor attestation or verified production configuration.
- **Transcription convention:** prose below is literal source text with line wrapping normalized. Diagram labels are literal; descriptions of geometry are separately labelled.

## Page 1: literal text

B2B SaaS network architecture

Illustrative reference diagrams — network segmentation and administrative access, annotated for SOC 2 review

### 1. Network segmentation and data flow

Shows the path from external users through the CDN/WAF into the VPC, and the segmentation between the public subnet, application tier, and data tier. Highlights TLS in transit, security-group boundaries between tiers, and encryption at rest on the data tier.

### Figure 1: literal visual labels

| Visual location | Literal text |
|---|---|
| Top box | `Users / clients` |
| Edge box | `CDN + WAF`; `TLS termination, DDoS filtering` |
| Outer boundary | `VPC`; `Isolated network, multi-AZ` |
| Upper box within VPC | `Public subnet`; `Load balancer (TLS termination)` |
| Dashed boundary annotation | `Security groups enforce isolation` |
| Lower-left box | `Application tier`; `App servers, API, IAM/SSO` |
| Lower-right box | `Data tier`; `Isolated; encrypted at rest` |

**Visual structure (description):** The outer VPC boundary encloses the public subnet, application tier, and data tier. The image shows a downward arrow from users to CDN/WAF, a connector from CDN/WAF to the VPC's upper boundary, a downward arrow from the public subnet to the application tier, and a rightward arrow from the application tier to the data tier. A dashed horizontal line below the public subnet carries the security-group annotation. The CDN/WAF connector stops at the VPC boundary; it is not drawn continuously to the public-subnet box.

**Literal caption:** Figure 1: Network segmentation and data flow

### 2. Administrative access and logging

Shows the privileged-access path into production (MFA, VPN gateway, bastion host) and the logging path from production into a centralized SIEM for retention and alerting.

## Page 2: Figure 2 literal visual labels

| Visual location | Literal text |
|---|---|
| Top box | `Admin / engineer` |
| First downward arrow annotation | `MFA-verified login` |
| Second box | `VPN gateway`; `Enforces MFA, IP allow-list` |
| Third box | `Bastion host`; `Audited, ephemeral SSH access` |
| Lower-left box | `Production environment`; `App + data tiers (VPC)` |
| Lower-right box | `Centralized logging`; `SIEM, alerting, retention` |

**Visual structure (description):** The downward arrow sequence is Admin / engineer -> VPN gateway -> Bastion host -> Production environment. A rightward arrow leads from Production environment to Centralized logging.

**Literal caption:** Figure 2: Administrative access and logging

**Literal note:**

> Note: these are illustrative templates. For an actual SOC 2 engagement, the diagram must match the real configuration (security group rules, IAM policies, log retention settings) and that configuration is what auditors will test against.

## Interpretation and limits

The source describes reference designs for SOC 2 review. It names no organization, cloud vendor, cipher, TLS version, specific firewall rule, logging product, or retention period. The SIEM is part of the template depiction; it does not establish an active deployment or a roadmap commitment. Assess actual configuration against separate operational evidence.
