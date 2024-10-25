use house;
-- Backup the table structure
DROP TABLE IF EXISTS lianjia_data;
CREATE TABLE IF NOT EXISTS lianjia_data AS SELECT * FROM back_up;
SELECT* FROM back_up