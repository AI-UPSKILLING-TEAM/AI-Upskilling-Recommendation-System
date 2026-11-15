"""Requirement and security regression tests for the completed feature set."""
import json
from app import connect_db
import unittest
import test_sprint2 as helpers
from app import promote_admin, initialize

class CompletionTests(unittest.TestCase):
    setUp = helpers.SprintTwoTests.setUp
    tearDown = helpers.SprintTwoTests.tearDown
    call = helpers.SprintTwoTests.call
    student = helpers.SprintTwoTests.student

    def admin(self):
        self.student('admin@example.com')
        self.assertTrue(promote_admin('admin@example.com', self.db))

    def test_academic_profile_and_weak_skill_gap(self):
        self.student()
        profile = {'name':'Manish Demo','goal':'Data Analyst','interests':'analytics',
                   'department':'CSE AI & ML','academic_year':'Year 3','phone':'1234567890'}
        self.assertEqual(self.call('/api/profile',profile)[0],200)
        self.assertEqual(self.call('/api/skills',{'skills':['Python','SQL'],'levels':{'Python':1,'SQL':3}})[0],200)
        d=self.call('/api/dashboard')[1]
        self.assertEqual(d['profile']['department'],profile['department'])
        self.assertEqual(d['levels'],{'Python':1,'SQL':3})
        self.assertEqual(d['analysis']['weak_skills'],['Python'])
        self.assertEqual(d['analysis']['readiness_percent'],20)
        self.assertIn('Python',[r['skill'] for r in d['analysis']['recommendations']])
        self.assertEqual(self.call('/api/skills',{'skills':['Python'],'levels':{'Python':True}})[0],400)
        self.assertEqual(self.call('/api/skills',{'skills':['Python'],'levels':{'Python':4}})[0],400)
        self.assertEqual(self.call('/api/profile',{**profile,'department':[]})[0],400)

    def test_admin_catalog_resource_and_role_lifecycle(self):
        self.admin()
        self.assertEqual(self.call('/api/admin/skills',{'name':'Docker'})[0],200)
        self.assertIn('Docker',self.call('/api/catalog')[1]['skills'])
        role={'role':'Platform Engineer','skills':['Docker','Linux'],'required_levels':{'Docker':3,'Linux':2}}
        self.assertEqual(self.call('/api/admin/roles',role)[0],200)
        self.assertEqual(self.call('/api/catalog')[1]['required_levels']['Platform Engineer']['Docker'],3)
        resource={'skill':'Docker','title':'Container basics','url':'https://docs.docker.com/get-started/','kind':'course'}
        self.assertEqual(self.call('/api/admin/resources',resource)[0],200)
        rid=self.call('/api/resources')[1]['custom'][0]['id']
        self.assertEqual(self.call('/api/admin/resources',{**resource,'id':rid,'title':'Container guide'})[0],200)
        self.assertEqual(self.call('/api/profile',{'name':'A','goal':'Platform Engineer'})[0],200)
        d=self.call('/api/dashboard')[1]['analysis']
        docker=next(r for r in d['recommendations'] if r['skill']=='Docker')
        self.assertEqual(docker['resource'],'Container guide')
        self.assertEqual(docker['required_level'],3)
        self.assertEqual(self.call('/api/admin/roles-delete',{'role':'Platform Engineer'})[0],400)
        self.assertEqual(self.call('/api/profile',{'name':'A','goal':'Data Analyst'})[0],200)
        self.assertEqual(self.call('/api/admin/roles-delete',{'role':'Platform Engineer'})[0],200)
        self.assertEqual(self.call('/api/admin/skills-delete',{'name':'Docker'})[0],400)
        self.assertEqual(self.call('/api/admin/resources-delete',{'id':rid})[0],200)
        self.assertEqual(self.call('/api/admin/skills-delete',{'name':'Docker'})[0],200)
        initialize(self.db)
        self.assertNotIn('Docker',self.call('/api/catalog')[1]['skills'])
        self.assertGreaterEqual(len(self.call('/api/admin/audit')[1]['audit']),7)

    def test_admin_student_edit_and_cascading_account_delete(self):
        self.admin()
        admin_token=self.token
        learner_token=self.student('learner@example.com')
        self.call('/api/portfolio/add',{'kind':'project','title':'Private work','skill':'SQL'})
        self.call('/api/progress',{'skill':'SQL','completed':True})
        self.token=admin_token
        learner=next(u for u in self.call('/api/admin/users')[1]['users'] if u['email']=='learner@example.com')
        self.assertEqual(self.call('/api/admin/users',{'id':learner['id'],'name':'Updated','department':'CSE','academic_year':'3'})[0],200)
        self.assertEqual(self.call('/api/dashboard',token=learner_token)[1]['profile']['name'],'Updated')
        self.assertEqual(self.call('/api/admin/users-delete',{'id':learner['id']})[0],200)
        self.assertEqual(self.call('/api/dashboard',token=learner_token)[0],401)
        with connect_db(self.db) as db:
            for table in ['skills','progress','sessions','portfolio','recommendation_snapshots']:
                self.assertEqual(db.execute('SELECT COUNT(*) FROM '+table+' WHERE user_id=?',(learner['id'],)).fetchone()[0],0)
        aid=self.call('/api/dashboard')[1]['profile']['id']
        self.assertEqual(self.call('/api/admin/users-delete',{'id':aid})[0],400)

    def test_every_admin_mutation_rejects_students_and_anonymous(self):
        self.student()
        routes=['skills','skills-delete','users','users-delete','roles','roles-delete','resources','resources-delete']
        for route in routes:
            self.assertEqual(self.call('/api/admin/'+route,{})[0],403,route)
            self.assertEqual(self.call('/api/admin/'+route,{},token=None)[0],401,route)

    def test_malformed_input_does_not_crash_server(self):
        self.student()
        for key,value in [('skills',[{}]),('skills',True),('skills',None)]:
            self.assertEqual(self.call('/api/skills',{key:value})[0],400)
        self.assertEqual(self.call('/api/register',{'name':{},'email':[],'password':42})[0],400)
        self.assertEqual(self.call('/api/login',{'email':[],'password':'a'*10000})[0],401)
        self.assertEqual(self.call('/api/profile',{'name':'X','goal':'Data Analyst','interests':{}})[0],400)
        self.assertEqual(self.call('/health')[0],200)

    def test_persistence_reinitialize_and_progress_for_matching_skills(self):
        self.student()
        self.call('/api/profile',{'name':'A','goal':'Data Analyst'})
        self.call('/api/skills',{'skills':['Python'],'levels':{'Python':3}})
        self.call('/api/progress',{'skill':'Python','completed':True})
        initialize(self.db)
        d=self.call('/api/dashboard')[1]
        self.assertEqual(d['levels']['Python'],3)
        self.assertEqual(d['completed'],['Python'])
        self.assertEqual(d['analysis']['practice_progress_percent'],20)
        with connect_db(self.db) as db:
            snapshot=json.loads(db.execute('SELECT payload FROM recommendation_snapshots').fetchone()[0])
            self.assertEqual(snapshot['career_goal'],'Data Analyst')

    def test_admin_rejects_invalid_public_urls(self):
        self.admin()
        for url in ['https://10.0.0.1/x','https://127.0.0.2/x','https://localhost/a','https://[broken','javascript:alert(1)','https://user:pw@example.com','https://example.com:bad','https://example.com:8080']:
            code,_=self.call('/api/admin/resources',{'skill':'Python','title':'Test','url':url})
            self.assertEqual(code,400,url)

if __name__=='__main__':
    unittest.main()
