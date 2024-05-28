import pytest
from unittest.mock import patch, MagicMock
from libcovulor.finding import Finding, FindingModel

@pytest.fixture
def mock_db(mocker):
    mock_collection = mocker.patch('libcovulor.finding.findings_collection')
    return mock_collection

def test_create_finding(mock_db):
    data = {
        "tool": "test",
        "title": "test title",
        "repo_id": "",
        "line": 1,
        "client_id": "123",
        "date": "0000-00-00",
        "description": "",
        "end_column": 0,
        "file_path": "test/test",
        "finding_id": "",
        "language": "",
        "original_line": 1,
        "severity": "",
        "start_column": 0,
        "_id": "",
    }

    mock_db.find_one.return_value = None
    mock_db.insert_one.return_value.inserted_id = "507f1f77bcf86cd799439011"

    result = Finding.create(data)

    assert result.object_id == "507f1f77bcf86cd799439011"
    mock_db.find_one.assert_called_once_with({'cwe': [], 'file_path': 'test/test', 'original_line': 1, 'tool': 'test'})
    mock_db.insert_one.assert_called_once()

# def test_create_finding_already_exists(mock_db):
#     data = {
#         "tool": "test",
#         "title": "test title",
#         "repo_id": "",
#         "line": 1,
#         "client_id": "123",
#         "date": "0000-00-00",
#         "description": "",
#         "end_column": 0,
#         "file_path": "test/test",
#         "finding_id": "",
#         "language": "",
#         "original_line": 1,
#         "severity": "",
#         "start_column": 0,
#         "_id": "",
#     }
#     mock_db.find_one.return_value = {"_id": "507f1f77bcf86cd799439011"}

#     result = Finding.create(data)

#     assert result is None
#     mock_db.find_one.assert_called_once_with({'cwe': [], 'file_path': 'test/test', 'original_line': 1, 'tool': 'test'})

# def test_delete_finding(mock_db):
#     client_id = "123"
#     finding_id = "507f1f77bcf86cd799439011"
#     mock_db.delete_one.return_value = {"deleted_count": 1}

#     data = {
#         Finding.ACCESS_CREDENTIAL: None,
#         Finding.ACTUAL_LINE: 1,
#         Finding.ASVS_ID: None,
#         Finding.ASVS_SECTION: None,
#         Finding.CLIENT_ID: "123",
#         Finding.CONFIDENCE: 100,
#         Finding.CVSSV3_SCORE: 0.0,
#         Finding.CVSSV3_VECTOR: [],
#         Finding.CWES: [],
#         Finding.DATA_SOURCE: None,
#         Finding.DATE: "0000-00-00",
#         Finding.DESCRIPTION: "",
#         Finding.DUPLICATE_ID: None,
#         Finding.END_COLUMN: 0,
#         Finding.EPSS: 0,
#         Finding.EXCLUDED_FILE_TYPES: [],
#         Finding.FILE: "test/test",
#         Finding.FIXING_EFFORT: None,
#         Finding.IAC: None,
#         Finding.ID: "",
#         Finding.IMPACT: None,
#         Finding.IS_DUPLICATE: False,
#         Finding.IS_FALSE_POSITIVE: False,
#         Finding.IS_MITIGATED_EXTERNALLY: False,
#         Finding.ISSUE_OWNER: None,
#         Finding.LANGUAGE: None,
#         Finding.LIKELIHOOD: None,
#         Finding.MITIGATION: None,
#         Finding.NB_OCCURENCES: None,
#         Finding.NOTES: [],
#         Finding.NUMERICAL_SEVERITY: 0,
#         Finding.ORIGINAL_LINE: 1,
#         Finding.OWASPS: [],
#         Finding.PLATFORM: None,
#         Finding.PRIORITY: 0,
#         Finding.PROCESSING_STATUS: "processing",
#         Finding.PROVIDER: None,
#         Finding.RECORD_SOURCE: None,
#         Finding.REFERENCES: [],
#         Finding.REMEDIATION_TYPE: None,
#         Finding.REPOSITORY_ID: "",
#         Finding.RESOURCE_ENTITY: None,
#         Finding.REVIEW_REQUESTED_BY: None,
#         Finding.SAST_SINK_OBJECT: None,
#         Finding.SAST_SOURCE_FILE: None,
#         Finding.SAST_SOURCE_LINE: None,
#         Finding.SAST_SOURCE_OBJECT: None,
#         Finding.SCAN_ID: None,
#         Finding.SCANNER_REPORT: None,
#         Finding.SCANNER_REPORT_CODE: None,
#         Finding.SCANNER_WEAKNESS: None,
#         Finding.SERVICE: None,
#         Finding.SEVERITY: "",
#         Finding.SLSA_THREATS: [],
#         Finding.START_COLUMN: 0,
#         Finding.STATUS: "In Progress",
#         Finding.SUPPLY_CHAINS: ["Source Code"],
#         Finding.TAGS: [],
#         Finding.TARGET_FILE_TYPES: [],
#         Finding.TITLE: "test title",
#         Finding.TOOL: "test",
#         Finding.TYPE: "Code Weakness",
#         Finding.NB_OCCURENCES: 0,
#         "_id": "507f1f77bcf86cd799439011"
#     }

