CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    category_type VARCHAR NOT NULL,
    category_name VARCHAR NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS spendings (
    id SERIAL PRIMARY KEY,
    main_category VARCHAR NOT NULL,
    subcategory VARCHAR NOT NULL,
    price FLOAT CHECK (price > 0),
    date DATE NOT NULL
);
