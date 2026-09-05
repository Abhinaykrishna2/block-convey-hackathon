// Graph overview
MATCH (n)
UNWIND labels(n) AS label
RETURN label, count(*) AS count
ORDER BY label;

// Questionnaire decision distribution
MATCH (q:QuestionnaireQuestion)
RETURN q.decision_state AS decision_state, count(*) AS count
ORDER BY decision_state;

// Evidence-backed MFA answer path
MATCH (q:QuestionnaireQuestion)-[:ASKS_ABOUT]->(:ControlArea {id: "mfa"})<-[:MAPS_TO]-(c:Claim)-[:SUPPORTED_BY]->(e:EvidenceBlock)-[:FROM_SOURCE]->(s:Source)
RETURN q.id AS question_id, q.question AS question, c.subject AS subject, c.predicate AS predicate, c.object AS object, e.locator AS locator, s.path AS source
ORDER BY question_id
LIMIT 25;

// Conflict playbook with agent guidance
MATCH (conflict:Conflict)-[:REQUIRES]->(action:ActionItem)
RETURN conflict.id AS conflict_id, conflict.topic AS topic, conflict.severity AS severity, conflict.agent_guidance AS agent_guidance, action.description AS action
ORDER BY conflict_id;

// Contradictory claims and their evidence
MATCH (conflict:Conflict)-[:INVOLVES]->(claim:Claim)-[:SUPPORTED_BY]->(evidence:EvidenceBlock)-[:FROM_SOURCE]->(source:Source)
RETURN conflict.id AS conflict_id, conflict.topic AS topic, claim.subject AS subject, claim.predicate AS predicate, claim.object AS object, evidence.locator AS locator, source.path AS source
ORDER BY conflict_id, source.path
LIMIT 50;

// Questions that still need a human answer
MATCH (q:QuestionnaireQuestion)-[:REQUIRES]->(action:ActionItem)
WHERE q.decision_state IN ["ASK_USER", "UNKNOWN", "ESCALATE"]
RETURN q.id AS question_id, q.question AS question, q.decision_state AS decision_state, action.description AS needed
ORDER BY question_id;

// VAPT remediation status
MATCH (finding:AssessmentFinding)-[:VIOLATES_OR_WEAKENS]->(area:ControlArea)
OPTIONAL MATCH (finding)-[:SUPPORTED_BY]->(evidence:EvidenceBlock)-[:FROM_SOURCE]->(source:Source)
RETURN finding.id AS finding_id, finding.title AS title, finding.severity AS severity, finding.status AS status, area.name AS control_area, evidence.locator AS locator, source.path AS source
ORDER BY finding.severity DESC, finding.id;

// Contract obligations mapped to controls
MATCH (obligation:ContractObligation)-[:REQUIRES_CONTROL]->(area:ControlArea)
OPTIONAL MATCH (obligation)-[:SUPPORTED_BY]->(evidence:EvidenceBlock)-[:FROM_SOURCE]->(source:Source)
RETURN obligation.id AS obligation_id, obligation.title AS obligation, area.name AS control_area, evidence.locator AS locator, source.path AS source
ORDER BY obligation_id, control_area;

// External facts must remain isolated and supplement-only
MATCH (external:ExternalFact)
OPTIONAL MATCH (external)-[rel:SUPPLEMENTS]->(target)
RETURN external.id AS external_fact_id, external.url AS url, type(rel) AS relationship, labels(target) AS supplemented_labels, target.id AS supplemented_id
ORDER BY external_fact_id;
