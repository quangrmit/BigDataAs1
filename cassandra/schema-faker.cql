USE kafkapipeline;
CREATE TABLE IF NOT EXISTS kafkapipeline.fakerdata (
  name TEXT,
  address TEXT,
  year INT,
  bank TEXT,
  favourite_color TEXT,
  credit_card TEXT,
  company_email TEXT,
  domain_name TEXT,
  avatar TEXT,
  job TEXT, 
  PRIMARY KEY (name, address)
);