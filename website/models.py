from mysql.connector import Error
import mysql.connector


class client():
    idc = 0
    year = 0
    databasename = 'toutprod_bestbuytn_2022'
    prix = []
    puachat = []
    diff = []
    reg = []
    paye = []
    inf = []

    def __init__(self, idc, year):
        self.idc = idc
        self.year = year

    def find_exercice(self):
        yearlist = ['toutprod_bestbuytn_2020',
                    'toutprod_bestbuytn_2021', 'toutprod_bestbuytn_2022']
        for i in range(0, len(yearlist)):
            if str(self.year) in yearlist[i]:
                self.databasename = yearlist[i]

    def info_reg(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database=self.databasename,
                user='root',
                password='692000DDn'
            )

            if connection.is_connected():
                cursor = connection.cursor()
                stmt = '''SELECT sum(montant) FROM reglement_facture where id_fact in ( select id_fact from bestbuytn.facture where idc = %s ) group by type;'''
                cursor.execute(stmt, (self.idc,))
                record = cursor.fetchall()
                p = []
                p_fact = []
                for row in record:
                    a = '%s' % row
                    p_fact.append(a)
                p.append(p_fact)
                cursor1 = connection.cursor()
                stmt1 = '''SELECT sum(montant) FROM reglement_ticket where idc = %s group by type'''
                cursor1.execute(stmt1, (self.idc,))
                record1 = cursor1.fetchall()
                p_ticket = []
                for row in record1:
                    a = '%s' % row
                    p_ticket.append(a)
                p.append(p_ticket)
                cursor2 = connection.cursor()
                stmt2 = '''SELECT sum(montant) FROM reglement_bl where id_bl in ( select id from bon_livraison where idc = %s ) group by type;'''
                cursor2.execute(stmt2, (self.idc,))
                record2 = cursor2.fetchall()
                p_bl = []
                for row in record2:
                    a = '%s' % row
                    p_bl.append(a)
                p.append(p_bl)
                self.inf = p
        except Error as e:
            print('error while connecting ', e)
        finally:
            if connection.is_connected():
                # cursor.close()
                connection.close()

    def ret_inf(self):
        return self.inf

    def reg_paye(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database=self.databasename,
                user='root',
                password='692000DDn'
            )

            if connection.is_connected():
                cursor = connection.cursor()
                stmt = '''SELECT sum(montant) FROM reglement_facture where id_fact in ( select id_fact from bestbuytn.facture where idc = %s ) and created < SYSDATE();'''
                cursor.execute(stmt, (self.idc,))
                record = cursor.fetchall()
                p = []
                for row in record:
                    a = '%s' % row
                    p.append(a)
                cursor1 = connection.cursor()
                stmt1 = '''SELECT sum(montant) FROM reglement_ticket where idc = %s and created < sysdate()'''
                cursor1.execute(stmt1, (self.idc,))
                record1 = cursor1.fetchall()
                for row in record1:
                    a = '%s' % row
                    p.append(a)
                cursor2 = connection.cursor()
                stmt2 = '''SELECT sum(montant) FROM reglement_bl where id_bl in ( select id from bon_livraison where idc = %s ) and created < sysdate();'''
                cursor2.execute(stmt2, (self.idc,))
                record2 = cursor2.fetchall()
                for row in record2:
                    a = '%s' % row
                    p.append(a)
                self.paye = p
        except Error as e:
            print('error while connecting ', e)
        finally:
            if connection.is_connected():
                # cursor.close()
                connection.close()

    def ret_paye(self):
        return self.paye

    def reglement(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database=self.databasename,
                user='root',
                password='692000DDn'
            )

            if connection.is_connected():
                cursor = connection.cursor()
                stmt = '''SELECT sum(montant) FROM reglement_facture where id_fact in ( select id_fact from facture where idc = %s )'''
                cursor.execute(stmt, (self.idc,))
                record = cursor.fetchall()
                p = []
                for row in record:
                    a = '%s' % row
                    p.append(a)
                cursor1 = connection.cursor()
                stmt1 = '''SELECT sum(montant) FROM reglement_ticket where idc = %s'''
                cursor1.execute(stmt1, (self.idc,))
                record1 = cursor1.fetchall()
                for row in record1:
                    a = '%s' % row
                    p.append(a)
                cursor2 = connection.cursor()
                stmt2 = '''SELECT sum(montant) FROM reglement_bl where id_bl in ( select id from bon_livraison where idc = %s )'''
                cursor2.execute(stmt2, (self.idc,))
                record2 = cursor2.fetchall()
                for row in record2:
                    a = '%s' % row
                    p.append(a)
                self.reg = p
        except Error as e:
            print('error while connecting ', e)
        finally:
            if connection.is_connected():
                # cursor.close()
                connection.close()

    def ret_reg(self):
        return self.reg

    def etat_vente(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database=self.databasename,
                user='root',
                password='692000DDn'
            )

            if connection.is_connected():
                db_info = connection.get_server_info()
                print('connected', db_info)
                cursor = connection.cursor()
                stmt = '''SELECT sum((l.prix*(l.quantite-l.qte_avoir))*(1+(l.tva/100))*(1-(l.remis/100)))
                        FROM ligne_facture l, facture f
                        WHERE l.id_fact = f.id_fact and  f.idc=%s and (l.id_fact not in (select id_fact from ticket ) or l.id_fact not in (select id_fact from bon_livraison)   )   '''
                cursor.execute(stmt, (self.idc,))
                record = cursor.fetchall()
                p = []
                for row in record:
                    a = '%s' % row
                    p.append(a)
                cursor1 = connection.cursor()
                stmt1 = '''SELECT sum((l.prix*(l.qte-l.qte_ret))*(1+(l.tva/100))*(1-(l.remise/100)))
                        FROM ligne_ticket l, ticket t
                        WHERE l.idt = t.idt and t.idc=%s'''
                cursor1.execute(stmt1, (self.idc,))
                record1 = cursor1.fetchall()
                for row in record1:
                    a = '%s' % row
                    p.append(a)
                cursor2 = connection.cursor()
                stmt2 = '''SELECT sum((l.prix*(l.qte - l.qte_ret))*(1+(l.tva/100))*(1-(l.remise/100)))
                    FROM ligne_livraison l, bon_livraison b
                    WHERE l.id_cmd = b.id and b.idc=%s'''
                cursor2.execute(stmt2, (self.idc,))
                record2 = cursor2.fetchall()
                for row in record2:
                    a = '%s' % row
                    p.append(a)
                self.prix = p
        except Error as e:
            print('error while connecting ', e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def etat_achat(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database=self.databasename,
                user='root',
                password='692000DDn'
            )

            if connection.is_connected():
                db_info = connection.get_server_info()
                print('connected', db_info)
                cursor = connection.cursor()
                stmt = '''SELECT sum((l.puachat*(l.quantite-l.qte_avoir))*(1+(l.tva/100))*(1-(l.remis/100)))
                        FROM ligne_facture l, facture f
                        WHERE l.id_fact = f.id_fact and  f.idc=%s and (l.id_fact not in (select id_fact from ticket ) or l.id_fact not in (select id_fact from bon_livraison)   )   '''
                cursor.execute(stmt, (self.idc,))
                record = cursor.fetchall()
                p = []
                for row in record:
                    a = '%s' % row
                    p.append(a)
                cursor1 = connection.cursor()
                stmt1 = '''SELECT sum((l.puachat*(l.qte-l.qte_ret))*(1+(l.tva/100))*(1-(l.remise/100)))
                        FROM ligne_ticket l, ticket t
                        WHERE l.idt = t.idt and t.idc=%s'''
                cursor1.execute(stmt1, (self.idc,))
                record1 = cursor1.fetchall()
                for row in record1:
                    a = '%s' % row
                    p.append(a)
                cursor2 = connection.cursor()
                stmt2 = '''SELECT sum((l.puachat*(l.qte - l.qte_ret))*(1+(l.tva/100))*(1-(l.remise/100)))
                    FROM ligne_livraison l, bon_livraison b
                    WHERE l.id_cmd = b.id and b.idc=%s'''
                cursor2.execute(stmt2, (self.idc,))
                record2 = cursor2.fetchall()
                for row in record2:
                    a = '%s' % row
                    p.append(a)
                self.puachat = p
        except Error as e:
            print('error while connecting ', e)
        finally:
            if connection.is_connected():
                cursor.close()

                connection.close()

    def display_etat_vente(self):
        return self.prix

    def display_etat_achat(self):
        return self.puachat

    def difference(self):
        p = []
        for i in range(0, 3):
            p.append(float(self.prix[i].replace(',', '')) -
                     float(self.puachat[i].replace(',', '')))
        self.diff = p
        return self.diff


class search_client():
    name = ''

    def __init__(self, name):
        self.name = name

    def search(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='bestbuytn',
                user='root',
                password='692000DDn'
            )

            if connection.is_connected():
                db_info = connection.get_server_info()
                print('connected', db_info)
                cursor = connection.cursor()
                stmt = 'SELECT * FROM client WHERE  nom=%s '
                cursor.execute(stmt, (self.name, ))
                record = cursor.fetchall()
                return record

        except Error as e:
            print('error while connecting ', e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


class client_name_list():
    def name_list():
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='bestbuytn',
                user='root',
                password='692000DDn'
            )

            if connection.is_connected():
                db_info = connection.get_server_info()
                print('connected', db_info)
                cursor = connection.cursor()
                stmt = 'SELECT nom FROM client '
                cursor.execute(stmt)
                record = cursor.fetchall()
                return record

        except Error as e:
            print('error while connecting ', e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