#     existing_document = {
#         "object_id": "507f1f77bcf86cd799439011",
#         "access_credential": None,
#         "actual_line": 1,
#         "asvs_id": None,
#         "asvs_section": None,
#         "client_id": "123",
#         "confidence": 100,
#         "cvssv3_score": 0.0,
#         "cvssv3_vector": [],
#         "cwes": [],
#         "data_source": None,
#         "date": "0000-00-00",
#         "description": "",
#         "duplicate_id": None,
#         "end_column": 0,
#         "epss": 0,
#         "excluded_file_types": [],
#         "file": "test/test",
#         "fixing_effort": None,
#         "iac": None,
#         "id": "",
#         "impact": None,
#         "is_duplicate": False,
#         "is_false_positive": False,
#         "is_mitigated_externally": False,
#         "issue_owner": None,
#         "language": None,
#         "likelihood": None,
#         "mitigation": None,
#         "nb_occurences": 0,
#         "notes": [],
#         "numerical_severity": 0,
#         "original_line": 1,
#         "owasps": [],
#         "platform": None,
#         "priority": 0,
#         "processing_status": "processing",
#         "provider": None,
#         "record_source": None,
#         "references": [],
#         "remediation_type": None,
#         "repository_id": "",
#         "resource_entity": None,
#         "review_requested_by": None,
#         "sast_sink_object": None,
#         "sast_source_file": None,
#         "sast_source_line": None,
#         "sast_source_object": None,
#         "scan_id": None,
#         "scanner_report": None,
#         "scanner_report_code": None,
#         "scanner_weakness": None,
#         "service": None,
#         "severity": "",
#         "slsa_threats": [],
#         "start_column": 0,
#         "status": "In Progress",
#         "supply_chains": ["Source Code"],
#         "tags": [],
#         "target_file_types": [],
#         "title": "test title",
#         "tool": "test",
#         "type": "Code Weakness"
#     }


#     with patch('libcovulor.finding.delete_one', return_value=data) as mock_delete_one:
#         result = Finding.delete(client_id, finding_id)
#         assert result == existing_document
#         mock_delete_one.assert_called_once_with(mock_db, client_id, finding_id)

# def test_find_many_findings(mock_db):
#     client_id = "123"
#     options = None
#     mock_db.find.return_value = {"data": [{"attributes": {"title": "finding1"}}, {"attributes": {"title": "finding2"}}]}

#     with patch('libcovulor.finding.find_many', return_value={"data": [{"attributes": {"title": "finding1"}}, {"attributes": {"title": "finding2"}}]}) as mock_find_many:
#         result = Finding.find_many(client_id, options)

#         assert "data" in result
#         assert len(result["data"]) == 2
#         mock_find_many.assert_called_once_with(mock_db, client_id, options)

# def test_find_one_finding(mock_db):
#     client_id = "123"
#     finding_id = "507f1f77bcf86cd799439011"
#     mock_db.find_one.return_value = {"_id": finding_id, "title": "finding1"}

#     with patch('libcovulor.finding.find_one', return_value={"_id": finding_id, "title": "finding1"}) as mock_find_one:
#         result = Finding.find_one(client_id, finding_id)

#         assert result == {"_id": finding_id, "title": "finding1"}
#         mock_find_one.assert_called_once_with(mock_db, client_id, finding_id)

# def test_update_finding(mock_db):
#     client_id = "123"
#     finding_id = "507f1f77bcf86cd799439011"
#     data = {
#         "title": "updated_title"
#     }
#     mock_db.update_one.return_value = {"modified_count": 1}

#     with patch('libcovulor.finding.update_one', return_value={"modified_count": 1}) as mock_update_one:
#         result = Finding.update(client_id, finding_id, data)

#         assert result == {"modified_count": 1}
#         mock_update_one.assert_called_once_with(mock_db, client_id, finding_id, data)
