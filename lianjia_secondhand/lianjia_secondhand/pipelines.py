import pymysql

class MySQLPipeline:
    def open_spider(self, spider):
        self.connection = pymysql.connect(host='localhost', user='root', password='2001', database='house')
        self.cursor = self.connection.cursor()
        
        # SQL query to drop the table if it exists
        drop_table_query = "DROP TABLE IF EXISTS back_up"
        self.cursor.execute(drop_table_query)
        
        # Create table if not exists
        create_table_query = """
        CREATE TABLE IF NOT EXISTS back_up (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL UNIQUE,
            total_price VARCHAR(50),
            unit_price VARCHAR(50),
            area VARCHAR(50),
            b_type VARCHAR(50),
            configuration VARCHAR(50),
            renovation VARCHAR(50),
            floor VARCHAR(50),
            orientation VARCHAR(50),
            location VARCHAR(100)
        )
        """
        self.cursor.execute(create_table_query)
    
    def close_spider(self, spider):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
    
    def clean_data(self, item):
        # Perform data cleaning operations here
        cleaned_item = {
            'title': item['title'].strip(),
            'total_price': item['total_price'].strip(),
            'unit_price': item['unit_price'].strip(),
            'location': item['location'].strip()
        }
        
        # Extracting data from the 'info' field
        info_data = item.get('info', '').split(' | ')
        if len(info_data) == 6:
            cleaned_item['configuration'] = info_data[0].strip()
            cleaned_item['area'] = info_data[1].split('平米')[0].strip()
            cleaned_item['orientation'] = info_data[2].strip()
            cleaned_item['renovation'] = info_data[3].strip()
            cleaned_item['floor'] = info_data[4].strip()
            cleaned_item['b_type'] = info_data[5].strip()
        
        return cleaned_item
    
    def process_item(self, item, spider):
        if item is None:
            return None
        
        cleaned_item = self.clean_data(item)
        
        insert_query = "INSERT INTO back_up (title, total_price, unit_price, area, b_type, configuration, renovation, floor, orientation, location) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        data = (cleaned_item['title'], cleaned_item['total_price'], cleaned_item['unit_price'], cleaned_item['area'], cleaned_item['b_type'], cleaned_item['configuration'], cleaned_item['renovation'], cleaned_item['floor'], cleaned_item['orientation'], cleaned_item['location'])
        self.cursor.execute(insert_query, data)
        
        return item