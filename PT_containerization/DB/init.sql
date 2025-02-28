CREATE TABLE emails (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL
);

CREATE TABLE phones (
    id SERIAL PRIMARY KEY,
    phone_number VARCHAR(20) NOT NULL
);

INSERT INTO emails (email) VALUES
('test@example.com'),
('user@example.com');

INSERT INTO phones (phone_number) VALUES
('+7234567890'),
('+8 876 54 32 10');

GRANT ALL PRIVILEGES ON TABLE emails TO admin;
GRANT ALL PRIVILEGES ON TABLE emails_id_seq TO admin;
GRANT ALL PRIVILEGES ON TABLE phones TO admin;
GRANT ALL PRIVILEGES ON TABLE phones_id_seq TO admin;

CREATE ROLE repl_user WITH REPLICATION LOGIN PASSWORD 'qwe';

