from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from alembic.script import ScriptDirectory
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Set the sqlalchemy.url in the config from environment variable
config.set_main_option('sqlalchemy.url', os.getenv('POSTGRES_CONNECTION_STRING', ''))

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = None

def override_get_heads(scripts):
    """Override the get_heads method to return only the head we want based on environment"""
    original_get_heads = scripts.get_heads

    def get_heads():
        heads = original_get_heads()
        print(f"Original heads found: {heads}")
        
        if not heads:
            return heads

        # Determine which branch we want based on MULTITENANT env var
        is_multitenant = os.getenv("MULTITENANT", "true").lower() == "true"
        target_branch = 'multitenant' if is_multitenant else 'singletenant'
        print(f"Looking for heads with branch label: {target_branch}")
        
        # Filter heads to only include our target branch
        filtered_heads = []
        for head in heads:
            rev = scripts.get_revision(head)
            print(f"Checking revision {head} with branch labels: {rev.branch_labels}")
            if rev.branch_labels and target_branch in rev.branch_labels:
                filtered_heads.append(head)
        
        print(f"Filtered heads: {filtered_heads}")
        
        # If we have exactly one head after filtering, use that
        if len(filtered_heads) == 1:
            print(f"Using single filtered head: {filtered_heads[0]}")
            return [filtered_heads[0]]
            
        # If we still have multiple heads or no heads, use all heads
        print(f"Using all heads: {heads}")
        return heads

    return get_heads

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    # Create script directory
    script = ScriptDirectory.from_config(context.config)
    script.get_heads = override_get_heads(script)

    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        script=script
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Create script directory
    script = ScriptDirectory.from_config(context.config)
    script.get_heads = override_get_heads(script)

    # Get section and ensure URL is set from environment
    config_section = config.get_section(config.config_ini_section)
    
    connectable = engine_from_config(
        config_section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            script=script
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()