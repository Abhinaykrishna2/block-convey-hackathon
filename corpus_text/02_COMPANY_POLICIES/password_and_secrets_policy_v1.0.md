# Regodit_password_and_secrets_policy_v1.0

Source: `Hackathon/2. Company policies/Regodit_password_and_secrets_policy_v1.0.docx`
Source SHA-256: `1fc6cd68d0f07d695376b87c97c995fe7f2e6a415c923ae3d476555ff7bf8a05`
Document role: `documented_policy`

The text below records source statements. Policy requirements, template text, and requested actions are not proof of implementation or completion.

<!-- evidence:873245839be0880d6776cb05 source:word/document.xml#p00001 -->
Password and Secrets Policy

<!-- evidence:069e60255eeb5ce30dccea3b source:word/document.xml#p00002 -->
Solsphere AI Inc.| Regodit

<!-- evidence:b795da8754a0f00ffb77b995 source:word/document.xml#p00003 | table 1, XML row 1, XML cell 1 -->
Document Title

<!-- evidence:aa12e13d0b49d75eb8224424 source:word/document.xml#p00004 | table 1, XML row 1, XML cell 2 -->
Password and Secrets Policy

<!-- evidence:b68f1b2ee0bf727561573f5f source:word/document.xml#p00005 | table 1, XML row 2, XML cell 1 -->
Document Owner

<!-- evidence:4bac5348504ee3f0fe5bd43d source:word/document.xml#p00006 | table 1, XML row 2, XML cell 2 -->
Sahil Pugalia

<!-- evidence:e7e3e9a55059a26daaf1ad56 source:word/document.xml#p00007 | table 1, XML row 3, XML cell 1 -->
Approved By

<!-- evidence:305dbc36373ad7996fe0cbe4 source:word/document.xml#p00008 | table 1, XML row 3, XML cell 2 -->
Priyanka Choudhury

<!-- evidence:f0652d25a01920c6aeaeaea1 source:word/document.xml#p00009 | table 1, XML row 4, XML cell 1 -->
Classification

<!-- evidence:09738367f2fbc705c8605123 source:word/document.xml#p00010 | table 1, XML row 4, XML cell 2 -->
Internal / Confidential

<!-- evidence:a129044bfcb025d866c29bf3 source:word/document.xml#p00011 | table 1, XML row 5, XML cell 1 -->
Effective Date

<!-- evidence:0cec5ac63a08c7c33a1d1bdc source:word/document.xml#p00012 | table 1, XML row 5, XML cell 2 -->
14 July 2026

<!-- evidence:61608c78a5a5ecdf19f34af5 source:word/document.xml#p00013 | table 1, XML row 6, XML cell 1 -->
Review Cycle

<!-- evidence:b12afe3bb3ccd631b7c39e56 source:word/document.xml#p00014 | table 1, XML row 6, XML cell 2 -->
Annual, or upon material change to systems, regulations, or organizational structure

<!-- evidence:5909da00647a77c258b863d5 source:word/document.xml#p00015 | table 1, XML row 7, XML cell 1 -->
Applies To

<!-- evidence:ad60b20b81bf985afe53e01f source:word/document.xml#p00016 | table 1, XML row 7, XML cell 2 -->
All employees, contractors, interns, and third parties with access to company or client systems/data

<!-- evidence:b6a0e28e09a526c1ff02b2f4 source:word/document.xml#p00018 -->
1. Purpose and Scope

<!-- evidence:c15b0f8da107ec41142db455 source:word/document.xml#p00019 -->
This Password and Secrets Policy defines how passwords, credentials, and application secrets are constructed, protected, and managed so that access to the company’s systems and data stays secure. It applies to all founders, employees, interns, contractors, and third parties with access to company systems.

<!-- evidence:ceb95539c3881afb493988a1 source:word/document.xml#p00020 -->
The policy is proportionate to a small, cloud-native, remote-first team in which most authentication is centralized through a single sign-on identity provider protected by multi-factor authentication. It works alongside the Information Security Policy, the Access Control Policy, and the Cryptography Policy, and follows the guidance in NIST SP 800-63B.

<!-- evidence:22a30681baf084fb53428887 source:word/document.xml#p00021 -->
2. Roles and Responsibilities

<!-- evidence:a5666c8f60791881f75d7be2 source:word/document.xml#p00022 -->
The Chief Executive Officer, acting as Chief Information Security Officer, owns this policy and the company’s password and secrets standards.

<!-- evidence:3298ff22063382fbda53924b source:word/document.xml#p00023 -->
The Chief Technology Officer configures and manages secrets storage and enforces authentication controls in the identity provider and cloud consoles.

