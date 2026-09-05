# Regodit_cryptography_policy_v1.0

Source: `Hackathon/2. Company policies/Regodit_cryptography_policy_v1.0.docx`
Source SHA-256: `17fb7a83fb360c4543beb42457e036e7246e6c3fc6b1bd44a9f27a350a7180fe`
Document role: `documented_policy`

The text below records source statements. Policy requirements, template text, and requested actions are not proof of implementation or completion.

<!-- evidence:ef4ba71bcdcd348a93baf002 source:word/document.xml#p00001 -->
Cryptography Policy

<!-- evidence:2d8718c3efc9348051b6b21a source:word/document.xml#p00002 -->
Solsphere AI Inc.| Regodit

<!-- evidence:7cdcc61c3ebb8c9f64200b43 source:word/document.xml#p00003 | table 1, XML row 1, XML cell 1 -->
Document Title

<!-- evidence:67a0f55cc1627f4835945c14 source:word/document.xml#p00004 | table 1, XML row 1, XML cell 2 -->
Cryptography Policy

<!-- evidence:c6c2ded9362e02f9b6df916a source:word/document.xml#p00005 | table 1, XML row 2, XML cell 1 -->
Document Owner

<!-- evidence:26cd4daaadbf45dc3581595c source:word/document.xml#p00006 | table 1, XML row 2, XML cell 2 -->
Sahil Pugalia

<!-- evidence:65fb0dd5eade6cf6c864564c source:word/document.xml#p00007 | table 1, XML row 3, XML cell 1 -->
Approved By

<!-- evidence:44ea06b7f7514cc710badc02 source:word/document.xml#p00008 | table 1, XML row 3, XML cell 2 -->
Priyanka Choudhury

<!-- evidence:3140d48725e9b22f4a95f47f source:word/document.xml#p00009 | table 1, XML row 4, XML cell 1 -->
Classification

<!-- evidence:cf92a49c031aa030be50cff6 source:word/document.xml#p00010 | table 1, XML row 4, XML cell 2 -->
Internal / Confidential

<!-- evidence:e60b86f961f1294b64ddd5c6 source:word/document.xml#p00011 | table 1, XML row 5, XML cell 1 -->
Effective Date

<!-- evidence:ebf4de0396d29a43fff59d00 source:word/document.xml#p00012 | table 1, XML row 5, XML cell 2 -->
14 July 2026

<!-- evidence:876fa70820593c6398b29d73 source:word/document.xml#p00013 | table 1, XML row 6, XML cell 1 -->
Review Cycle

<!-- evidence:540f69f08154a812313137c6 source:word/document.xml#p00014 | table 1, XML row 6, XML cell 2 -->
Annual, or upon material change to systems, regulations, or organizational structure

<!-- evidence:c7b5136ea3d927f0304dee48 source:word/document.xml#p00015 | table 1, XML row 7, XML cell 1 -->
Applies To

<!-- evidence:e1724c2d785f18ca7a2f05da source:word/document.xml#p00016 | table 1, XML row 7, XML cell 2 -->
All employees, contractors, interns, and third parties with access to company or client systems/data

<!-- evidence:f9f708386fe518827beb1b7e source:word/document.xml#p00018 -->
1. Purpose and Scope

<!-- evidence:4d249bb3aa6ea9f6a60f47c5 source:word/document.xml#p00019 -->
This Cryptography Policy defines the cryptographic controls used to protect the confidentiality, integrity, and authenticity of the company’s information. It applies to all founders, employees, interns, contractors, and third parties with access to company systems and data, and to all systems that store or transmit sensitive information.

<!-- evidence:5fdd75cccd56912f3f0babf1 source:word/document.xml#p00020 -->
Cryptographic controls apply to personally identifiable information, financial data, intellectual property, authentication credentials, and any data classified as Confidential or Restricted under the Data Classification Policy. This policy is proportionate to a cloud-native operating model in which key management is delegated to the cloud provider’s managed services, and works alongside the Information Security Policy, the Access Control Policy, the Password and Secrets Policy, and the Data Classification Policy.

<!-- evidence:b37a0c71af744d8a2c05c6c1 source:word/document.xml#p00021 -->
2. Roles and Responsibilities

<!-- evidence:00863ee1a1db00541bdb32b8 source:word/document.xml#p00022 -->
The Chief Executive Officer, acting as Chief Information Security Officer, owns this policy, approves the approved-algorithm set, and reviews cryptographic standards annually.

