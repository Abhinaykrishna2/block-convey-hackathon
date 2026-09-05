# Regodit_business_continuity_and_disaster_recovery_policy_v1.0

Source: `Hackathon/2. Company policies/Regodit_business_continuity_and_disaster_recovery_policy_v1.0.docx`
Source SHA-256: `ee9e365e786f94ecd616f3c97f48ffe3e8767b3f9eda91b5d6d2de90e26876ba`
Document role: `documented_policy`

The text below records source statements. Policy requirements, template text, and requested actions are not proof of implementation or completion.

<!-- evidence:0bb0b3d5eca3a331905a634d source:word/document.xml#p00001 -->
Business Continuity and Disaster Recovery Policy

<!-- evidence:1704817e8c147270bcf954f3 source:word/document.xml#p00002 -->
Solsphere AI Inc. | Regodit

<!-- evidence:aa139c571aaade8467577b00 source:word/document.xml#p00003 | table 1, XML row 1, XML cell 1 -->
Document Title

<!-- evidence:5b9edc53bb1d9a20a9e38b71 source:word/document.xml#p00004 | table 1, XML row 1, XML cell 2 -->
Business Continuity and Disaster Recovery Policy

<!-- evidence:d9c4e576f5c6ed0a98737a8c source:word/document.xml#p00005 | table 1, XML row 2, XML cell 1 -->
Document Owner

<!-- evidence:015eb9b37f585fb6f9c84553 source:word/document.xml#p00006 | table 1, XML row 2, XML cell 2 -->
Sahil Pugalia

<!-- evidence:fb412b091f349bbab325e566 source:word/document.xml#p00007 | table 1, XML row 3, XML cell 1 -->
Approved By

<!-- evidence:4d42e3fabf86f0c314c14296 source:word/document.xml#p00008 | table 1, XML row 3, XML cell 2 -->
Priyanka Choudhury

<!-- evidence:062bf2e7010e0097a880026f source:word/document.xml#p00009 | table 1, XML row 4, XML cell 1 -->
Classification

<!-- evidence:ba75daeeb17de93e9accecf4 source:word/document.xml#p00010 | table 1, XML row 4, XML cell 2 -->
Internal / Confidential

<!-- evidence:16342264d888a9a547e3f339 source:word/document.xml#p00011 | table 1, XML row 5, XML cell 1 -->
Effective Date

<!-- evidence:717df53c71372b798ea86019 source:word/document.xml#p00012 | table 1, XML row 5, XML cell 2 -->
14 July 2026

<!-- evidence:a84ec6deedf361a4c71082b0 source:word/document.xml#p00013 | table 1, XML row 6, XML cell 1 -->
Review Cycle

<!-- evidence:40df9a9d479b3231edd1abf7 source:word/document.xml#p00014 | table 1, XML row 6, XML cell 2 -->
Annual, or upon material change to systems, regulations, or organizational structure

<!-- evidence:84fd62cf7ead8166aee21d9f source:word/document.xml#p00015 | table 1, XML row 7, XML cell 1 -->
Applies To

<!-- evidence:2d90fbedd329dd6755788ce9 source:word/document.xml#p00016 | table 1, XML row 7, XML cell 2 -->
All employees, contractors, interns, and third parties with access to company or client systems/data

<!-- evidence:4899d29d4d098ab8934be2b0 source:word/document.xml#p00018 -->
1. Purpose and Scope

<!-- evidence:006ef6c0c7ec4667b4d03f74 source:word/document.xml#p00019 -->
This Business Continuity and Disaster Recovery Policy sets out how the company prepares for, responds to, and recovers from disruptions affecting its systems, data, and ability to operate. It applies to all founders, employees, interns, contractors, and third parties involved in company operations.

<!-- evidence:7b1c5cfe5a1a3d4a60c35776 source:word/document.xml#p00020 -->
In scope are the company’s production environment and the data it holds, the software-as-a-service applications the business depends on, and the company’s ability to work through disruption. The policy is proportionate to a cloud-native, remote-first operating model in which infrastructure resilience is delegated to the cloud provider and the company owns no physical premises critical to operations. It works alongside the Incident Management Policy, the Information Security Policy, the Asset Management Policy, the Risk Management Policy, and the Data Classification Policy.

<!-- evidence:daac2ccd24588dede8c2b41e source:word/document.xml#p00021 -->
2. Roles and Responsibilities

