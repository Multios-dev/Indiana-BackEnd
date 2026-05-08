from __future__ import annotations

import base64
import json
from functools import lru_cache
from typing import Optional

import aiohttp
import requests
from pydantic import Field
from pydantic_settings import BaseSettings

global_aiohttp_session: aiohttp.ClientSession

# ---------------------------------------------------------------------------
#                               SETTINGS
# ---------------------------------------------------------------------------

class Settings(BaseSettings):
    # -------- Scaleway ----
    scw_region: str = Field("fr-par", alias="SCW_REGION")
    scw_secret_key: str = Field(..., alias="SCW_SECRET_KEY")
    scw_default_project_id: str = Field(..., alias="SCW_DEFAULT_PROJECT_ID")

    # -------- secrets -----
    database_url: str | None = None
    keycloak_url: str | None = None
    mailjet_api_key: str | None = None
    mailjet_base_url: str | None = None

    # -----------------------------------------------------------
    #                CHARGEMENT BLOQUANT DES SECRETS
    # -----------------------------------------------------------
    def hydrate(self, session: Optional[requests.Session] = None) -> None:
        """
        Remplit tous les champs manquants. Plante immédiatement si l’appel
        Scaleway échoue.
        """
        created = session is None
        if created:
            session = requests.Session()

        try:
            fields_to_load = (
                "redis_url",
                "postgres_dsn_async",
                "postgres_dsn_sync",
                "gemini_api_key",
                "gemini_api_url"  ,
                "llama_api_key",
                "llama_api_url",
                "x_api_key",
                "x_api_key_chat",
                "scrap_url",
                "api_key_scrap",
                "bnb_ref_url",
                "bnb_accounting_url",
                "api_key_bnb",
                "celery_broker_url",
                "celery_result_backend",
                "fernet_key",
                "netlify_access_token",
                "netlify_site_base_url",
                "email_api_key",
                "email_api_url",
                "voiceteris_api_url",
                "voiceteris_api_key",
                "qdrant_api_url",
                "qdrant_api_key",
                "mc_auth_url",
                "mc_auth_api_key"
            )
            # une seule requête : le bundle contient tout
            self._fetch_secret_bundle(session, fields_to_load)
        finally:
            if created:
                session.close()

    # -----------------------------------------------------------
    def _fetch_secret_bundle(
        self,
        session: requests.Session,
        fields: tuple[str, ...],
    ) -> None:
        """
        Lit le secret bundle JSON et hydrate les attributs demandés.
        """
        url = (
            "https://api.scaleway.com/secret-manager/v1beta1/regions/"
            f"{self.scw_region}/secrets/{self.scw_default_project_id}"
            "/versions/latest/access"
        )
        headers = {"X-Auth-Token": self.scw_secret_key}

        resp = session.get(url, headers=headers, timeout=5)
        if resp.status_code != 200:
            raise RuntimeError(f"Scaleway {resp.status_code} – {resp.text}")

        payload_str = base64.b64decode(resp.json()["data"]).decode()

        # 1) si c’est un JSON, on met à jour tous les attributs trouvés
        try:
            bundle = json.loads(payload_str)
            if isinstance(bundle, dict):
                for k, v in bundle.items():
                    attr = k.lower()             # "REDIS_URL" → "redis_url"
                    if attr in self.model_fields and getattr(self, attr) is None:
                        setattr(self, attr, v)
                return
        except json.JSONDecodeError:
            pass  # ce n’est pas du JSON, on continue

        # 2) sinon, on suppose que c’est la valeur du premier champ manquant
        for field in fields:
            if getattr(self, field) is None:
                setattr(self, field, payload_str)
                return


# ---------------------------------------------------------------------------
#                       SINGLETON UTILISABLE PARTOUT
# ---------------------------------------------------------------------------
@lru_cache
def get_settings() -> Settings:
    cfg = Settings()      # parse les variables d’environnement
    cfg.hydrate()         # bloque si un secret n’est pas récupérable
    return cfg