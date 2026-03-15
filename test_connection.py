"""
Test script to verify EasyPanel API connection (READ-ONLY).

This script only performs GET operations - no changes will be made.
Tests tRPC endpoints used by the MCP server.
"""

import asyncio
import sys
from config import config, EasyPanelConfig
from src.client import EasyPanelClient


async def test_connection():
    """Test connection to EasyPanel API (read-only operations)."""
    
    print("=" * 60)
    print("EasyPanel MCP - Connection Test (READ-ONLY)")
    print("=" * 60)
    print()
    
    # Show configuration (hiding full API key)
    api_key_preview = f"{config.easypanel.api_key[:8]}...{config.easypanel.api_key[-4:]}" if len(config.easypanel.api_key) > 12 else "***"
    auth_type = "Email/Password" if ":" in config.easypanel.api_key and "@" in config.easypanel.api_key else "API Key"
    print(f"📍 EasyPanel URL: {config.easypanel.base_url}")
    print(f"🔑 API Key: {api_key_preview}")
    print(f"🔐 Auth Type: {auth_type}")
    print(f"⏱️  Timeout: {config.easypanel.timeout}s")
    print(f"🔒 Verify SSL: {config.easypanel.verify_ssl}")
    print()
    
    client = EasyPanelClient(config.easypanel)
    
    try:
        # Connect
        print("🔌 Connecting to EasyPanel API...")
        await client.connect()
        print("✅ Connected successfully!")
        print()
        
        # Test 1: Health check
        print("🏥 Testing health check...")
        health = await client.health_check()
        print(f"   Status: {'✅ Healthy' if health else '⚠️  Unhealthy'}")
        print()
        
        # Test 2: List projects (READ-ONLY)
        print("📁 Testing: List projects (GET)...")
        projects = await client.list_projects()
        print(f"   ✅ Found {len(projects)} project(s)")
        for proj in projects[:3]:
            name = proj.get('name', 'Unknown') if isinstance(proj, dict) else proj
            proj_id = proj.get('id', 'Unknown') if isinstance(proj, dict) else 'N/A'
            print(f"      - {name} ({proj_id})")
        print()
        
        # Test 3: List networks (READ-ONLY)
        print("🌐 Testing: List networks (GET)...")
        networks = await client.list_networks()
        print(f"   ✅ Found {len(networks)} network(s)")
        for net in networks[:3]:
            name = net.get('name', 'Unknown') if isinstance(net, dict) else net
            net_id = net.get('id', 'Unknown') if isinstance(net, dict) else 'N/A'
            print(f"      - {name} ({net_id})")
        print()
        
        # Test 4: List services (READ-ONLY)
        print("🔧 Testing: List services (GET)...")
        services = await client.list_services()
        print(f"   ✅ Found {len(services)} service(s)")
        for svc in services[:3]:
            name = svc.get('name', 'Unknown') if isinstance(svc, dict) else svc
            svc_id = svc.get('id', 'Unknown') if isinstance(svc, dict) else 'N/A'
            print(f"      - {name} ({svc_id})")
        print()
        
        # Test 5: System info (READ-ONLY)
        print("💻 Testing: System info (GET)...")
        sys_info = await client.get_system_info()
        if sys_info:
            print(f"   ✅ System info retrieved")
            print(f"      {sys_info}")
        else:
            print(f"   ⚠️  No system info available")
        print()
        
        print("=" * 60)
        print("✅ ALL TESTS PASSED - Connection is working!")
        print("=" * 60)
        print()
        print("🎉 Your EasyPanel MCP is ready to use!")
        print()
        print("📚 Next steps:")
        print("   1. Configure your AI agent (Claude Desktop, etc.)")
        print("   2. See docs: https://dannymaaz.github.io/easypanel-mcp/")
        print()
        
        return True
        
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ CONNECTION FAILED")
        print("=" * 60)
        print()
        print(f"Error: {type(e).__name__}: {e}")
        print()
        print("Possible issues:")
        print("  1. Check your EASYPANEL_URL in .env (must include https://)")
        print("  2. Check your EASYPANEL_API_KEY in .env")
        print("  3. Verify your EasyPanel instance is running")
        print("  4. Check if SSL verification is needed (EASYPANEL_VERIFY_SSL)")
        print()
        print("For API Key authentication:")
        print("  - Generate an API key in EasyPanel settings")
        print("  - Use format: EASYPANEL_API_KEY=your_api_key")
        print()
        print("For Email/Password authentication:")
        print("  - Use format: EASYPANEL_API_KEY=email:password")
        print()
        return False
        
    finally:
        await client.disconnect()


if __name__ == "__main__":
    success = asyncio.run(test_connection())
    sys.exit(0 if success else 1)
