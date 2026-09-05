# Network segmentation diagram: visual transcription

- **Source path (repository-relative):** `Hackathon/5. Infrastructure_internal info/network-segmentation-diagram.png`
- **Source locator:** entire standalone PNG, 1700 x 1275 pixels; matching diagram also visually reviewed on page 1, Figure 1 of `Hackathon/5. Infrastructure_internal info/network_architecture_diagrams.pdf`.
- **Evidence status:** illustrative reference template. This status comes from the accompanying PDF's page 2 note, not from text within the standalone PNG.

## Literal visual text

| Visual location | Literal text |
|---|---|
| Top box | `Users / clients` |
| Edge box | `CDN + WAF`; `TLS termination, DDoS filtering` |
| Outer boundary | `VPC`; `Isolated network, multi-AZ` |
| Upper box within VPC | `Public subnet`; `Load balancer (TLS termination)` |
| Dashed boundary annotation | `Security groups enforce isolation` |
| Lower-left box | `Application tier`; `App servers, API, IAM/SSO` |
| Lower-right box | `Data tier`; `Isolated; encrypted at rest` |

## Visual structure (description)

The outer VPC boundary encloses the public subnet, application tier, and data tier. The image shows a downward arrow from users to CDN/WAF, a connector from CDN/WAF to the VPC's upper boundary, a downward arrow from the public subnet to the application tier, and a rightward arrow from the application tier to the data tier. A dashed horizontal line below the public subnet carries the security-group annotation. The CDN/WAF connector stops at the VPC boundary; it is not drawn continuously to the public-subnet box.

## Interpretation and limits

The depicted design separates public ingress, application, and data components. It is not evidence that a particular company has deployed these controls. No cloud provider, load-balancer product, database product, cipher, TLS version, replication mode, network ACL, IP addressing, security-group rule, or questionnaire mapping is specified. In particular, `AES-256`, `AWS`, `RDS`, `S3`, `TLS 1.2+`, and active replication are not literal diagram claims.

Accompanying PDF, page 2, literal note:

> Note: these are illustrative templates. For an actual SOC 2 engagement, the diagram must match the real configuration (security group rules, IAM policies, log retention settings) and that configuration is what auditors will test against.
