
USE kafkapipeline;
CREATE TABLE IF NOT EXISTS kafkapipeline.airdata (
  ind TEXT,
  location TEXT,  
  forcastdate TEXT,
  pm10 FLOAT,
  pm2_5 FLOAT,

  PRIMARY KEY (ind, location)
);

