from database.DAO import DAO

countries = DAO.getAllCountries()
print(*countries, sep='\n')

retailers = DAO.getRetailers("Italy")
print(*retailers, sep='\n')

# peso = DAO.getPeso(1225, 1135, 2015, "France")
# print(peso)
