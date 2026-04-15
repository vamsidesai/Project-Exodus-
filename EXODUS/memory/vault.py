import json
import os
from core.state import ModeState

class IdentityVault:
    """
    The Inner Sanctum. Stores the Master's true identity, values, and secrets.
    Access is STRICTLY controlled by ModeState.
    """
    
    def __init__(self, vault_path="identity_vault.json"):
        self.vault_path = vault_path
        self._cache = {}
        # Initial Boot: Ensure vault exists
        if not os.path.exists(self.vault_path):
            self._initialize_clean_vault()

    def _initialize_clean_vault(self):
        """Creates an empty secure vault structure."""
        initial_data = {
            "master_profile": {
                "name": "Vamsi",
                "role": "Master",
                "values": ["Loyalty", "Growth", "Privacy"]
            },
            "secrets": {},
            "financial_context": {}
        }
        with open(self.vault_path, 'w') as f:
            json.dump(initial_data, f, indent=4)

    def read_identity(self, state: ModeState):
        """
        Returns Identity Data ONLY if unlocked and in Master Mode.
        """
        # HARD CHECK
        if state.mode != "MASTER":
            return {"error": "ACCESS_DENIED: Wrong Mode"}
        
        if state.identity_locked:
            return {"error": "ACCESS_DENIED: Vault Locked"}
            
        # Load Data
        with open(self.vault_path, 'r') as f:
            data = json.load(f)
            
        return data["master_profile"]

    def unlock(self, key: str, state: ModeState) -> bool:
        """
        Unlocks the vault for this session.
        In V1, this is a simulated key check.
        """
        # TODO: Implement real Argon2 hash verification
        if key == "exodus_init": # Placeholder
            state.identity_locked = False
            return True
        return False

    def lock(self, state: ModeState):
        state.identity_locked = True