<!-- evidence:f0265b7b9a356df039554b26 source:word/document.xml#p00022 -->
The Chief Executive Officer, acting as Chief Information Security Officer, owns this policy, declares activation of continuity and recovery procedures, and owns cloud infrastructure recovery.

<!-- evidence:bc7c9f218aedce1bb0b58490 source:word/document.xml#p00023 -->
The Chief Technology Officer leads technical recovery, including restoration of data and redeployment of the application, and confirms service integrity before operations resume.

<!-- evidence:1a368fdad2c625cfc13cc3df source:word/document.xml#p00024 -->
The Chief Business Officer / Chief Privacy Officer coordinates communication with customers, partners, and other external parties, and owns non-technical continuity matters.

<!-- evidence:b34ba936b0f360348c8d3e2e source:word/document.xml#p00025 -->
All personnel report disruption promptly and follow the procedures in this policy.

<!-- evidence:fb8cd0eeb52e3b1d51ef4130 source:word/document.xml#p00026 -->
The company does not maintain separate business continuity, disaster recovery, or incident response teams. These roles are performed by the founders, as stated in the Information Security Policy.

<!-- evidence:b4258232adb077cc16b95404 source:word/document.xml#p00027 -->
3. Operating Model and Continuity Assumptions

<!-- evidence:249a98f545ea5f92694f79dc source:word/document.xml#p00028 -->
The company is remote-first and holds no on-premises servers, data centers, or server rooms. Loss of access to any physical workspace, including the co-working facility used by some personnel, does not interrupt operations, because personnel work remotely and all systems are accessed over the internet. Continuity planning therefore focuses on the availability of the production environment, the recoverability of data, and the availability of the third-party services the business depends on.

<!-- evidence:ddc2a553d4a139823ace61be source:word/document.xml#p00029 -->
4. Business Impact and Risk Assessment

<!-- evidence:ea78f6c86c0177d18b7d3dd8 source:word/document.xml#p00030 -->
Critical services, their dependencies, and the impact of their loss are identified as part of the annual risk assessment carried out under the Risk Management Policy. Disruption scenarios considered include loss of a cloud availability zone, data corruption or accidental deletion, compromise of the production environment, failure or outage of a critical third-party service, and unavailability of key personnel. Risks arising from these scenarios are recorded in the risk register and treated in accordance with that policy.

<!-- evidence:58cc1583a62180e75429f74f source:word/document.xml#p00031 -->
5. Recovery Objectives

<!-- evidence:6971ffe59d86b68459684ff1 source:word/document.xml#p00032 -->
The company sets the following recovery objectives. These are internal objectives that guide planning and prioritization. They are not service level guarantees and are not commitments to any customer. Where a customer contract or service level agreement specifies different recovery commitments, that contract takes precedence over this section.

<!-- evidence:1aa3c9e5d760bc0f65fd8d03 source:word/document.xml#p00033 | table 2, XML row 1, XML cell 1 -->
Objective

<!-- evidence:fa108b6905642551e3413fe6 source:word/document.xml#p00034 | table 2, XML row 1, XML cell 2 -->
Target

<!-- evidence:892da82b3e0755036599fc2a source:word/document.xml#p00035 | table 2, XML row 1, XML cell 3 -->
Basis

<!-- evidence:35e8f343f10f953cfc51a7d0 source:word/document.xml#p00036 | table 2, XML row 2, XML cell 1 -->
Recovery Point Objective (RPO)

<!-- evidence:8037e318140224e2d8447e95 source:word/document.xml#p00037 | table 2, XML row 2, XML cell 2 -->
Up to 24 hours

<!-- evidence:13d9ceab37b919ce7301c5ed source:word/document.xml#p00038 | table 2, XML row 2, XML cell 3 -->
Production databases are backed up automatically on a daily basis, so up to 24 hours of data may be lost in a recovery scenario. Point-in-time recovery is used where the managed database service provides it, which reduces actual data loss in most cases.

<!-- evidence:3844b0831688f13e21c8968b source:word/document.xml#p00039 | table 2, XML row 3, XML cell 1 -->
Recovery Time Objective (RTO)

<!-- evidence:aed6e735c992a0abd91055dd source:word/document.xml#p00040 | table 2, XML row 3, XML cell 2 -->
Up to 24 hours

