# -*- coding: UTF-8 -*-

import sys
import os
import pymysql

from pythinkutils.mysql.ThinkMysql import ThinkMysql
from pythinkutils.common.log import g_logger

def create_table_group():
    conn = ThinkMysql.get_conn_pool().connection()
    try:
        cur = conn.cursor(pymysql.cursors.DictCursor)
        szSql = '''
        DROP TABLE IF EXISTS t_thinkauth_group;
        
        CREATE TABLE t_thinkauth_group (
            `id` bigint(0) UNSIGNED NOT NULL AUTO_INCREMENT
            , `name` varchar(256) NOT NULL 
            , PRIMARY KEY (`id`)
        );
            
        alter table t_thinkauth_group AUTO_INCREMENT=10000001;
        ALTER TABLE `db_thinkutils`.`t_thinkauth_group` ADD INDEX `IX_group_name`(`name`) USING BTREE;
        
        insert into t_thinkauth_group(name) VALUES ('admin');
        insert into t_thinkauth_group(name) VALUES ('guest');
        '''

        for statement in szSql.split(';'):
            if len(statement.strip()) > 0:
                cur.execute(statement + ';')

        conn.commit()

    except Exception as e:
        g_logger.error(e)
    finally:
        conn.close()

def create_table_user():
    conn = ThinkMysql.get_conn_pool().connection()
    try:
        cur = conn.cursor(pymysql.cursors.DictCursor)
        szSql = '''
                DROP TABLE IF EXISTS t_thinkauth_user;

                CREATE TABLE t_thinkauth_user (
                    `id` bigint(0) UNSIGNED NOT NULL AUTO_INCREMENT
                    , `username` varchar(256) NOT NULL 
                    , `password` varchar(256) NOT NULL 
                    , `is_superuser` INTEGER NOT NULL DEFAULT 0
                    , `is_active` INTEGER NOT NULL DEFAULT 1
                    , `date_added` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP 
                    , PRIMARY KEY (`id`)
                );

                alter table t_thinkauth_user AUTO_INCREMENT=10000001;
                ALTER TABLE `db_thinkutils`.`t_thinkauth_user` ADD INDEX `IX_user_name`(`username`) USING BTREE;


                INSERT INTO t_thinkauth_user(username, password, is_superuser) VALUES ('root', 'Ab123145', 1);
                INSERT INTO t_thinkauth_user(username, password) VALUES ('thinkman', 'Ab123145');

          
                '''

        for statement in szSql.split(';'):
            if len(statement.strip()) > 0:
                cur.execute(statement + ';')

        conn.commit()

    except Exception as e:
        pass
    finally:
        conn.close()

def main():
    create_table_group()
    create_table_user()

if __name__ == '__main__':
    main()