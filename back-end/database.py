import httpx
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

class SupabaseClient:
    def __init__(self):
        self.url = SUPABASE_URL
        self.headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json"
        }
    
    def table(self, table_name: str):
        return SupabaseTable(self.url, self.headers, table_name)

class SupabaseTable:
    def __init__(self, url, headers, table_name):
        self.url = f"{url}/rest/v1/{table_name}"
        self.headers = headers
        self.filters = []
    
    def select(self, columns="*"):
        self.columns = columns
        return self
    
    def eq(self, column, value):
        self.filters.append(f"{column}=eq.{value}")
        return self
    
    def ilike(self, column, value):
        self.filters.append(f"{column}=ilike.{value}")
        return self
    
    def gte(self, column, value):
        self.filters.append(f"{column}=gte.{value}")
        return self
    
    def lte(self, column, value):
        self.filters.append(f"{column}=lte.{value}")
        return self
    
    def execute(self):
        url = self.url
        if hasattr(self, 'columns'):
            url += f"?select={self.columns}"
        if self.filters:
            separator = "&" if "?" in url else "?"
            url += separator + "&".join(self.filters)
        
        response = httpx.get(url, headers=self.headers)
        return type('obj', (object,), {'data': response.json()})()
    
    def insert(self, data):
        response = httpx.post(self.url, json=data, headers=self.headers)
        return type('obj', (object,), {'data': response.json()})()
    
    def update(self, data):
        url = self.url
        if self.filters:
            url += "?" + "&".join(self.filters)
        response = httpx.patch(url, json=data, headers=self.headers)
        return type('obj', (object,), {'data': response.json()})()
    
    def delete(self):
        url = self.url
        if self.filters:
            url += "?" + "&".join(self.filters)
        response = httpx.delete(url, headers=self.headers)
        return type('obj', (object,), {'data': response.json()})()

def get_supabase():
    return SupabaseClient()