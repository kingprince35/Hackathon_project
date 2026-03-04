"""GST Rules Database - Simplified for MVP"""

GST_RULES = {
    # HSN Code -> GST Rate mapping
    "hsn_gst_rates": {
        "1001": 0,      # Wheat
        "1006": 5,      # Rice
        "0401": 0,      # Fresh milk
        "0402": 12,     # Cream
        "0403": 5,      # Yogurt
        "0406": 12,     # Cheese
        "2201": 0,      # Water
        "2202": 12,     # Soft drinks
        "8517": 18,     # Mobile phones
        "8471": 18,     # Computers
        "6403": 18,     # Footwear
        "6109": 12,     # T-shirts
        "3004": 12,     # Medicines
        "2710": 18,     # Petrol/Diesel
    },
    
    # Mandatory fields
    "mandatory_fields": [
        "invoice_number",
        "invoice_date",
        "gstin_seller",
        "gstin_buyer",
        "place_of_supply",
        "items"
    ],
    
    # GSTIN format: 15 characters
    "gstin_format": {
        "length": 15,
        "pattern": r"^\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}$"
    },
    
    # HSN code format: 4 or 8 digits
    "hsn_format": {
        "valid_lengths": [4, 8],
        "pattern": r"^\d{4}$|^\d{8}$"
    }
}

def get_gst_rate(hsn_code: str) -> float:
    """Get GST rate for HSN code"""
    return GST_RULES["hsn_gst_rates"].get(hsn_code, None)

def get_mandatory_fields():
    """Get list of mandatory fields"""
    return GST_RULES["mandatory_fields"]
