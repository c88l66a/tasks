CREATE TABLE users (
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE information (
    column1 VARCHAR(255) NOT NULL,
    column2 VARCHAR(255) NOT NULL,
    column3 VARCHAR(255) NOT NULL
);

INSERT INTO users (username, password) VALUES
('user_1', 'pass_1'),
('user_2', 'pass_2');

INSERT INTO information (column1, column2, column3) VALUES
('data_1_1', 'data_1_2', 'data_1_3'),
('data_2_1', 'data_2_2', 'data_2_3');

GRANT ALL PRIVILEGES ON TABLE users TO db_user;
GRANT ALL PRIVILEGES ON TABLE information TO db_user;
