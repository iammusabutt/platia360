import jwt
from jwt import (
    ExpiredSignatureError,
    InvalidSignatureError,
    InvalidTokenError,
    DecodeError,
)
import frappe

@frappe.whitelist(allow_guest=True)
def identity():
    # Get token from header or query param
    token = frappe.get_request_header("Authorization")
    if token and token.startswith("Bearer "):
        token = token.split(" ")[1]
    elif not token:
        token = frappe.form_dict.get("token")

    if not token:
        return {
            "error": "missing_token",
            "message": "Authorization token is required (provide as 'Bearer <token>' or ?token=)",
        }

    # Get public key
    public_key = frappe.conf.get("jwt_public_key")
    if not public_key:
        return {
            "error": "missing_public_key",
            "message": "Server public key not configured. Please set 'jwt_public_key' in site_config.json",
        }

    try:
        # Decode and validate JWT
        payload = jwt.decode(token, public_key, algorithms=["RS256"])

        # Validate payload fields
        user = payload.get("email")
        if not user:
            return {
                "error": "missing_email",
                "message": "Token payload missing required field: 'email'",
            }

        # Validate ERPNext user
        if not frappe.db.exists("User", user):
            return {
                "error": "user_not_found",
                "message": f"No ERPNext user found for email '{user}'",
            }

        # Set logged-in user
        frappe.local.login_manager.login_as(user)
        frappe.local.db.commit()
        
        session_id = frappe.local.session.sid
        session_user = frappe.session.user
        session_data = frappe.local.session.data if hasattr(frappe.local.session, "data") else None

        return {
            "status": "success",
            "user": session_user,
            "payload": payload,
            "session_id": session_id,
            "session": session_data,
            "message": f"Session created successfully for {session_user}",
        }

    # Handle specific JWT exceptions
    except ExpiredSignatureError:
        return {"error": "token_expired", "message": "JWT token has expired. Please log in again."}

    except InvalidSignatureError:
        return {"error": "invalid_signature", "message": "JWT signature verification failed (wrong key pair or tampered token)."}

    except DecodeError:
        return {"error": "decode_error", "message": "JWT token could not be decoded (malformed or corrupted)."}

    except InvalidTokenError:
        return {"error": "invalid_token", "message": "Invalid JWT token (verification failed)."}

    # Catch-all
    except Exception as e:
        return {"error": "internal_error", "message": str(e)}

    

