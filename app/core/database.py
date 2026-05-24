"""
Supabase database connection
"""
from supabase import create_client, Client
from app.core.config import settings


# create supabase client
supabase: Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_KEY
)

def get_supabase() -> Client:
    """Get supabase client"""
    return supabase