<!-- evidence:eca335fa448012b6018368f6 source:word/document.xml#p00023 -->
The Chief Technology Officer configures encryption on systems and data stores, manages keys through the cloud provider’s managed key service, and approves the cryptographic libraries used in the product.

<!-- evidence:a671a8ede1b3043f86978b08 source:word/document.xml#p00024 -->
All personnel use only approved cryptographic mechanisms and must not implement custom or unapproved cryptography.

<!-- evidence:984b6f99a71c391ae7bca7b4 source:word/document.xml#p00025 -->
3. Approved Algorithms and Key Lengths

<!-- evidence:ee18228ee371c2281bd8f483 source:word/document.xml#p00026 -->
Only the following vetted algorithms are permitted:

<!-- evidence:a8a9aacd4062f61fbb89e973 source:word/document.xml#p00027 -->
Symmetric encryption: AES with a minimum of 256-bit keys.

<!-- evidence:14311a68e156a0fdffa49915 source:word/document.xml#p00028 -->
Asymmetric encryption: RSA with a minimum of 2048-bit keys, or elliptic-curve cryptography with curves of at least 256 bits.

<!-- evidence:b8f324d6c4a7c9498d0bb015 source:word/document.xml#p00029 -->
Hashing: SHA-256 or stronger.

<!-- evidence:6bdcaf92788bcd55beb062cc source:word/document.xml#p00030 -->
Digital signatures: RSA-PSS or ECDSA, with SHA-256 or stronger.

<!-- evidence:b343a0660137785da1fc3664 source:word/document.xml#p00031 -->
Key derivation and password hashing: PBKDF2, bcrypt, scrypt, or Argon2.

<!-- evidence:ce6e868cbfc712f8eb81c5e5 source:word/document.xml#p00032 -->
Algorithms deprecated by recognized standards bodies, including MD5 and SHA-1, are prohibited. Approved algorithms and key lengths are reviewed at least annually against evolving standards.

<!-- evidence:16daaaddbe40da4f0f21e4ee source:word/document.xml#p00033 -->
4. Encryption in Transit and at Rest

<!-- evidence:2c42a9cb7723d813b26b99d4 source:word/document.xml#p00034 -->
All data transmitted over public or internal networks is encrypted using TLS 1.3, with TLS 1.2 permitted only where a required system does not yet support TLS 1.3. Deprecated protocols, including all versions of SSL and TLS 1.0 and 1.1, are prohibited, as are insecure transfer protocols such as unencrypted file transfer and remote-terminal protocols.

<!-- evidence:4b6ebb8aa32101d1b405bf24 source:word/document.xml#p00035 -->
Sensitive data at rest is encrypted using AES-256. Databases, object storage, and disks are encrypted using the cloud provider’s native encryption, enabled by default on production data stores. Endpoint disk encryption is enabled where supported by the device.

<!-- evidence:b8cf24898e5238c2697495ae source:word/document.xml#p00036 -->
5. Key Management

<!-- evidence:f8fb02dc49777c0c5734c5a1 source:word/document.xml#p00037 -->
Cryptographic keys are generated, stored, and managed through the cloud provider’s managed key service. The company does not operate its own hardware security modules; it relies on the validated cryptographic modules that underpin the provider’s managed key service, and on the provider’s certified random-number generation for key material.

<!-- evidence:9d2e27904beb0ade7b86008b source:word/document.xml#p00038 -->
Application secrets, API keys, and service-account credentials are held in the cloud provider’s managed secrets manager as defined in the Password and Secrets Policy. Keys and secrets are never committed to source control, embedded in application code, or stored in plaintext.

<!-- evidence:652195451db161fc3a984cb4 source:word/document.xml#p00039 -->
6. Key Rotation and Destruction

<!-- evidence:15384d01002f24a21257737f source:word/document.xml#p00040 -->
Keys are rotated automatically by the managed key service where provider-managed rotation is enabled. In addition, keys and secrets are rotated on evidence or suspicion of compromise, on exposure, and on departure of personnel who held access to them. Fixed calendar rotation intervals are not imposed where the managed key service handles rotation, since provider-managed rotation and access controls provide stronger assurance than manual scheduled rotation.

