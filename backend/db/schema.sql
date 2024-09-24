-- Active: 1726803005051@@127.0.0.1@5432@collab_ide@public
-- Connect to the default 'postgres' database first


-- Create users table

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE files (
    file_id SERIAL PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    is_folder BOOLEAN NOT NULL,
    is_project BOOLEAN NOT NULL,
    parent_folder_id INTEGER,
    file_path VARCHAR(255) NOT NULL, -- Real path in the server
    CONSTRAINT unique_file_name_parent_file_id UNIQUE (file_name, parent_folder_id),
    CONSTRAINT ensure_project_is_folder CHECK (NOT is_project OR is_folder)
);

ALTER TABLE files
ADD CONSTRAINT fk_parent_folder_id
FOREIGN KEY (parent_folder_id)
REFERENCES files(file_id);

CREATE TABLE projects (
    project_id SERIAL PRIMARY KEY,
    project_name VARCHAR(255) NOT NULL UNIQUE,
    user_id INTEGER REFERENCES users(user_id) NOT NULL,
    file_id INTEGER REFERENCES files(file_id) NOT NULL
);


CREATE TABLE project_users (
    user_id INTEGER REFERENCES users(user_id),
    project_id INTEGER REFERENCES projects(project_id),
    role VARCHAR(255) NOT NULL,
    PRIMARY KEY (user_id, project_id)
);



