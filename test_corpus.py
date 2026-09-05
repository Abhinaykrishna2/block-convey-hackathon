"""Small regression check for the actual data failures found during review."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    index = json.loads((ROOT / 'corpus_text/00_INDEX/master_corpus_index.json').read_text())
    assert 'was remediated on 09/04/2026' not in json.dumps(index), 'Requested revocation was incorrectly presented as completed'
    assert index.get('source_count') == 26, 'Source inventory must reconcile all 26 supplied files'
    assert index.get('runtime_evidence') == 'evidence/blocks.jsonl', 'Keep curator instructions separate from evidence'
    from corpus_io import read_source, raw_paths
    blocks = [b for p in raw_paths() for b in read_source(p)]
    backup = [b for b in blocks if b['source'].endswith('Regodit_business_continuity_and_disaster_recovery_policy_v1.0.docx')]
    assert any('Automated daily backups' in b['text'] for b in backup)
    assert any('no restore or recovery test has yet been performed' in b['text'] for b in backup)
    policy = [b for b in blocks if b['source'].endswith('Regodit_password_and_secrets_policy_v1.0.docx')]
    assert any('12' in b['text'] and 'character' in b['text'] for b in policy)
    questions = json.loads((ROOT / 'evidence/questionnaire.json').read_text())['questions']
    assert len(questions) == 66 and len({q['id'] for q in questions}) == 66
    q52 = next(q for q in questions if str(q['id']) in ('52', '52.0'))
    assert q52['wording_status'] == 'recovered_from_reference_sheet'
    assert q52['question'] == "Will you be using an Regodit asset to access Regodit's network?"
    assert q52['source_cell'] == 'B67' and q52['wording_source_cell'] == 'B70'
    print('PASS: remediation status, source count, input isolation, source policy wording and question 52 recovery')


if __name__ == '__main__':
    main()
