import csv

class CSV_interface:
    def __init__(self, filename):
        with open(filename, newline='') as csvfile:
            csvreader = csv.DictReader(csvfile)
            self.column_names = csvreader.fieldnames 

        self.filename = filename 
        self.update_data_from_file()
    
    @property
    def all_data(self):
        self.update_data_from_file()
        return self.__all_data 

    @all_data.setter
    def all_data(self, val):
        self.__all_data = val 

    def update_data_from_file(self):
        data = []
        with open(self.filename, newline='') as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                data.append(row)

        self.__all_data = data
        return self.__all_data 

    def generate_product_categories(self):
        category_exists = []
        with open(self.filename, newline='') as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                if row['category'] not in category_exists:
                    category_exists.append(row['category'])    
            return category_exists

    def get_products_by_category(self, category):
        category_products_data = []
        with open(self.filename, newline='') as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                if row['category'] == category:
                    category_products_data.append(row)    
            return category_products_data

    def get_product_details(self, product_id):
        individual_product = []
        with open(self.filename, newline='') as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                if row['id'] == product_id:
                    individual_product.append(row)   
            return individual_product

    def append_one_row_to_file(self, new_data_dict):
        with open(self.filename, "a", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.column_names)
            writer.writerow(new_data_dict)
        return self.all_data