<!-- evidence:2052d325bd8502e7626ea9e6 source:word/document.xml#p00024 -->
All users protect their own credentials, do not share them, and report any suspected credential compromise.

<!-- evidence:555af30acd9ac181fae466ef source:word/document.xml#p00025 -->
3. Password Construction

<!-- evidence:8cdef11d1528ec3f4c2cb36b source:word/document.xml#p00026 -->
Passwords must be at least 12 characters. Passphrases are encouraged, and length is prioritized over forced character-composition rules. Passwords must not reuse dictionary words, usernames, or easily guessable information, and known-breached passwords are screened and rejected where the identity provider supports it. Construction requirements are enforced centrally through the identity provider wherever possible.

<!-- evidence:298a33e7f1d26476209b9ef4 source:word/document.xml#p00027 -->
4. Multi-Factor Authentication

<!-- evidence:3a993e43a47535017b644b13 source:word/document.xml#p00028 -->
Multi-factor authentication is required across all core systems, including cloud infrastructure consoles, the identity and email provider, and the source-code platform, and for all administrative access. MFA coverage is defined in the Access Control Policy.

<!-- evidence:ef277f1aeddb5311e9834b09 source:word/document.xml#p00029 -->
5. Password Rotation

<!-- evidence:fb7c4ab2148b710f169442ed source:word/document.xml#p00030 -->
The company does not force scheduled or periodic password rotation. Consistent with NIST SP 800-63B, passwords are changed only on evidence or suspicion of compromise, on exposure of a shared credential, or where a specific system requires it. Forced periodic rotation tends to encourage weaker, predictable passwords; multi-factor authentication and breach screening provide stronger protection.

<!-- evidence:30fb03015d55928ca7ef2543 source:word/document.xml#p00031 -->
6. Account Lockout and Brute-Force Protection

<!-- evidence:9783782bbb60f01749863b04 source:word/document.xml#p00032 -->
Account lockout, rate-limiting, and brute-force protections are enforced by the identity provider and cloud consoles using their standard controls, rather than by self-configured thresholds. Anomalous authentication activity surfaced by these providers is reviewed and investigated.

<!-- evidence:1d8b1c0dda62224434b27b41 source:word/document.xml#p00033 -->
7. Credential Storage and Transmission

<!-- evidence:9d4604c7ff4ed868301fdfe7 source:word/document.xml#p00034 -->
Passwords are never stored in plaintext. Where the company controls credential storage, passwords are hashed and salted using a strong algorithm such as bcrypt, scrypt, Argon2, or PBKDF2. Credentials are transmitted only over encrypted channels using TLS. Users must not store passwords in plaintext files or in unmanaged browser stores.

<!-- evidence:85ec667b5eb6da5ee3eea85f source:word/document.xml#p00035 -->
8. Secrets Management

<!-- evidence:98f1fdb1e9f160cb41224252 source:word/document.xml#p00036 -->
Application secrets, API keys, and service-account credentials are stored in the cloud provider’s managed secrets manager. Secrets are not committed to source control or hard-coded into application code. Access to secrets is restricted by role and logged, and secrets are rotated on suspected exposure or on relevant personnel changes. Each service account uses a unique credential scoped to least privilege.

<!-- evidence:dc77d9a14c8bbd17b082b4e6 source:word/document.xml#p00037 -->
9. Privileged and Administrative Accounts

<!-- evidence:2a40c5ae2f56f18b1a40b9f2 source:word/document.xml#p00038 -->
Privileged and administrative accounts require multi-factor authentication without exception, are limited to the minimum number of holders, and follow least privilege. Privileged actions are logged. Additional controls for production and administrative access are defined in Section 5 of the Access Control Policy.

<!-- evidence:25c2374514947661c530ff03 source:word/document.xml#p00039 -->
10. Password Managers

<!-- evidence:0ed9838aa5abb306326f5ada source:word/document.xml#p00040 -->
For any credentials not covered by single sign-on, personnel are expected to use an approved password manager. Credentials must not be recorded in plaintext or shared through insecure channels.

<!-- evidence:90498089048d2a24f78d6779 source:word/document.xml#p00041 -->
11. Recovery and Temporary Credentials

<!-- evidence:b3ee7eb18a5367e65a19d8fe source:word/document.xml#p00042 -->
Password recovery is handled through the identity provider’s verified recovery flow. Recovery and reset links are single-use and time-limited. Any temporary or system-generated password is randomly generated, single-use, and expires shortly after issue.

<!-- evidence:5dcdd4237b4942d614c0c20b source:word/document.xml#p00043 -->
12. User Awareness

