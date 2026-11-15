"""Validated administration operations, behind server-side role checks."""
import ipaddress
import time
from urllib.parse import urlsplit

class ValidationError(ValueError):
    pass

def text(data, key, maximum=120, required=True):
    value = data.get(key, '')
    if not isinstance(value, str) or len(value.strip()) > maximum or (required and not value.strip()):
        raise ValidationError('Invalid ' + key)
    return value.strip()

def public_url(value):
    try:
        p = urlsplit(value)
        host = p.hostname
        if (p.scheme != 'https' or not host or p.username or p.password
                or p.port not in (None, 443) or any(c.isspace() for c in value)
                or '.' not in host or host.lower().endswith(('.local', '.localhost'))):
            return False
        try:
            return ipaddress.ip_address(host).is_global
        except ValueError:
            return host.lower() != 'localhost'
    except (ValueError, TypeError):
        return False

def skill_names(db):
    return [r[0] for r in db.execute('SELECT name FROM skill_catalog ORDER BY name')]

def execute(db, uid, route, data):
    action = route.rsplit('/', 1)[-1]
    target = ''
    if action in ('skills', 'skills-delete'):
        name = text(data, 'name', 80)
        target = name
        if action == 'skills':
            db.execute('INSERT OR IGNORE INTO skill_catalog(name) VALUES (?)', (name,))
        else:
            used = sum(db.execute(sql, (name,)).fetchone()[0] for sql in (
                'SELECT COUNT(*) FROM skills WHERE skill=?',
                'SELECT COUNT(*) FROM career_role_skills WHERE skill=?',
                'SELECT COUNT(*) FROM learning_resources WHERE skill=?',
                'SELECT COUNT(*) FROM portfolio WHERE skill=?',
                'SELECT COUNT(*) FROM progress WHERE skill=?'))
            if used:
                raise ValidationError('Skill is in use; remove its references before deleting')
            if len(skill_names(db)) <= 1:
                raise ValidationError('Keep at least one skill')
            db.execute('DELETE FROM skill_catalog WHERE name=?', (name,))
    elif action in ('roles', 'roles-delete'):
        role = text(data, 'role', 80)
        target = role
        if action == 'roles-delete':
            if db.execute('SELECT 1 FROM users WHERE goal=?', (role,)).fetchone():
                raise ValidationError('Career role is selected by a student; reassign their goal first')
            if db.execute('SELECT COUNT(*) FROM career_roles').fetchone()[0] <= 1:
                raise ValidationError('Keep at least one career role')
            db.execute('DELETE FROM career_roles WHERE name=?', (role,))
        else:
            skills = data.get('skills')
            levels = data.get('required_levels', {})
            if (not isinstance(skills, list) or not skills or len(skills) > 100
                    or any(not isinstance(s, str) or s not in skill_names(db) for s in skills)
                    or not isinstance(levels, dict)
                    or any(s not in skills or type(v) is not int or not 1 <= v <= 3 for s, v in levels.items())):
                raise ValidationError('Invalid role requirements or levels (1 to 3)')
            db.execute('INSERT OR IGNORE INTO career_roles(name) VALUES (?)', (role,))
            db.execute('DELETE FROM career_role_skills WHERE role=?', (role,))
            db.executemany('INSERT OR IGNORE INTO career_role_skills(role,skill,required_level) VALUES (?,?,?)',
                           [(role, s, levels.get(s, 2)) for s in skills])
    elif action in ('resources', 'resources-delete'):
        rid = data.get('id')
        if rid is not None and (type(rid) is not int or rid < 1):
            raise ValidationError('Invalid resource id')
        if action == 'resources-delete':
            if rid is None:
                raise ValidationError('Resource id is required')
            db.execute('DELETE FROM learning_resources WHERE id=?', (rid,))
        else:
            skill, title = text(data, 'skill', 80), text(data, 'title', 100)
            url, description = text(data, 'url', 500), text(data, 'description', 500, False)
            kind = data.get('kind', 'course')
            if skill not in skill_names(db) or kind not in ('course', 'resource') or not public_url(url):
                raise ValidationError('Use a catalog skill, course/resource type and public HTTPS URL')
            if rid is None:
                rid = db.execute('INSERT INTO learning_resources(skill,title,url,description,kind) VALUES (?,?,?,?,?)',
                                 (skill, title, url, description, kind)).lastrowid
            else:
                if not db.execute('SELECT 1 FROM learning_resources WHERE id=?', (rid,)).fetchone():
                    raise ValidationError('Resource not found')
                db.execute('UPDATE learning_resources SET skill=?,title=?,url=?,description=?,kind=? WHERE id=?',
                           (skill, title, url, description, kind, rid))
        target = str(rid)
    elif action in ('users', 'users-delete'):
        sid = data.get('id')
        if type(sid) is not int:
            raise ValidationError('Invalid student id')
        student = db.execute('SELECT role FROM users WHERE id=?', (sid,)).fetchone()
        if not student or student[0] != 'student':
            raise ValidationError('Only student accounts can be managed here')
        target = str(sid)
        if action == 'users-delete':
            db.execute('DELETE FROM users WHERE id=?', (sid,))
        else:
            name = text(data, 'name', 80)
            department = text(data, 'department', 100, False)
            year = text(data, 'academic_year', 30, False)
            db.execute('UPDATE users SET name=?,department=?,academic_year=? WHERE id=?', (name, department, year, sid))
    else:
        return 404, {'error': 'Unknown administration endpoint'}
    audit = {'roles': 'edit-role-requirements', 'resources': 'edit-resource' if data.get('id') else 'add-resource'}.get(action, action)
    db.execute('INSERT INTO audit_log(actor_id,action,target,created_at) VALUES (?,?,?,?)', (uid, audit, target, int(time.time())))
    return 200, {'message': 'Saved'}
