from rest_framework.response import Response


class MetadataMixin:
    def get_metadata(self, serialized_data):
        return {
            "drfapi": "1.0.0",
            "info": {
                "title": "Drinks API",
                "version": "1.0.0",
                "description": "This is the public API for DrinksAPI"
            },
            "servers": [
                {"url": "/api/v1"}
            ],
            "external_docs": {
                "url": "http://www.drinksapi.com",
                "description": "Access to cocktail and shot recipes"
            },
            "security": [
                {
                    "client_id": [],
                    "client_secret": []
                }
            ],
            "drinks": serialized_data  # Add the actual drinks data here
        }
