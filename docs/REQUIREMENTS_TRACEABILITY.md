# SRS Requirement Traceability Matrix
Source: SRS_Project_ID_22.pdf, pages 9-13 and diagrams pages 6/8. New SAD/Test Plan document the actual implementation. Implemented/tested describes the candidate, not independent acceptance.

| ID | Original requirement | Implementation / evidence | Candidate status |
|---|---|---|---|
| FR-01 | The system shall allow a new student to register. | app.py authentication; test_app auth; test_nfr | Implemented; review pending |
| FR-02 | The system shall validate registration information. | app.py authentication; test_app auth; test_nfr | Implemented; review pending |
| FR-03 | The system shall allow registered students to log in. | app.py authentication; test_app auth; test_nfr | Implemented; review pending |
| FR-04 | The system shall display an error message for invalid login credentials. | app.py authentication; test_app auth; test_nfr | Implemented; review pending |
| FR-05 | The system shall allow students to create a profile. | app.py profile; test_completion academic profile; browser | Implemented; review pending |
| FR-06 | The system shall allow students to edit their profile. | app.py profile; test_completion academic profile; browser | Implemented; review pending |
| FR-07 | The system shall store student academic and career information. | app.py profile; test_completion academic profile; browser | Implemented; review pending |
| FR-08 | The system shall allow students to add skills. | app.py skills/levels; test_completion weak skill; browser | Implemented; review pending |
| FR-09 | The system shall allow students to update or remove skills. | app.py skills/levels; test_completion weak skill; browser | Implemented; review pending |
| FR-10 | The system shall store student skill information. | app.py skills/levels; test_completion weak skill; browser | Implemented; review pending |
| FR-11 | The system shall display available career roles. | career_catalog/profile; test_app validation; browser | Implemented; review pending |
| FR-12 | The student shall be able to select a career goal. | career_catalog/profile; test_app validation; browser | Implemented; review pending |
| FR-13 | The system shall store the selected career goal. | career_catalog/profile; test_app validation; browser | Implemented; review pending |
| FR-14 | The system shall identify the student's existing skills. | gap_report; test_completion academic profile; test_app gap_report | Implemented; review pending |
| FR-15 | The system shall identify skills required for the selected career role. | gap_report; test_completion academic profile; test_app gap_report | Implemented; review pending |
| FR-16 | The system shall identify missing or weak skills. | gap_report; test_completion academic profile; test_app gap_report | Implemented; review pending |
| FR-17 | The system shall display the identified skill gaps. | gap_report; test_completion academic profile; test_app gap_report | Implemented; review pending |
| FR-18 | The system shall analyze the student's skill gaps. | recommendations.py; test_sprint2 ranking/projects; evaluation JSON | Implemented; review pending |
| FR-19 | The system shall generate personalized recommendations. | recommendations.py; test_sprint2 ranking/projects; evaluation JSON | Implemented; review pending |
| FR-20 | The system shall recommend relevant courses and learning resources. | recommendations.py; test_sprint2 ranking/projects; evaluation JSON | Implemented; review pending |
| FR-21 | The system shall recommend suitable projects. | recommendations.py; test_sprint2 ranking/projects; evaluation JSON | Implemented; review pending |
| FR-22 | The system shall recommend relevant certifications where applicable. | recommendations.py; test_sprint2 ranking/projects; evaluation JSON | Implemented; review pending |
| FR-23 | The system shall display recommended learning resources. | app.js cards; test_frontend_contract; browser; link audit | Implemented; review pending |
| FR-24 | The system shall categorize learning resources according to skills. | app.js cards; test_frontend_contract; browser; link audit | Implemented; review pending |
| FR-25 | The system shall allow students to view recommended resources. | app.js cards; test_frontend_contract; browser; link audit | Implemented; review pending |
| FR-26 | The system shall allow students to mark learning activities as completed. | app.py progress/dashboard; test_app progress; test_completion persistence | Implemented; review pending |
| FR-27 | The system shall calculate learning progress. | app.py progress/dashboard; test_app progress; test_completion persistence | Implemented; review pending |
| FR-28 | The system shall display learning progress on the dashboard. | app.py progress/dashboard; test_app progress; test_completion persistence | Implemented; review pending |
| FR-29 | The system shall update recommendations based on learning progress where applicable. | app.py progress/dashboard; test_app progress; test_completion persistence | Implemented; review pending |
| FR-30 | The system shall display the student's career goal. | app.js render; browser-results and screenshots | Implemented; review pending |
| FR-31 | The system shall display identified skill gaps. | app.js render; browser-results and screenshots | Implemented; review pending |
| FR-32 | The system shall display recommended learning resources. | app.js render; browser-results and screenshots | Implemented; review pending |
| FR-33 | The system shall display learning progress. | app.js render; browser-results and screenshots | Implemented; review pending |
| FR-34 | The administrator shall manage student information. | administration.py; test_completion CRUD/authorization; browser | Implemented; review pending |
| FR-35 | The administrator shall manage skills. | administration.py; test_completion CRUD/authorization; browser | Implemented; review pending |
| FR-36 | The administrator shall manage career roles. | administration.py; test_completion CRUD/authorization; browser | Implemented; review pending |
| FR-37 | The administrator shall manage courses and learning resources. | administration.py; test_completion CRUD/authorization; browser | Implemented; review pending |
| FR-38 | The administrator shall update career-role skill requirements. | administration.py; test_completion CRUD/authorization; browser | Implemented; review pending |
| NFR-01 | The system should respond to normal user requests within a reasonable time. | performance.json serial/concurrent benchmark | Verified in documented local scope |
| NFR-02 | Recommendation results should be generated without unnecessary delay. | performance.json includes recommendations | Verified in documented local scope |
| NFR-03 | User passwords shall be stored securely. | test_nfr salted password hash | Verified in documented local scope |
| NFR-04 | Only authenticated users shall access their personal information. | test_sprint2 isolation; test_nfr expiry; test_app logout | Verified in documented local scope |
| NFR-05 | Administrator functions shall be accessible only to authorized administrators. | test_completion all admin mutations | Verified in documented local scope |
| NFR-06 | The system shall provide a simple and user-friendly interface. | browser acceptance; accessibility.json; human acceptance remains | Verified in documented local scope |
| NFR-07 | Navigation between different pages shall be clear and consistent. | navigation anchors; mobile/desktop screenshots | Verified in documented local scope |
| NFR-08 | The system should provide recommendations based on the available data. | deterministic rank tests; custom-skill fallback | Verified in documented local scope |
| NFR-09 | Student progress should not be lost during normal system operation. | test_completion persistence; backup verification | Verified in documented local scope |
| NFR-10 | The system should use modular components so that individual features can be updated easily. | separate modules, CI matrix, repeatable tests | Verified in documented local scope |
