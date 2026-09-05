# BCP_DR_Plan_Solsphere

Source: `Hackathon/5. Infrastructure_internal info/BCP_DR_Plan_Solsphere.docx`
Source SHA-256: `6c1ffa158ff553a3141d83756741c9e4166e5fe18ccfe6631c0bdccc8b59d3fb`
Document role: `template_with_placeholders`

The text below records source statements. Policy requirements, template text, and requested actions are not proof of implementation or completion.

<!-- evidence:8a8a7a6156faf49ec2c96679 source:word/document.xml#p00001 -->
Business Continuity & Disaster Recovery (BCP / DR) Plan

<!-- evidence:dc99ef72cc51022479dd8d2b source:word/document.xml#p00003 -->
Company Name: Solsphere AI Inc

<!-- evidence:97ab7f5499ab266e90c895ae source:word/document.xml#p00004 -->
Effective Date: 09/04/2026

<!-- evidence:bde02d7e6b98148ac3fe1217 source:word/document.xml#p00005 -->
Approved By: S. Pugalia, CEO

<!-- evidence:5a144e54da5a36a4b177f85c source:word/document.xml#p00007 -->
1. Purpose

<!-- evidence:828593aa6244deedab7dd378 source:word/document.xml#p00008 -->
This Business Continuity & Disaster Recovery (BCP/DR) Plan is designed to ensure the ongoing operation of the company's critical business functions and the protection of customer data in the event of any disruption, disaster, or emergency. Such events may include natural disasters, cyber incidents, or system failures. The plan aims to provide a framework for maintaining essential services and safeguarding sensitive information during adverse situations.

<!-- evidence:e4b1924a382c2c671a0f59b8 source:word/document.xml#p00009 -->
2. Scope

<!-- evidence:f13964646dcc674d767babd3 source:word/document.xml#p00010 -->
The scope of this plan encompasses all production systems, cloud environments, and business-critical SaaS tools utilized by the company. It applies to every individual with access to company systems or customer data, including employees, contractors, and vendors. The objective is to ensure comprehensive protection and continuity across all operational areas and personnel.

<!-- evidence:e6cf1af678ca7311c0dbc497 source:word/document.xml#p00011 -->
3. Objectives

<!-- evidence:3bc05de741004b8c3385fd6c source:word/document.xml#p00012 -->
Minimize disruption to business operations.

<!-- evidence:991dea8742e2fa66947250de source:word/document.xml#p00013 -->
Ensure the recovery of systems, data, and applications.

<!-- evidence:9ef079122b84ee1b47013b73 source:word/document.xml#p00014 -->
Maintain the security and confidentiality of protected information, including personally identifiable information (PII) and protected health information (PHI).

<!-- evidence:0a43463134bf54022ff540e0 source:word/document.xml#p00015 -->
Facilitate effective communication with employees, customers, and partners during an incident.

<!-- evidence:f440d8ef937cb0aada281fb7 source:word/document.xml#p00016 -->
4. Roles and Responsibilities

<!-- evidence:910d68c946053e4af8966170 source:word/document.xml#p00017 | table 1, XML row 1, XML cell 1 -->
Role

<!-- evidence:d7457c24cf713f9d1e2dbce6 source:word/document.xml#p00018 | table 1, XML row 1, XML cell 2 -->
Responsibility

<!-- evidence:64ef52c0d0387c8b6763335a source:word/document.xml#p00019 | table 1, XML row 2, XML cell 1 -->
BCP/DR Coordinator (CTO / Co-Founder)

<!-- evidence:c991bc1a466c2d6347d9bbf9 source:word/document.xml#p00020 | table 1, XML row 2, XML cell 2 -->
Owns the BCP/DR plan, leads the recovery process, and coordinates efforts with all relevant stakeholders.

<!-- evidence:8d00249c67a5c34d57056e66 source:word/document.xml#p00021 | table 1, XML row 3, XML cell 1 -->
IT Lead

