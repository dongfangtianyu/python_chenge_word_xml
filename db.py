import sqlite3
import sys
import os

class db:
    data = {}
    data['company'] = {}
    data['CompanyByName'] = {}

    def __init__(self):

        try:
            home_dir = os.path.split(os.path.realpath(sys.argv[0]))[0]+'\\'
            self.conn = sqlite3.connect('./inc/data.db')
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            self.datainfo = {'user': ('id', 'name'),
                             'company': ('ID', 'Name', 'Address', 'Tel', 'BankName', 'BankNo', 'TaxID')}
        except Exception, e:
            print e

####
    def insert(self, data=None, table='company'):
        fields = vals = ''
        t=[]
        if self.exists_table(table) is False or data is None:
            return False

        for field in self.datainfo[table][1:]:
            fields += field + ','
            vals += '?,'
            t.append(data[field])

        fields = fields[:-1]
        vals = vals[:-1]
        t = tuple(t)

        sql = 'insert into ' + table + ' (' + fields + ') values (' + vals + ')'
        # print(t)
        # sys.exit(0)
        self.cursor.execute(sql, t)
        self.conn.commit()
####

    def update(self, data=None, table='company'):
        if self.exists_table(table) is False or data is None:
            return False

        fields = vals = ''
        t=[]
        index=self.datainfo[table][0]

        for field in self.datainfo[table][1:]:
            fields += field + '= ?,'
            t.append(data[field])

        fields = fields[:-1]
        t.append(data[index])

        t = tuple(t)

        sql = 'update ' + table + ' set '+ fields + ' where ' + index +' = ?'
        # print(t)
        # sys.exit(0)
        self.cursor.execute(sql,t)
        self.conn.commit()

####
    def delete(self, id=None, table='company'):
        if (self.exists_table(table) is False) or (id is None):
            return 'tables is not existe or ID in None'
        else:
            index = self.datainfo[table][0]

            sql = 'delete from ' + table + '  where ' + index +' = ?'
            self.cursor.execute(sql, (id,))
            self.conn.commit()
            del self.data[table][id]
            return True


####
    def get(self, id=None, table='company'):
        if self.exists_table(table) is not True or id is None:
            pass
            return 'tables is not existe or ID in None'

        if self.data.has_key(table) and self.data[table].has_key(id):
            return self.data[table][id]
        else:
            sql = 'select * from '+ table +' where ID= ?'
            self.cursor.execute(sql, (id,))
            for row in self.cursor:
                pass
                x = {}
                for field in self.datainfo[table]:
                    x[field] = row[field]
                self.data[table][id] = x

                if table=='company' and (self.data.has_key('CompanyByName') is False or self.data['CompanyByName'].has_key(x['Name']) is False):
                    self.data['CompanyByName'][x['Name']] = x
                break

            return self.data[id]


####
    def get_company_by_name(self, name=None):
        table = 'company'
        if self.exists_table(table) is not True or name is None:
            pass
            return 'tables is not existe or name in None'

        if self.data.has_key('CompanyByName') and self.data['CompanyByName'].has_key(name):
            return self.data['CompanyByName'][name]
        else:
            x = {}
            sql = 'select * from '+ table +' where Name= ?'
            self.cursor.execute(sql, (name,))
            #name=name.encode('utf-8')
            for row in self.cursor:
                pass
                for field in self.datainfo[table]:
                    x[field] = row[field]
                self.data['CompanyByName'][name] = x
                break
            return x

####
    def get_list(self, table='company', where=None):
        if self.exists_table(table):
            sql = 'select * from ' + table
            self.cursor.execute(sql)
            for row in self.cursor:
                pass
                x = {}
                for field in self.datainfo[table]:
                    x[field] = row[field]
                self.data[table][row['id']] = x

                if table=='company':
                    self.data['CompanyByName'][x['Name']] = x
            return  self.data[table]
        else:
            pass
            return False

####
    def exists_table(self, table=None):
        if table is None:
            return False

        self.cursor.execute('select count(*)  from sqlite_master where type=\'table\' and name =?', (table,))
        cont = self.cursor.fetchall()
        if cont[0][0] == 1:
            return True
        else:
            return False

####
    def close_db(self):
        self.cursor.close()
        self.conn.close()

####
    def create_table(self):
        if self.exists_table('company') is not True:
            self.cursor.execute('''
CREATE TABLE company (
ID INTEGER primary key autoincrement,
Name varchar(255),
Address varchar(255),
Tel varchar(30),
BankName varchar(255),
BankNo varchar(250),
TaxID varchar(250)
);
''')
        self.conn.commit()
        print('table create ok!')

# if __name__ =="__main__":
#     mydb = db()
#     test = mydb.get(2)
#     print (test)
