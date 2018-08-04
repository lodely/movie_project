#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest
from app import app
from app.models import db, Admin, Role, Users

class DatabaseTestCase(unittest.TestCase):
    """数据库单元测试"""

    def setUp(self):
        # 导入配置
        app.config.from_object('tests.config')
        self.app = app
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_append_admin(self):
        """添加数据"""

        admin = Admin(
            name='testadmin',
            pwd='testadmin',
            is_super=0,
            role_id=1
        )
        role = Role(
            name='ROLE',
        )
        db.session.add_all([admin, role])
        db.session.commit()
        # 管理员名大小写敏感
        ad = Admin.query.filter(Admin.name=='Testadmin').first()
        self.assertIsNone(ad)

    def test_append_user(self):
        """添加数据"""

        user = Users(
            nickname='user'
        )

        db.session.add(user)
        db.session.commit()
        # 用户名大小写敏感
        us = Users.query.filter(Users.nickname=='User').first()
        self.assertIsNone(us)

if __name__ == '__main__':
    unittest.main()