<!-- evidence:fbb5213482280bea9bc2e43e source:word/document.xml#p00044 -->
Credential hygiene, including recognizing phishing and handling secrets safely, is covered during onboarding and in ongoing security awareness training delivered through the company’s platform, as described in the Information Security Policy and the Human Resource Policy.

<!-- evidence:971502d3c62251c2bdeafb12 source:word/document.xml#p00045 -->
13. Integration with Other Policies

<!-- evidence:57b0fd5b653cabf77e4bd91e source:word/document.xml#p00046 -->
This policy supports the Access Control Policy, which determines who may access what; this policy governs the credentials and secrets by which that access is proven. The two are intended to be read together, and the multi-factor authentication requirement stated in both is a single control described from two perspectives.

<!-- evidence:01249e54793c8e4116fc96af source:word/document.xml#p00047 -->
Secrets and keys protected here are encrypted and managed as set out in the Cryptography Policy, and the credentials themselves are treated as Restricted information under the Data Classification Policy. The systems on which credentials are used are recorded under the Asset Management Policy. Credential hygiene is taught as part of the training arrangements described in the Information Security Policy and the Human Resource Policy.

<!-- evidence:8bbbcc535e2dccfef4bf3b6b source:word/document.xml#p00048 -->
A suspected or confirmed credential compromise is handled as an event under the Incident Management Policy, and triggers the rotation required by this policy. Weaknesses in the libraries used to store or hash credentials are remediated under the Vulnerability and Patch Management Policy, and any accepted exposure is recorded under the Risk Management Policy.

<!-- evidence:290586768c6bc9a9b8cff697 source:word/document.xml#p00049 -->
14. Compliance and Review

<!-- evidence:1d7ac6ebfe980e8c1ef11acb source:word/document.xml#p00050 -->
This policy supports the company’s SOC 2 objectives and aligns with NIST SP 800-63B. It is reviewed at least annually and updated as the company grows or its controls change.

<!-- evidence:57c4c75aa3139611450de007 source:word/document.xml#p00051 -->
15. Policy Acknowledgment

<!-- evidence:80029fc2a2148967d9dceb2a source:word/document.xml#p00052 -->
All personnel are required to acknowledge this policy at onboarding and on significant updates. Violations may result in disciplinary action under the Human Resource Policy, up to and including termination.

<!-- evidence:b4dbaa707dba74453d2781fb source:word/document.xml#p00053 -->
Document Control

<!-- evidence:4d2bfa30f84c39a28f1be60e source:word/document.xml#p00054 -->
Revision History

<!-- evidence:49058e1de6a4b6cd20d9c518 source:word/document.xml#p00055 | table 2, XML row 1, XML cell 1 -->
Version

<!-- evidence:d2fcd74234e257bc2ef71667 source:word/document.xml#p00056 | table 2, XML row 1, XML cell 2 -->
Date

<!-- evidence:903e7aaaec93b44090aab9e6 source:word/document.xml#p00057 | table 2, XML row 1, XML cell 3 -->
Author

<!-- evidence:6ef331374c0f41953e720339 source:word/document.xml#p00058 | table 2, XML row 1, XML cell 4 -->
Description of Change

<!-- evidence:0dc74095ee41ef7cc203dc26 source:word/document.xml#p00059 | table 2, XML row 2, XML cell 1 -->
1.0

<!-- evidence:5c4a05c6d3d80d1bd68315e4 source:word/document.xml#p00060 | table 2, XML row 2, XML cell 2 -->
14-07-2026

<!-- evidence:c7967dc86e5624412c35d0de source:word/document.xml#p00061 | table 2, XML row 2, XML cell 3 -->
Sahil Pugalia

<!-- evidence:dde18077c2829512d427c9e9 source:word/document.xml#p00062 | table 2, XML row 2, XML cell 4 -->
Initial policy

<!-- evidence:e20b7bcb7e5c29a778d18048 source:word/document.xml#p00063 -->
Approval

<!-- evidence:5a73c370c2dcb17eea337708 source:word/document.xml#p00064 | table 3, XML row 1, XML cell 1 -->
Role

<!-- evidence:982218ee9ae0c9a85c656dc8 source:word/document.xml#p00065 | table 3, XML row 1, XML cell 2 -->
Name

<!-- evidence:b5f0fdbb6cc4a5332ca19d09 source:word/document.xml#p00066 | table 3, XML row 1, XML cell 3 -->
Date

<!-- evidence:fa80c1e14bef629c98b9fb28 source:word/document.xml#p00067 | table 3, XML row 2, XML cell 1 -->
Chief Business Officer / Chief Privacy Officer

<!-- evidence:7969ea8d69b19c2d60f4d49e source:word/document.xml#p00068 | table 3, XML row 2, XML cell 2 -->
Priyanka Choudhury