<!-- evidence:f6e3a08b8c7298fbf22296fe source:word/document.xml#p00041 | table 2, XML row 3, XML cell 3 -->
Reflects the time required to restore data, redeploy the application from source control, and verify service, with recovery performed by the founders rather than a standby team.

<!-- evidence:6673f40f738217843a42d5eb source:word/document.xml#p00043 -->
These objectives reflect what the company can currently achieve and evidence. They are reviewed at least annually and are expected to tighten as the company matures, as automation is introduced, and as customer commitments require.

<!-- evidence:923e8ca5bb20f9d017890c8e source:word/document.xml#p00044 -->
6. Backup

<!-- evidence:178b3ef6f32c1e3942078340 source:word/document.xml#p00045 -->
The company relies on the following backup arrangements:

<!-- evidence:dda97327eadc451903a1bfcf source:word/document.xml#p00046 | table 3, XML row 1, XML cell 1 -->
Asset

<!-- evidence:4045d4353e50ffccb005534b source:word/document.xml#p00047 | table 3, XML row 1, XML cell 2 -->
Arrangement

<!-- evidence:fcbcfa1a9ec6007cb3a94f61 source:word/document.xml#p00048 | table 3, XML row 1, XML cell 3 -->
Retention

<!-- evidence:8dc1fe726804f9552cfd97dd source:word/document.xml#p00049 | table 3, XML row 2, XML cell 1 -->
Production databases

<!-- evidence:f60c94c54a2d3908b8d54464 source:word/document.xml#p00050 | table 3, XML row 2, XML cell 2 -->
Automated daily backups taken by the managed database service, with point-in-time recovery where available.

<!-- evidence:e416559bacf286e27ba998ae source:word/document.xml#p00051 | table 3, XML row 2, XML cell 3 -->
Rolling 35 days

<!-- evidence:570ecd173b2f203760cc4994 source:word/document.xml#p00052 | table 3, XML row 3, XML cell 1 -->
Object storage

<!-- evidence:c8f88ff21c0415fa35ca5c35 source:word/document.xml#p00053 | table 3, XML row 3, XML cell 2 -->
Data written to object storage, including application logs shipped from hosts, is retained by the storage service, which provides durability across multiple facilities within the region.

<!-- evidence:fa3995df356fd0a0b6ebd559 source:word/document.xml#p00054 | table 3, XML row 3, XML cell 3 -->
Long-term, no scheduled expiry

<!-- evidence:45f98d96b4028605b42a1b6c source:word/document.xml#p00055 | table 3, XML row 4, XML cell 1 -->
Application configuration

<!-- evidence:d30a8bdbfa8d60876849dd77 source:word/document.xml#p00056 | table 3, XML row 4, XML cell 2 -->
Held in the cloud provider’s managed parameter store, and recoverable through it.

<!-- evidence:4b52ceaf18fc3fe4fcff5748 source:word/document.xml#p00057 | table 3, XML row 4, XML cell 3 -->
Maintained by the service

<!-- evidence:68d952a29cb69d1608e4fb5a source:word/document.xml#p00058 | table 3, XML row 5, XML cell 1 -->
Application code and infrastructure as code

<!-- evidence:340236acc1c56a6c7b42e0f2 source:word/document.xml#p00059 | table 3, XML row 5, XML cell 2 -->
Held in the source-code platform, which retains full version history and enables the environment to be redeployed.

<!-- evidence:2c268961c3211d09844e7065 source:word/document.xml#p00060 | table 3, XML row 5, XML cell 3 -->
Full history retained

<!-- evidence:443ca2a0065686c21aacd8a0 source:word/document.xml#p00062 -->
Backups are encrypted at rest using the mechanisms described in the Cryptography Policy, and access to backups is restricted in line with the Access Control Policy.

<!-- evidence:b31c4b1f90dd6707a3f7ebdc source:word/document.xml#p00063 -->
The 35-day database backup window is a recovery window, not a records retention period. It governs how far back the company can restore an operational database, and is distinct from the retention of records and logs described in the Data Classification Policy, which is met through object storage and other retained records rather than through database backups.

<!-- evidence:e22af886ed79a118a4ac0c9f source:word/document.xml#p00064 -->
7. Resilience and Recovery Approach

