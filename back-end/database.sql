CREATE TABLE products (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  user_id TEXT NOT NULL,
  
  name TEXT NOT NULL,
  description TEXT,
  price INTEGER NOT NULL,
  rental_price INTEGER,
  
  category TEXT NOT NULL,
  type TEXT NOT NULL,
  region TEXT,
  
  is_rental BOOLEAN DEFAULT false,
  wore_once BOOLEAN DEFAULT false,
  fabric_transparency INTEGER CHECK (fabric_transparency BETWEEN 1 AND 5),
  prayer_friendly BOOLEAN DEFAULT false,
  wudu_compatible BOOLEAN DEFAULT false,
  
  size TEXT,
  condition TEXT,
  
  image_url TEXT,
  location TEXT,
  masjid_pickup BOOLEAN DEFAULT false,
  
  available_dates JSONB
);

ALTER TABLE products ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Products viewable by everyone"
ON products FOR SELECT
USING (true);

CREATE POLICY "Authenticated users can insert"
ON products FOR INSERT
WITH CHECK (true);