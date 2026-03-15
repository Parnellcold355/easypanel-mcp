"""
EasyPanel API Client.

Handles all communication with the EasyPanel API using tRPC protocol.
EasyPanel uses tRPC for all API operations.
"""

import httpx
import logging
import json
from typing import Any, Optional
from config import EasyPanelConfig

logger = logging.getLogger(__name__)


class EasyPanelClient:
    """Client for interacting with EasyPanel API using tRPC."""

    def __init__(self, config: EasyPanelConfig):
        """
        Initialize EasyPanel client.

        Args:
            config: EasyPanel configuration settings
        """
        self.base_url = config.base_url.rstrip("/")
        self.api_key = config.api_key
        self.timeout = config.timeout
        self.verify_ssl = config.verify_ssl

        self._client: Optional[httpx.AsyncClient] = None
        self._token: Optional[str] = None

    async def connect(self) -> None:
        """Establish connection to EasyPanel API."""
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            timeout=self.timeout,
            verify=self.verify_ssl
        )
        
        # If API key looks like email:password, authenticate via tRPC
        if ":" in self.api_key and "@" in self.api_key:
            await self._authenticate_with_email_password()
        else:
            # Use API key as Bearer token (session token)
            self._client.headers["Authorization"] = f"Bearer {self.api_key}"
            logger.info(f"Connected to EasyPanel at {self.base_url} (Bearer token auth)")

    async def _authenticate_with_email_password(self) -> None:
        """Authenticate using email and password via tRPC."""
        try:
            email, password = self.api_key.split(":", 1)
            response = await self._client.post(
                "/api/trpc/auth.login",
                json={"json": {"email": email, "password": password}}
            )
            response.raise_for_status()
            result = response.json()
            token = result.get("result", {}).get("data", {}).get("json", {}).get("token")
            
            if token:
                self._token = token
                self._client.headers["Authorization"] = token
                logger.info(f"Authenticated to EasyPanel as {email}")
            else:
                raise RuntimeError("No token received from auth.login")
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            raise

    async def disconnect(self) -> None:
        """Close connection to EasyPanel API."""
        if self._client:
            await self._client.aclose()
            logger.info("Disconnected from EasyPanel")

    async def _trpc_request(
        self,
        procedure: str,
        input_data: Optional[dict[str, Any]] = None,
        method: str = "POST"
    ) -> Any:
        """
        Make tRPC request to EasyPanel API.

        Args:
            procedure: tRPC procedure name (e.g., "projects.listProjects")
            input_data: Input data for the procedure
            method: HTTP method (GET or POST). GET is used for query procedures.

        Returns:
            tRPC response data (the json payload inside result.data.json)

        Raises:
            RuntimeError: If request fails
        """
        if not self._client:
            raise RuntimeError("Client not connected. Call connect() first.")

        endpoint = f"/api/trpc/{procedure}"
        
        try:
            # Query procedures (list, get, inspect) use GET
            # Mutation procedures (create, update, delete) use POST
            query_procedures = ["list", "get", "inspect", "stats", "info", "check", "public"]
            is_query = any(q in procedure.lower() for q in query_procedures)
            
            if is_query or method == "GET":
                # tRPC GET requests encode input as JSON string in query param
                if input_data:
                    input_json = json.dumps(input_data)
                    response = await self._client.get(endpoint, params={"input": input_json})
                else:
                    response = await self._client.get(endpoint)
            else:
                # tRPC POST requests send JSON body with "json" wrapper
                payload = {"json": input_data} if input_data else {}
                response = await self._client.post(endpoint, json=payload)
            
            response.raise_for_status()
            result = response.json()
            
            # Extract data from tRPC response structure:
            # { "result": { "data": { "json": {...}, "meta": {...} } } }
            data = result.get("result", {}).get("data", {})
            if "json" in data:
                return data["json"]
            return data
            
        except httpx.HTTPStatusError as e:
            error_msg = e.response.text
            try:
                error_data = e.response.json()
                error_msg = error_data.get("error", {}).get("json", {}).get("message", error_msg)
            except:
                pass
            logger.error(f"tRPC error [{procedure}]: {error_msg}")
            raise RuntimeError(f"tRPC error: {error_msg}")
        except httpx.RequestError as e:
            logger.error(f"Request error [{procedure}]: {str(e)}")
            raise

    # ========== Project Management ==========
    # tRPC procedures: projects.listProjects, projects.createProject, 
    #                  projects.destroyProject, projects.inspectProject,
    #                  projects.getDockerContainers, projects.updateProjectEnv,
    #                  projects.updateAccess, projects.listProjectsAndServices
    
    async def list_projects(self) -> list[dict[str, Any]]:
        """List all projects."""
        try:
            result = await self._trpc_request("projects.listProjects")
            # Result is typically { data: [...] } or directly [...]
            if isinstance(result, dict) and "data" in result:
                return result.get("data", [])
            return result if isinstance(result, list) else []
        except Exception as e:
            logger.error(f"Error listing projects: {e}")
            return []

    async def get_project(self, project_id: str) -> dict[str, Any]:
        """Get project details (inspect)."""
        try:
            result = await self._trpc_request("projects.inspectProject", {"id": project_id})
            return result if isinstance(result, dict) else {}
        except Exception as e:
            logger.error(f"Error getting project: {e}")
            return {}

    async def create_project(
        self,
        name: str,
        description: Optional[str] = None
    ) -> dict[str, Any]:
        """Create a new project."""
        try:
            data = {"name": name}
            if description:
                data["description"] = description
            result = await self._trpc_request("projects.createProject", data)
            return result if isinstance(result, dict) else {}
        except Exception as e:
            logger.error(f"Error creating project: {e}")
            return {}

    async def delete_project(self, project_id: str) -> dict[str, Any]:
        """Delete a project."""
        try:
            result = await self._trpc_request("projects.destroyProject", {"id": project_id})
            return result if isinstance(result, dict) else {}
        except Exception as e:
            logger.error(f"Error deleting project: {e}")
            return {}

    # ========== Service Management ==========
    # tRPC procedures for apps:
    #   services.app.createService, services.app.deployService,
    #   services.app.destroyService, services.app.inspectService,
    #   services.app.restartService, services.app.startService,
    #   services.app.stopService, services.app.updateEnv,
    #   services.app.updateSourceImage, services.app.updateSourceGithub,
    #   services.app.updateSourceGit, services.app.updateSourceDockerfile,
    #   services.app.updateBuild, services.app.updateDeploy,
    #   services.app.updateResources, services.app.updatePorts,
    #   services.app.updateRedirects, services.app.updateBasicAuth,
    #   services.app.updateMaintenance, services.app.getExposedPorts,
    #   services.app.enableGithubDeploy, services.app.disableGithubDeploy,
    #   services.app.refreshDeployToken, services.app.uploadCodeArchive
    
    async def list_services(self, project_id: Optional[str] = None) -> list[dict[str, Any]]:
        """List all services, optionally filtered by project."""
        try:
            # First get projects with services
            if project_id:
                result = await self._trpc_request("projects.listProjectsAndServices")
                projects = result.get("data", []) if isinstance(result, dict) else result
                # Filter services by project
                services = []
                for proj in projects:
                    if proj.get("id") == project_id:
                        services = proj.get("services", [])
                        break
                return services
            else:
                # Get all projects and collect all services
                result = await self._trpc_request("projects.listProjectsAndServices")
                projects = result.get("data", []) if isinstance(result, dict) else result
                services = []
                for proj in projects:
                    services.extend(proj.get("services", []))
                return services
        except Exception as e:
            logger.error(f"Error listing services: {e}")
            return []

    async def get_service(self, service_id: str) -> dict[str, Any]:
        """Get service details (inspect)."""
        try:
            result = await self._trpc_request("services.app.inspectService", {"id": service_id})
            return result if isinstance(result, dict) else {}
        except Exception as e:
            logger.error(f"Error getting service: {e}")
            return {}

    async def create_service(
        self,
        name: str,
        project_id: str,
        image: str,
        config: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        """Create a new service (app type)."""
        try:
            data = {
                "projectId": project_id,
                "name": name,
                "sourceImage": image,
                **(config or {})
            }
            result = await self._trpc_request("services.app.createService", data)
            return result if isinstance(result, dict) else {}
        except Exception as e:
            logger.error(f"Error creating service: {e}")
            return {}

    async def update_service(
        self,
        service_id: str,
        config: dict[str, Any]
    ) -> dict[str, Any]:
        """Update service configuration."""
        try:
            # Determine which update method to use based on config keys
            data = {"id": service_id, **config}
            
            # Try generic update first
            for method in ["services.app.updateDeploy", "services.app.updateBasicAuth", 
                          "services.app.updateResources"]:
                try:
                    result = await self._trpc_request(method, data)
                    return result if isinstance(result, dict) else {}
                except RuntimeError:
                    continue
            return {}
        except Exception as e:
            logger.error(f"Error updating service: {e}")
            return {}

    async def delete_service(self, service_id: str) -> dict[str, Any]:
        """Delete a service."""
        try:
            result = await self._trpc_request("services.app.destroyService", {"id": service_id})
            return result if isinstance(result, dict) else {}
        except Exception as e:
            logger.error(f"Error deleting service: {e}")
            return {}

    async def restart_service(self, service_id: str) -> dict[str, Any]:
        """Restart a service."""
        try:
            result = await self._trpc_request("services.app.restartService", {"id": service_id})
            return result if isinstance(result, dict) else {}
        except Exception as e:
            logger.error(f"Error restarting service: {e}")
            return {}

    async def start_service(self, service_id: str) -> dict[str, Any]:
        """Start a service."""
        try:
            result = await self._trpc_request("services.app.startService", {"id": service_id})
            return result if isinstance(result, dict) else {}
        except Exception as e:
            logger.error(f"Error starting service: {e}")
            return {}

    async def stop_service(self, service_id: str) -> dict[str, Any]:
        """Stop a service."""
        try:
            result = await self._trpc_request("services.app.stopService", {"id": service_id})
            return result if isinstance(result, dict) else {}
        except Exception as e:
            logger.error(f"Error stopping service: {e}")
            return {}

    async def deploy_service(self, service_id: str) -> dict[str, Any]:
        """Deploy/redeploy a service."""
        try:
            result = await self._trpc_request("services.app.deployService", {"id": service_id})
            return result if isinstance(result, dict) else {}
        except Exception as e:
            logger.error(f"Error deploying service: {e}")
            return {}

    async def get_service_logs(
        self,
        service_id: str,
        lines: int = 100
    ) -> list[str]:
        """Get service logs."""
        # Note: EasyPanel doesn't expose logs via tRPC directly
        # This would need a different approach (Docker logs via API)
        logger.warning("Service logs not available via EasyPanel tRPC API")
        return []

    # ========== Network Management ==========
    # Note: EasyPanel manages networks automatically
    # Networks are created when services are deployed
    # No direct tRPC procedures for network management
    
    async def list_networks(self) -> list[dict[str, Any]]:
        """List all networks (not directly supported by EasyPanel)."""
        # EasyPanel doesn't expose networks directly via tRPC
        # Networks are managed automatically
        logger.info("Network listing not available via EasyPanel tRPC API")
        return []

    async def create_network(
        self,
        name: str,
        internal: bool = False,
        driver: str = "overlay"
    ) -> dict[str, Any]:
        """Create a new network (not directly supported by EasyPanel)."""
        logger.warning("Network creation not available via EasyPanel tRPC API")
        return {}

    async def delete_network(self, network_id: str) -> dict[str, Any]:
        """Delete a network (not directly supported by EasyPanel)."""
        logger.warning("Network deletion not available via EasyPanel tRPC API")
        return {}

    # ========== Deployment Management ==========
    # Deployments are handled via services.app.deployService
    
    async def list_deployments(self, project_id: Optional[str] = None) -> list[dict[str, Any]]:
        """List all deployments (via services)."""
        # Deployments are tied to services in EasyPanel
        return await self.list_services(project_id)

    async def get_deployment(self, deployment_id: str) -> dict[str, Any]:
        """Get deployment details (via service inspect)."""
        return await self.get_service(deployment_id)

    async def create_deployment(
        self,
        project_id: str,
        service_id: str,
        image: str,
        config: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        """Create a new deployment (update service source and deploy)."""
        try:
            # Update the service source image
            await self._trpc_request("services.app.updateSourceImage", {
                "id": service_id,
                "sourceImage": image
            })
            # Deploy the service
            result = await self._trpc_request("services.app.deployService", {"id": service_id})
            return result if isinstance(result, dict) else {}
        except Exception as e:
            logger.error(f"Error creating deployment: {e}")
            return {}

    async def get_deployment_logs(self, deployment_id: str) -> list[str]:
        """Get deployment logs (not directly available)."""
        logger.warning("Deployment logs not available via EasyPanel tRPC API")
        return []

    # ========== System Information ==========
    # tRPC procedures: monitor.getSystemStats, monitor.getServiceStats,
    #                  monitor.getStorageStats, monitor.getAdvancedStats,
    #                  monitor.getDockerTaskStats, monitor.getMonitorTableData
    
    async def get_system_info(self) -> dict[str, Any]:
        """Get system information."""
        try:
            result = await self._trpc_request("monitor.getSystemStats")
            return result if isinstance(result, dict) else {}
        except Exception as e:
            logger.error(f"Error getting system info: {e}")
            return {}

    async def get_system_stats(self) -> dict[str, Any]:
        """Get system statistics (CPU, memory, disk)."""
        try:
            result = await self._trpc_request("monitor.getSystemStats")
            return result if isinstance(result, dict) else {}
        except Exception as e:
            logger.error(f"Error getting system stats: {e}")
            return {}

    async def get_service_stats(self) -> dict[str, Any]:
        """Get service statistics."""
        try:
            result = await self._trpc_request("monitor.getServiceStats")
            return result if isinstance(result, dict) else {}
        except Exception as e:
            logger.error(f"Error getting service stats: {e}")
            return {}

    async def health_check(self) -> bool:
        """Check EasyPanel API health."""
        try:
            if not self._client:
                return False
            # Try to get session - if it works, API is healthy
            response = await self._client.get("/api/trpc/auth.getSession")
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False

    async def get_server_ip(self) -> str:
        """Get server IP address (not directly available)."""
        # EasyPanel doesn't expose server IP directly
        # Could be extracted from system stats
        try:
            stats = await self.get_system_stats()
            # Try to extract IP from stats
            return stats.get("ip", "") if isinstance(stats, dict) else ""
        except:
            return ""

    # ========== Additional Utilities ==========
    
    async def list_domains(self, service_id: Optional[str] = None) -> list[dict[str, Any]]:
        """List domains."""
        try:
            result = await self._trpc_request("domains.listDomains")
            if isinstance(result, dict) and "data" in result:
                return result.get("data", [])
            return result if isinstance(result, list) else []
        except Exception as e:
            logger.error(f"Error listing domains: {e}")
            return []

    async def create_domain(
        self,
        name: str,
        service_id: Optional[str] = None
    ) -> dict[str, Any]:
        """Create a new domain."""
        try:
            data = {"name": name}
            if service_id:
                data["serviceId"] = service_id
            result = await self._trpc_request("domains.createDomain", data)
            return result if isinstance(result, dict) else {}
        except Exception as e:
            logger.error(f"Error creating domain: {e}")
            return {}

    async def get_public_key(self) -> str:
        """Get Git public key."""
        try:
            result = await self._trpc_request("git.getPublicKey")
            if isinstance(result, dict):
                return result.get("publicKey", "")
            return str(result) if result else ""
        except Exception as e:
            logger.error(f"Error getting public key: {e}")
            return ""