<!-- evidence:a727e4400bdc13b2774da376 source:word/document.xml#p00065 -->
The production environment runs in a single cloud region, and the company’s recovery approach is zonal: it recovers into an alternative availability zone within that region using the managed services and backups described above. The company does not currently operate a multi-region or geographically distributed deployment, and does not maintain backups in a second geographic region. It states this position openly rather than claiming geographic diversity it does not have.

<!-- evidence:876f15e23e0b79170e18d13d source:word/document.xml#p00066 -->
The company accepts, as a recorded risk under the Risk Management Policy, that a disruption affecting an entire cloud region would exceed the recovery objectives in Section 5. Establishing cross-region backup and recovery capability is a planned improvement, to be prioritized against customer requirements as the company grows.

<!-- evidence:284aaafde35603af2879e548 source:word/document.xml#p00067 -->
Recovery is performed by restoring data from the most recent available backup, redeploying the application from source control and its stored configuration, verifying integrity and functionality before service is resumed, and monitoring closely afterwards for recurrence.

<!-- evidence:452febbfebcff4a096fbedd5 source:word/document.xml#p00068 -->
8. Activation and Response

<!-- evidence:74660aa6ab9fda16c95b1b03 source:word/document.xml#p00069 -->
Disruption is detected through cloud-native monitoring, provider status notifications, and reports from personnel or customers. Any event that materially affects the availability or integrity of the production environment or customer data is handled as an incident under the Incident Management Policy, which governs classification, response times, escalation, and communication.

<!-- evidence:7024483ba178cca72bace406 source:word/document.xml#p00070 -->
Where the response requires restoration from backup or recovery into an alternative availability zone, the Chief Executive Officer declares activation of the procedures in this policy, and the Chief Technology Officer leads technical recovery. Actions taken during recovery are recorded so that the sequence of events can be reconstructed afterwards.

<!-- evidence:a7c6f285e5625a1e01811c68 source:word/document.xml#p00071 -->
9. Communication

<!-- evidence:82b3a9618b7fd190d9138bb2 source:word/document.xml#p00072 -->
Internal communication during disruption takes place through the company’s internal channels. Customers and other external parties are notified where a disruption affects their data or service, in accordance with the applicable customer contract or data processing agreement, and in line with the communication requirements of the Incident Management Policy. External communications are approved by senior management.

<!-- evidence:dabdea5193f025540b7bf1b9 source:word/document.xml#p00073 -->
10. Third-Party Dependencies

<!-- evidence:479453745091ef1e6e2b599c source:word/document.xml#p00074 -->
The company depends on its cloud providers and on the software-as-a-service applications used to run the business. Continuity and resilience of those services rest with their providers under their own arrangements. Dependency on critical vendors, and the resilience they offer, is assessed as part of vendor due diligence and the annual risk assessment under the Risk Management Policy. The company monitors provider status communications and follows the guidance issued by a provider during an outage.

<!-- evidence:ba512184c9895c23af4ed5b5 source:word/document.xml#p00075 -->
11. Testing

<!-- evidence:f54ebba71215236360043cdf source:word/document.xml#p00076 -->
The company conducts a combined continuity exercise at least annually, comprising a restore test, in which a backup is restored to a non-production environment and the restored data is verified for integrity and completeness, and a recovery test, in which recovery of the application into an alternative availability zone is exercised.

<!-- evidence:9f487fd5303d15d4b91a175a source:word/document.xml#p00077 -->
The company records openly that, as at the effective date of this policy, no restore or recovery test has yet been performed. The first combined exercise is scheduled within the first annual cycle following the effective date, and the exercise is repeated at least annually thereafter. Until the first exercise is completed, the company treats its recovery objectives as unverified, and this is recorded as a risk under the Risk Management Policy.

<!-- evidence:adea3529308a34b36fd50cce source:word/document.xml#p00078 -->
Each exercise is documented, recording what was tested, the outcome, the time taken measured against the objectives in Section 5, and any shortfalls identified. Shortfalls are tracked to closure and, where material, added to the risk register.

<!-- evidence:f837e4676f0ae4377498a7c4 source:word/document.xml#p00079 -->
12. Review and Continuous Improvement

<!-- evidence:0ce89a33bdc6d0e3006b6d4a source:word/document.xml#p00080 -->
This policy is reviewed at least annually, and additionally following any significant disruption, any material change to the production architecture, or a change in customer commitments. Findings from continuity exercises and from actual disruptions are incorporated into this policy and into the risk register, and post-incident reviews are conducted under the Incident Management Policy.

