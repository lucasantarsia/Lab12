from database.DB_connect import DBConnect
from model.retailer import Retailer


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllCountries():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct r.Country 
                from go_retailers r
                order by r.Country"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["Country"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getRetailers(country):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                from go_retailers r
                where r.Country = %s"""

        cursor.execute(query, (country,))

        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPeso(retailer1: Retailer, retailer2: Retailer, year, country):
        conn = DBConnect.get_connection()

        peso = 0

        cursor = conn.cursor(dictionary=True)
        query = """select count(*) as peso
                from(
                select ds2.Product_number
                from go_daily_sales ds1, go_daily_sales ds2, go_retailers r1, go_retailers r2
                where r1.Retailer_code = ds1.Retailer_code and r2.Retailer_code = ds2.Retailer_code
                and ds1.Product_number = ds2.Product_number 
                and ds1.Retailer_code = %s and ds2.Retailer_code = %s
                and year(ds1.`Date`) = %s and year(ds2.`Date`) = %s
                and r1.Country = %s and r2.Country = %s
                group by ds2.Product_number, year(ds2.`Date`)
                order by ds2.`Date`
                ) t1"""

        cursor.execute(query, (retailer1.Retailer_code, retailer2.Retailer_code, year, year, country, country,))

        for row in cursor:
            peso = row["peso"]

        cursor.close()
        conn.close()
        return peso