<!-- evidence:3d7e80cf7f9f48d4f606d758 source:word/document.xml#p00022 | table 1, XML row 3, XML cell 2 -->
Responsible for restoring systems, managing backups, and verifying the integrity of data throughout the recovery process.

<!-- evidence:bc1bb55d88f856607b308e24 source:word/document.xml#p00023 | table 1, XML row 4, XML cell 1 -->
Security & Compliance Lead

<!-- evidence:af8bb069b6ca686cfa13cb7f source:word/document.xml#p00024 | table 1, XML row 4, XML cell 2 -->
Ensures that all security controls and evidentiary documentation align with SOC 2 and HIPAA requirements.

<!-- evidence:4bcc2b0c5d40af12c468c163 source:word/document.xml#p00025 | table 1, XML row 5, XML cell 1 -->
CEO / Founder

<!-- evidence:08d4ff80c55f20cfb5288364 source:word/document.xml#p00026 | table 1, XML row 5, XML cell 2 -->
Approves the activation of the plan and handles external communications as necessary.

<!-- evidence:aaf3ffa82639389f40691d7c source:word/document.xml#p00027 | table 1, XML row 6, XML cell 1 -->
All Employees

<!-- evidence:fc1ac7ee6a1da1c1ce4be547 source:word/document.xml#p00028 | table 1, XML row 6, XML cell 2 -->
Adhere to internal communication and escalation procedures as outlined in the plan.

<!-- evidence:cd0572fd7b94f29c31c80d76 source:word/document.xml#p00029 -->
5. Risk & Impact Assessment

<!-- evidence:85beb1aa1a0161d8483d282a source:word/document.xml#p00030 | table 2, XML row 1, XML cell 1 -->
Type of Threat

<!-- evidence:cf3b50f544999c2a9c8b4f3c source:word/document.xml#p00031 | table 2, XML row 1, XML cell 2 -->
Example

<!-- evidence:1eb6ffc7ce122e137ee004c9 source:word/document.xml#p00032 | table 2, XML row 1, XML cell 3 -->
Impact

<!-- evidence:446f647c6e69c01a607f459e source:word/document.xml#p00033 | table 2, XML row 1, XML cell 4 -->
Mitigation / Control

<!-- evidence:89db8793523de78bb90c8bfe source:word/document.xml#p00034 | table 2, XML row 2, XML cell 1 -->
Cloud Provider Outage

<!-- evidence:31c51ba571a4a6a4f8403146 source:word/document.xml#p00035 | table 2, XML row 2, XML cell 2 -->
AWS region failure

<!-- evidence:861602334ae9df07a95373af source:word/document.xml#p00036 | table 2, XML row 2, XML cell 3 -->
High

<!-- evidence:77f7a38e08572e2777aeb03f source:word/document.xml#p00037 | table 2, XML row 2, XML cell 4 -->
Implement a multi-region backup and failover strategy to minimize downtime and data loss.

<!-- evidence:7692a4c038906939b3ab1d54 source:word/document.xml#p00038 | table 2, XML row 3, XML cell 1 -->
Cyber Attack

<!-- evidence:fa6f17c0bea7cf537bffbe9e source:word/document.xml#p00039 | table 2, XML row 3, XML cell 2 -->
Unauthorized access, encryption of data

<!-- evidence:35a4a55e90006b62764192de source:word/document.xml#p00040 | table 2, XML row 3, XML cell 3 -->
High

<!-- evidence:165708832928d0fbf60040ff source:word/document.xml#p00041 | table 2, XML row 3, XML cell 4 -->
Enforce multi-factor authentication (MFA), identity and access management (IAM) controls, endpoint detection and response (EDR) protection, and daily backups.

<!-- evidence:ce01b4ad15be33b47751985a source:word/document.xml#p00042 | table 2, XML row 4, XML cell 1 -->
Human Error

<!-- evidence:ecf260b0d6740228dccdd28e source:word/document.xml#p00043 | table 2, XML row 4, XML cell 2 -->
Accidental deletion, misconfiguration