<!-- evidence:946f45a62d975b8096421ffd source:word/document.xml#p00041 -->
Key destruction and decommissioning are performed through the managed key service using its scheduled deletion and cryptographic erasure mechanisms, and the resulting actions are recorded in the provider’s audit logs.

<!-- evidence:42fe6f1e7bbd51d99e97ec87 source:word/document.xml#p00042 -->
7. Access to Keys

<!-- evidence:64651e05493f85371c127f1b source:word/document.xml#p00043 -->
Access to cryptographic keys and secrets is restricted to authorized roles on a least-privilege basis and enforced through role-based access control, with multi-factor authentication required as defined in the Access Control Policy. Key and secret access is logged, and access is included in the annual access review.

<!-- evidence:55ba2bd6c5e94dace860851c source:word/document.xml#p00044 -->
8. Key Lifecycle

<!-- evidence:0185394ca70f3a540fc317d7 source:word/document.xml#p00045 -->
Key lifecycle activities, comprising generation, distribution, use, storage, rotation, revocation, and destruction, follow the guidance of NIST SP 800-57 and are carried out through the managed key service so that lifecycle events are automated and auditable rather than manually administered.

<!-- evidence:95939eee8d8df9dd0107e053 source:word/document.xml#p00046 -->
9. Integrity, Attribution, and Non-Repudiation

<!-- evidence:40956b8b85369cd81a9d45bb source:word/document.xml#p00047 -->
The company relies on cryptographically supported attribution rather than transaction-level digital signatures. Actions on company systems are attributable to an individual through authenticated access via the single sign-on identity provider with multi-factor authentication, through cloud provider audit logs that record the identity, timestamp, and action for each event, and through the signed, tamper-evident commit history maintained in the source-code platform.

<!-- evidence:5df4058b07fd8d57903d4a74 source:word/document.xml#p00048 -->
Digital signatures and certificate-based authentication are used where the platform provides them, including TLS certificates for service authentication and provider-managed signing for artifacts where supported. Where a contract or regulation requires signed records for a specific business process, signatures are applied using the approved algorithms in Section 3.

<!-- evidence:551daa93acfd714567e530f9 source:word/document.xml#p00049 -->
10. Retention of Cryptographic and Audit Records

<!-- evidence:f05ef46d0131a0ffdb7778ab source:word/document.xml#p00050 -->
Audit records that establish attribution, including authentication events, key and secret access, and administrative actions, are retained in accordance with the retention requirements of the Data Classification Policy and the logging arrangements in the Access Control Policy. The cloud provider’s logging service retains logs for approximately one year, and logs shipped to object storage are retained on a long-term basis.

<!-- evidence:ad5cb0c215527b5961ef0ef9 source:word/document.xml#p00051 -->
Records are retained for the longer of the period required by contract, the period required by applicable law or regulation, and the period defined in the Data Classification Policy retention schedule. Because the company was incorporated recently, retained records extend from inception rather than for any longer fixed historical period, and the company does not represent that records predate its incorporation. Retention periods are reassessed as the company matures and as customer or regulatory obligations require.

<!-- evidence:62b2acadf48a30e6d8fe4c81 source:word/document.xml#p00052 -->
11. Approved Libraries and Tools

<!-- evidence:278dd3901534498410a69207 source:word/document.xml#p00053 -->
Only well-maintained, reputable cryptographic libraries approved by the Chief Technology Officer may be used. Custom cryptographic implementations are prohibited; the company uses standard platform and language-provided libraries. Libraries are kept current, and end-of-life or unmaintained cryptographic libraries must not be used. Dependencies are reviewed as part of the vulnerability management process defined in the Vulnerability and Patch Management Policy.

<!-- evidence:7cb921dca443199f6a486863 source:word/document.xml#p00054 -->
12. Cryptographic Failures and Incidents

<!-- evidence:4710928901f77b2b4d20a43d source:word/document.xml#p00055 -->
Suspected key compromise, certificate compromise, or cryptographic failure is treated as a security incident and handled under the Incident Management Policy. Response includes prompt revocation and replacement of affected keys, assessment of affected data, notification of affected parties in line with contractual and regulatory obligations, and a post-incident review whose findings are fed back into the risk register maintained under the Risk Management Policy.

<!-- evidence:180358725cb93b7296bc608e source:word/document.xml#p00056 -->
13. Integration with Other Policies