<!-- evidence:b5eeb923a1dac17c3036a087 source:word/document.xml#p00081 -->
13. Integration with Other Policies

<!-- evidence:f293c980ec0a242f2add042d source:word/document.xml#p00082 -->
This policy addresses the availability of the company's systems and data, and it operates in close conjunction with the Incident Management Policy, which governs how any disruptive event is classified, escalated, communicated, and reviewed. This policy governs what is recovered and how; that policy governs how the event itself is run. The two are intended to be read together during a disruption.

<!-- evidence:63787f2640d10ab18af0ca7e source:word/document.xml#p00083 -->
The scope of what must be recovered is drawn from the assets recorded under the Asset Management Policy, and the sensitivity and retention of the data being backed up and restored are determined by the Data Classification Policy. Backups are encrypted as required by the Cryptography Policy and access to them is restricted under the Access Control Policy, which also governs the approval required to deploy during recovery. Disruption scenarios, dependency on critical vendors, and the accepted exposure arising from a single-region deployment are recorded and treated under the Risk Management Policy. The overall direction for this policy is set by the Information Security Policy.

<!-- evidence:43d302b87ce8670fb0dab1f5 source:word/document.xml#p00084 -->
14. Compliance and Review

<!-- evidence:11571320c3172f8899cfec9f source:word/document.xml#p00085 -->
This policy supports the availability objectives within the company’s SOC 2 scope. It is reviewed at least annually and updated as the company grows or its controls change.

<!-- evidence:e7f4df6d142e2931c66cf9f8 source:word/document.xml#p00086 -->
15. Policy Acknowledgment

<!-- evidence:14beb2f33755ac6bd11e29c3 source:word/document.xml#p00087 -->
All personnel are required to acknowledge this policy at onboarding and on significant updates. Violations may result in disciplinary action under the Human Resource Policy, up to and including termination.

<!-- evidence:eaf6287dbd47142c2ed180bd source:word/document.xml#p00088 -->
Document Control

<!-- evidence:20cad9bbbdc513a6d5b3949e source:word/document.xml#p00089 -->
Revision History

<!-- evidence:fb099f3973c2f800cfaae1f1 source:word/document.xml#p00090 | table 4, XML row 1, XML cell 1 -->
Version

<!-- evidence:a131a052a7e56a503d3b422f source:word/document.xml#p00091 | table 4, XML row 1, XML cell 2 -->
Date

<!-- evidence:66b2800dbc8b789cffbd6bc6 source:word/document.xml#p00092 | table 4, XML row 1, XML cell 3 -->
Author

<!-- evidence:33dab23bc86d2e01aa844e75 source:word/document.xml#p00093 | table 4, XML row 1, XML cell 4 -->
Description of Change

<!-- evidence:8ea0acbd58e99b4c98d18fd2 source:word/document.xml#p00094 | table 4, XML row 2, XML cell 1 -->
1.0

<!-- evidence:55988629ee36ae5b216e44d9 source:word/document.xml#p00095 | table 4, XML row 2, XML cell 2 -->
14-07-2026

<!-- evidence:046bee5bbb444f9184376b9d source:word/document.xml#p00096 | table 4, XML row 2, XML cell 3 -->
Sahil Pugalia

<!-- evidence:8e4e090906c8952054cc2181 source:word/document.xml#p00097 | table 4, XML row 2, XML cell 4 -->
Initial policy

<!-- evidence:45a8074092376dff9114a60a source:word/document.xml#p00098 -->
Approval

<!-- evidence:39428a4af279fbc7e6ea4dc8 source:word/document.xml#p00099 | table 5, XML row 1, XML cell 1 -->
Role

<!-- evidence:3c839a5b442e1e4dccf60cc2 source:word/document.xml#p00100 | table 5, XML row 1, XML cell 2 -->
Name

<!-- evidence:7a7808a978df51697f1bf983 source:word/document.xml#p00101 | table 5, XML row 1, XML cell 3 -->
Date

<!-- evidence:08b04cc7e81e55d4edacbbfe source:word/document.xml#p00102 | table 5, XML row 2, XML cell 1 -->
Chief Business Officer / Chief Privacy Officer

<!-- evidence:8b3c14f4259c8474e7777f36 source:word/document.xml#p00103 | table 5, XML row 2, XML cell 2 -->
Priyanka Choudhury