<!-- evidence:e01e6a6431f31e14a0bb9ba0 source:word/document.xml#p00044 | table 2, XML row 4, XML cell 3 -->
Medium

<!-- evidence:37085cb6118ca15137796ca9 source:word/document.xml#p00045 | table 2, XML row 4, XML cell 4 -->
Utilize version control systems, apply IAM least privilege principles, and provide regular training to personnel.

<!-- evidence:60bfc776b14bbaee90054f52 source:word/document.xml#p00046 | table 2, XML row 5, XML cell 1 -->
Data Loss / Corruption

<!-- evidence:53960af89600b01711562db1 source:word/document.xml#p00047 | table 2, XML row 5, XML cell 2 -->
Backup failure or sync error

<!-- evidence:b784789d6deefa7a5cb5a2d2 source:word/document.xml#p00048 | table 2, XML row 5, XML cell 3 -->
High

<!-- evidence:9cdf0a942b60c11e5da42422 source:word/document.xml#p00049 | table 2, XML row 5, XML cell 4 -->
Perform daily backups with routine restore validation to ensure data can be recovered effectively.

<!-- evidence:c4d4d773535261c1c9376f22 source:word/document.xml#p00050 | table 2, XML row 6, XML cell 1 -->
Natural Disaster

<!-- evidence:322db8b131c042160a459642 source:word/document.xml#p00051 | table 2, XML row 6, XML cell 2 -->
Office outage

<!-- evidence:02a0cc5daa0be667dd62df00 source:word/document.xml#p00052 | table 2, XML row 6, XML cell 3 -->
Low

<!-- evidence:ba72909f97b61adf2682c64d source:word/document.xml#p00053 | table 2, XML row 6, XML cell 4 -->
Enable remote work capabilities and maintain cloud-hosted systems to reduce impact.

<!-- evidence:9259320c8eaa8274412d1fc2 source:word/document.xml#p00054 | table 2, XML row 7, XML cell 1 -->
Vendor Failure

<!-- evidence:b44a38e40cf0749eafeb3033 source:word/document.xml#p00055 | table 2, XML row 7, XML cell 2 -->
Downstream SaaS provider unavailable

<!-- evidence:673553814ab2bf43af44f52d source:word/document.xml#p00056 | table 2, XML row 7, XML cell 3 -->
Medium

<!-- evidence:7f62cdc1158217a8db3be9ab source:word/document.xml#p00057 | table 2, XML row 7, XML cell 4 -->
Establish secondary vendor options and conduct regular vendor risk reviews to ensure continuity.

<!-- evidence:259c2a89a60f3110e686317a source:word/document.xml#p00058 -->
6. Recovery Objectives

<!-- evidence:ac7efcd98d4f316387f98381 source:word/document.xml#p00059 | table 3, XML row 1, XML cell 1 -->
System / Function

<!-- evidence:d69c3bc76b26d75f0c7c17da source:word/document.xml#p00060 | table 3, XML row 1, XML cell 2 -->
Recovery Time Objective (RTO)

<!-- evidence:c4c178f3a61922e1c58a98d8 source:word/document.xml#p00061 | table 3, XML row 1, XML cell 3 -->
Recovery Point Objective (RPO)

<!-- evidence:9d9396efa0b1aa265509a468 source:word/document.xml#p00062 | table 3, XML row 1, XML cell 4 -->
Recovery Strategy 

<!-- evidence:8465b44b4115b66d2e1e8655 source:word/document.xml#p00063 | table 3, XML row 2, XML cell 1 -->
Core Application

<!-- evidence:d931598ef6c658216c471c1a source:word/document.xml#p00064 | table 3, XML row 2, XML cell 2 -->
2-8 hours

<!-- evidence:5bfca89142ec65d78c12d2fe source:word/document.xml#p00065 | table 3, XML row 2, XML cell 3 -->
15 mins – 1 Hour

<!-- evidence:9c8085e1e5998cbbf1f806be source:word/document.xml#p00066 | table 3, XML row 2, XML cell 4 -->
Restore from S3 backup or deploy to an alternate AWS region as necessary.