<!-- evidence:742b550d028ac6b449f81a5e source:word/document.xml#p00057 -->
This policy supplies the cryptographic controls that other policies rely on. The Data Classification Policy determines which data must be encrypted by assigning it a sensitivity level, and this policy determines how that encryption is performed. The Access Control Policy governs who may reach keys and secrets and enforces the authentication required to do so, while the Password and Secrets Policy governs the storage of the application secrets and credentials that this policy protects cryptographically.

<!-- evidence:d18774b08e0ce859fbdca3f1 source:word/document.xml#p00058 -->
The encryption of assets and devices required here is applied to the systems recorded under the Asset Management Policy, and cryptographic erasure supports the secure disposal that policy requires. Weaknesses in cryptographic libraries and dependencies are identified and remediated under the Vulnerability and Patch Management Policy. A suspected key or certificate compromise is handled as an event under the Incident Management Policy, and any resulting exposure is recorded and treated under the Risk Management Policy. The overall direction for all of the above is set by the Information Security Policy.

<!-- evidence:f6b93ccc50b47cf23bcc317d source:word/document.xml#p00059 -->
14. Compliance and Review

<!-- evidence:15e6b80c2b47816d88df68de source:word/document.xml#p00060 -->
Cryptographic practices support the company’s SOC 2 objectives and applicable data-protection obligations relevant to the customer data it processes. This policy, including approved algorithms, key lengths, and protocols, is reviewed at least annually, and additionally following disclosure of a significant cryptographic vulnerability or a material change to systems.

<!-- evidence:c4d038bb57ce36f3a47601d0 source:word/document.xml#p00061 -->
15. Policy Acknowledgment

<!-- evidence:01e57c8c8c222a51c94166a8 source:word/document.xml#p00062 -->
All personnel are required to acknowledge this policy at onboarding and on significant updates. Violations may result in disciplinary action under the Human Resource Policy, up to and including termination.

<!-- evidence:3cc0847b9ef280a7afa73adb source:word/document.xml#p00063 -->
Document Control

<!-- evidence:2b207e0268ffd3bf9e362e5b source:word/document.xml#p00064 -->
Revision History

<!-- evidence:43cc4a4c9f9eeaec429fe718 source:word/document.xml#p00065 | table 2, XML row 1, XML cell 1 -->
Version

<!-- evidence:6d8e2c56e2da7ea5fa7160a5 source:word/document.xml#p00066 | table 2, XML row 1, XML cell 2 -->
Date

<!-- evidence:b56baaf982ee04fe07666a99 source:word/document.xml#p00067 | table 2, XML row 1, XML cell 3 -->
Author

<!-- evidence:101efdb7bcffd700107fb7c4 source:word/document.xml#p00068 | table 2, XML row 1, XML cell 4 -->
Description of Change

<!-- evidence:984cb0219dde080e2a33ff53 source:word/document.xml#p00069 | table 2, XML row 2, XML cell 1 -->
1.0

<!-- evidence:a616d359f563c11ff1f37b4f source:word/document.xml#p00070 | table 2, XML row 2, XML cell 2 -->
14-07-2026

<!-- evidence:37f32a733de67d887319b808 source:word/document.xml#p00071 | table 2, XML row 2, XML cell 3 -->
Sahil Pugalia

<!-- evidence:e1ea1d3d856014b861521f0e source:word/document.xml#p00072 | table 2, XML row 2, XML cell 4 -->
Initial policy

<!-- evidence:63e6dcc70095c99aba2863ff source:word/document.xml#p00073 -->
Approval

<!-- evidence:15cda855d6c04b9700b66947 source:word/document.xml#p00074 | table 3, XML row 1, XML cell 1 -->
Role

<!-- evidence:cb00db4a7e87e8d2364775de source:word/document.xml#p00075 | table 3, XML row 1, XML cell 2 -->
Name

<!-- evidence:17fb5766f35a6822ea6d92fe source:word/document.xml#p00076 | table 3, XML row 1, XML cell 3 -->
Date

<!-- evidence:bf599595b16fc95ee8e3b683 source:word/document.xml#p00077 | table 3, XML row 2, XML cell 1 -->
Chief Business Officer / Chief Privacy Officer

<!-- evidence:3bad20d767aba95f43a3f4b5 source:word/document.xml#p00078 | table 3, XML row 2, XML cell 2 -->
Priyanka Choudhury
