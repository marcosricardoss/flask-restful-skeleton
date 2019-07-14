"""Initialize the JWTManager by setting functionality to manage the token."""

def init(jwt):
    """Initialize the JWTManager.
    
    Parameters:    
        jwt (JWTManager): an instance of the jwt manager.
    """

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decoded_token):
        """Callback to check if a token is in the blacklist.
        
        Parameters:    
            decrypted_token (dict): a jwt token decrypted into a dictionary.
        """
        from app.model import TokenRepository
        return TokenRepository().is_token_revoked(decoded_token)