<!-- evidence:3787d2d1d31b1010f5aa040b source:word/document.xml#p00067 | table 3, XML row 3, XML cell 1 -->
Production Database

<!-- evidence:9777d1b46f833dc8c964359f source:word/document.xml#p00068 | table 3, XML row 3, XML cell 2 -->
< 4 Hours

<!-- evidence:5770cfb78946851d7456222d source:word/document.xml#p00069 | table 3, XML row 3, XML cell 3 -->
< 15 mins

<!-- evidence:a3b63410c8e1d96282e0983a source:word/document.xml#p00070 | table 3, XML row 3, XML cell 4 -->
Utilize daily snapshots and point-in-time recovery methods.

<!-- evidence:8c2632dae94939b34b65c066 source:word/document.xml#p00071 | table 3, XML row 4, XML cell 1 -->
Email / Collaboration

<!-- evidence:3ed7ac0c577bf2262e35f1d3 source:word/document.xml#p00072 | table 3, XML row 4, XML cell 2 -->
4-12 Hours

<!-- evidence:06c4e7079a2fd6c52cab131c source:word/document.xml#p00073 | table 3, XML row 4, XML cell 3 -->
1-6 Hours

<!-- evidence:6ed87d702a8446bafddb7e61 source:word/document.xml#p00074 | table 3, XML row 4, XML cell 4 -->
Leverage Google Workspace with replication for fast recovery.

<!-- evidence:85c67303e78a67879406c686 source:word/document.xml#p00075 | table 3, XML row 5, XML cell 1 -->
Source Code Repos

<!-- evidence:9c33e2fcf83a0f54fb7b22a2 source:word/document.xml#p00076 | table 3, XML row 5, XML cell 2 -->
< 4 Hours

<!-- evidence:94a0ce13fcf1e059f73e48f1 source:word/document.xml#p00077 | table 3, XML row 5, XML cell 3 -->
< 4 Hours

<!-- evidence:7431d1e0f102cced5c552fc6 source:word/document.xml#p00078 | table 3, XML row 5, XML cell 4 -->
Maintain redundancy with GitHub and regular backups.

<!-- evidence:14ebc8fa9796340c36d4d8d1 source:word/document.xml#p00079 | table 3, XML row 6, XML cell 1 -->
Support / Ticketing

<!-- evidence:2eacaf63b2377402d0b3f97b source:word/document.xml#p00080 | table 3, XML row 6, XML cell 2 -->
12-24 Hours

<!-- evidence:e63e4ba1f4d6ba546404d592 source:word/document.xml#p00081 | table 3, XML row 6, XML cell 3 -->
4-12 Hours

<!-- evidence:0197dee22439dba7334fb80e source:word/document.xml#p00082 | table 3, XML row 6, XML cell 4 -->
Utilize SaaS provider failover capabilities.

<!-- evidence:5f6c24210bc6e746ee9edf17 source:word/document.xml#p00083 | table 3, XML row 7, XML cell 1 -->
Employee Devices

<!-- evidence:0a4c0d024296890a2d4df3fc source:word/document.xml#p00084 | table 3, XML row 7, XML cell 2 -->
< 48 Hours

<!-- evidence:3d9fe2f1d140c084b4c5f9fe source:word/document.xml#p00085 | table 3, XML row 7, XML cell 3 -->
< 24 Hours

<!-- evidence:06c7d880a937808228178c24 source:word/document.xml#p00086 | table 3, XML row 7, XML cell 4 -->
Provision cloud-based device configurations using mobile device management (MDM) tools.

<!-- evidence:3e546e036006c6036d9ea676 source:word/document.xml#p00088 -->
Instructions for Use: 

<!-- evidence:446cdc8701e74f8063f46b43 source:word/document.xml#p00089 -->
This template has been pre-filled with suggested responses in each section to help guide you through the completion process. Please carefully review the content provided and update or modify each section as necessary to ensure it aligns with your organization’s unique business processes, roles and requirements. Customizing the information will help maintain accuracy and relevance for your specific operational needs.
