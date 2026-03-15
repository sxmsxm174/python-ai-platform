# database.py - 数据库管理
import sqlalchemy as db
import pandas as pd
from datetime import datetime
import os

class StudyDatabase:
    def __init__(self):
        # 创建数据库文件
        self.engine = db.create_engine('sqlite:///study_progress.db')
        self.connection = self.engine.connect()
        self.metadata = db.MetaData()
        self.create_tables()
    
    def create_tables(self):
        # 创建用户表
        self.users = db.Table(
            'users', self.metadata,
            db.Column('id', db.Integer, primary_key=True),
            db.Column('username', db.String),
            db.Column('created_at', db.String)
        )
        
        # 创建学习记录表
        self.records = db.Table(
            'records', self.metadata,
            db.Column('id', db.Integer, primary_key=True),
            db.Column('user_id', db.Integer),
            db.Column('question_type', db.String),
            db.Column('code', db.Text),
            db.Column('result', db.String),
            db.Column('created_at', db.String)
        )
        
        self.metadata.create_all(self.engine)
        print("数据库表创建成功！")
    
    def add_user(self, username):
        query = db.insert(self.users).values(
            username=username,
            created_at=str(datetime.now())
        )
        result = self.connection.execute(query)
        return result.inserted_primary_key[0]
    
    def add_record(self, user_id, question_type, code, result):
        query = db.insert(self.records).values(
            user_id=user_id,
            question_type=question_type,
            code=code,
            result=result[:100] + '...' if len(result) > 100 else result,
            created_at=str(datetime.now())
        )
        self.connection.execute(query)
    
    def get_user_stats(self, user_id):
        # 正确的查询语法
        query = db.select(self.records).where(self.records.c.user_id == user_id)
        result = self.connection.execute(query)
        rows = result.fetchall()
        
        if len(rows) > 0:
            # 统计不同类型的题目数量
            type_count = {}
            for row in rows:
                q_type = row[2]  # question_type列
                type_count[q_type] = type_count.get(q_type, 0) + 1
            
            return {
                'total': len(rows),
                'by_type': type_count
            }
        return {'total': 0, 'by_type': {}}